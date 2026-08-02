"""The capture-file naming rule, and the per-capture scans built on top of it.

`parse_capture` is the single place the project decides what class a file belongs
to and which capture it came from. Every notebook from NB02 onward imports it
rather than re-deriving the rule, so that a change to the naming convention is a
change in one file.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import numpy as np
import pandas as pd

from .inventory import count_data_rows

# --------------------------------------------------------------------------
# the naming rule
# --------------------------------------------------------------------------


def parse_capture(filename):
    """Split a capture filename into its capture id, class label, and partition.

    `TCP_IP-DDoS-ICMP1_train.pcap.csv` -> capture ICMP1 of class DDoS-ICMP, train.

    The trailing digits are the capture number within a class, so stripping them
    gives the class. The `TCP_IP-` prefix is a grouping in the filenames rather
    than part of the class name, and `ARP_Spoofing` is the filename spelling of
    the class called Spoofing.
    """
    n = os.path.basename(filename).replace('.pcap.csv', '')
    partition = 'test' if n.endswith('_test') else 'train'
    n = re.sub(r'_(train|test)$', '', n)
    capture_id = n
    label = re.sub(r'\d+$', '', n).replace('TCP_IP-', '')
    if label == 'ARP_Spoofing':
        label = 'Spoofing'
    return {'capture_id': capture_id, 'label': label, 'partition': partition}


def group_six(label: str) -> str:
    """The 6-class grouping. Order matters: MQTT-DDoS is MQTT, not DDoS."""
    if label == "Benign":
        return "Benign"
    if label.startswith("DDoS"):
        return "DDoS"
    if label.startswith("DoS"):
        return "DoS"
    if label.startswith("MQTT-"):
        return "MQTT"
    if label.startswith("Recon-"):
        return "Recon"
    if label == "Spoofing":
        return "Spoofing"
    return "UNMAPPED"


def group_two(label: str) -> str:
    """The 2-class grouping."""
    return "Benign" if label == "Benign" else "Attack"


# --------------------------------------------------------------------------
# reading captures
# --------------------------------------------------------------------------


def read_capture(
    path: Path | str, *, frac: float = 1.0, known_rows: int | None = None, floor: int = 1000
) -> pd.DataFrame:
    """Read a capture file, or its opening `frac` of rows.

    Reading one file at a time is what makes a subsample stratified by class,
    because one file holds exactly one class. The subsample is the head of the
    file rather than a random draw from it, because stopping the reader early is
    the only version of this that is actually cheap. Rows inside a capture are in
    the order the extractor wrote them, so the head is a contiguous slice of the
    session and not a sample of it. That is fine for a screen and wrong for an
    estimate, which is why nothing quantitative is taken from it.
    """
    if frac >= 1.0:
        return pd.read_csv(path)
    total = known_rows if known_rows is not None else count_data_rows(path)
    return pd.read_csv(path, nrows=max(floor, int(round(total * frac))))


def column_stats(df: pd.DataFrame) -> dict:
    """Per column: how many distinct values it takes, and the value if only one."""
    stats = {}
    for col in df.columns:
        values = pd.unique(df[col].dropna())
        stats[col] = {
            "n_unique": int(len(values)),
            "value": values[0] if len(values) == 1 else None,
        }
    return stats


def scan_captures(paths, *, frac: float = 1.0, known_rows: dict | None = None, progress_every: int = 10):
    """One pass over the capture files, returning rows read and per-column stats."""
    scans = {}
    for i, path in enumerate(paths, start=1):
        name = Path(path).name
        df = read_capture(path, frac=frac, known_rows=(known_rows or {}).get(name))
        scans[name] = {"n_rows_read": int(len(df)), "columns": column_stats(df)}
        if progress_every and i % progress_every == 0:
            print(f"  scanned {i}/{len(paths)} files")
        del df
    return scans


# --------------------------------------------------------------------------
# the constant-within-capture check
# --------------------------------------------------------------------------


def capture_constant_columns(scans: dict) -> pd.DataFrame:
    """Find columns that hold one value inside a capture but differ between captures.

    A column like that carries the identity of the recording session. A model
    reading it can tell which file a row came from, which is not the same as
    telling which attack it represents.

    A capture session is stored as two files, one per side of the distributed
    split, so a value fixed for a session shows up as constant in both of them.

    Returns one row per column: in how many files it held a single value, and
    how many distinct values those single values took. A column that varies
    inside its files contributes no values at all, so `distinct_values` of zero
    means it was never constant, not that it is empty. Read the two counts
    together.
    """
    n_files = len(scans)
    columns = sorted({c for s in scans.values() for c in s["columns"]})

    rows = []
    for col in columns:
        constant_in, values = 0, []
        for scan in scans.values():
            stat = scan["columns"].get(col)
            if stat is None:
                continue
            if stat["n_unique"] <= 1:
                constant_in += 1
                if stat["value"] is not None:
                    values.append(stat["value"])
        distinct = sorted({_hashable(v) for v in values})
        rows.append(
            {
                "column": col,
                "constant_in_files": constant_in,
                "of_files": n_files,
                "constant_in_every_file": constant_in == n_files,
                "distinct_values_across_files": len(distinct),
                "values": distinct,
            }
        )

    frame = pd.DataFrame(rows)
    return frame.sort_values(
        ["distinct_values_across_files", "constant_in_files"], ascending=False
    ).reset_index(drop=True)


def _hashable(value):
    """Round floats before de-duplicating so 1.0000000001 and 1.0 are one value."""
    if isinstance(value, (float, np.floating)):
        return round(float(value), 10)
    if isinstance(value, (int, np.integer)):
        return int(value)
    return str(value)


def jsonable(obj):
    """Convert numpy scalars and paths so json.dump will accept the structure."""
    if isinstance(obj, dict):
        return {str(k): jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [jsonable(v) for v in obj]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    if isinstance(obj, Path):
        return str(obj)
    return obj
