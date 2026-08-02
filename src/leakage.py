"""Between-capture variance, and the row sampling the leakage tests run on.

A capture file holds one class recorded in one session. If a feature's distribution
sits in a different place in each session, then the session is readable from the
feature, and a model can answer the question "which recording is this" instead of
the question it was asked. These functions measure how far each feature moves
between recordings compared with how much it moves inside one.

Nothing here fits or trains. The notebook keeps the narrative and the printing.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# --------------------------------------------------------------------------
# what counts as one recording
# --------------------------------------------------------------------------


def capture_key(capture_id: str, partition: str, tier: str) -> str:
    """The identifier of one recording session.

    For a class recorded several times the chunk numbering restarts in each
    partition, so a train chunk and a test chunk carrying the same number are two
    different recordings and the partition has to stay in the key. For a class
    recorded once the two files are the two halves of a single session, so both
    files carry the same key and are pooled back together.
    """
    return f"{capture_id}_{partition}" if tier == "A" else capture_id


# --------------------------------------------------------------------------
# moments, one capture at a time
# --------------------------------------------------------------------------


def finite_rows(df: pd.DataFrame) -> np.ndarray:
    """Boolean mask of the rows where every value is finite."""
    return np.isfinite(df.to_numpy(dtype="float64", na_value=np.nan)).all(axis=1)


def sample_rows(df: pd.DataFrame, n: int, rng) -> pd.DataFrame:
    """At most `n` rows drawn without replacement, left in their original order."""
    if len(df) <= n:
        return df
    index = np.sort(rng.choice(len(df), size=n, replace=False))
    return df.iloc[index]


def moments(df: pd.DataFrame, features) -> pd.DataFrame:
    """Row count, mean and variance of each feature in one capture file.

    Computed while the file is open and returned as three numbers per feature, so
    a ranking over the whole corpus never needs the rows in memory at once.
    """
    features = list(features)
    frame = df[features].astype("float64")
    return pd.DataFrame(
        {
            "feature": features,
            "n": len(frame),
            "mean": frame.mean().to_numpy(dtype="float64"),
            "var": frame.var(ddof=0).to_numpy(dtype="float64"),
        }
    )


def pool_moments(long: pd.DataFrame, by: str = "capture") -> pd.DataFrame:
    """Combine the moments of several files into the moments of one capture.

    Where a session was stored as two files, reading them as two recordings would
    understate the distance between recordings. The combined mean and variance
    follow from the counts, so the files do not have to be read again.
    """
    frame = long.copy()
    frame["weighted_mean"] = frame["n"] * frame["mean"]
    frame["weighted_second"] = frame["n"] * (frame["var"] + frame["mean"] ** 2)

    grouped = frame.groupby([by, "feature"], sort=False)[
        ["n", "weighted_mean", "weighted_second"]
    ].sum()
    mean = grouped["weighted_mean"] / grouped["n"]
    var = (grouped["weighted_second"] / grouped["n"]) - mean**2

    return pd.DataFrame({"n": grouped["n"], "mean": mean, "var": var.clip(lower=0)}).reset_index()


# --------------------------------------------------------------------------
# the ratio
# --------------------------------------------------------------------------


def _ratio(between, within) -> np.ndarray:
    """between / within, with the two degenerate cases named rather than hidden.

    A feature that is constant inside every capture but differs between them has
    no within-capture variance to divide by. That is the strongest possible form
    of the effect, so it is recorded as infinite rather than as missing. A feature
    that is the same constant everywhere gets zero.
    """
    between = np.asarray(between, dtype="float64")
    within = np.asarray(within, dtype="float64")
    out = np.full(between.shape, np.nan)
    positive = within > 0
    out[positive] = between[positive] / within[positive]
    out[~positive & (between > 0)] = np.inf
    out[~positive & (between <= 0)] = 0.0
    return out


def variance_ratio(pooled: pd.DataFrame) -> pd.DataFrame:
    """Between-capture variance over mean within-capture variance, per feature.

    Each capture contributes one mean, and the spread of those means across
    captures is the between-capture variance. The within-capture variance is the
    average of the per-capture variances. A large ratio says the feature sits in a
    different place in each recording while holding still inside each one, which
    is exactly what a model would read to tell the recordings apart.
    """
    grouped = pooled.groupby("feature", sort=False)
    out = pd.DataFrame(
        {
            "n_captures": grouped["mean"].size(),
            "between_var": grouped["mean"].var(ddof=0),
            "within_var": grouped["var"].mean(),
            "grand_mean": grouped["mean"].mean(),
            "min_capture_mean": grouped["mean"].min(),
            "max_capture_mean": grouped["mean"].max(),
        }
    )
    out["ratio"] = _ratio(out["between_var"], out["within_var"])
    return out.sort_values("ratio", ascending=False)


def variance_ratio_by_class(
    pooled: pd.DataFrame, capture_labels: pd.Series, *, min_captures: int = 2
) -> pd.DataFrame:
    """The same ratio computed inside one class at a time.

    Across the whole corpus a feature that separates the classes also separates the
    captures, because a capture holds one class, so a high ratio there can mean
    either. Restricting to the captures of a single class holds the class fixed,
    and what is left is the difference between recordings of the same attack.
    Classes with fewer than `min_captures` recordings cannot answer the question
    and are left out.
    """
    labels = capture_labels.reindex(pooled["capture"]).to_numpy()
    frame = pooled.assign(label=labels)

    per_class = {}
    for label, group in frame.groupby("label", sort=True):
        if group["capture"].nunique() < min_captures:
            continue
        per_class[label] = variance_ratio(group)["ratio"]

    if not per_class:
        return pd.DataFrame(
            columns=["n_classes", "within_class_median_ratio", "within_class_max_ratio"]
        )

    wide = pd.DataFrame(per_class)
    summary = pd.DataFrame(
        {
            "n_classes": wide.notna().sum(axis=1),
            "within_class_median_ratio": wide.median(axis=1, skipna=True),
            "within_class_max_ratio": wide.max(axis=1, skipna=True),
        }
    )
    return summary.join(wide.add_prefix("ratio_"))


# --------------------------------------------------------------------------
# splits
# --------------------------------------------------------------------------


def json_number(value):
    """A number JSON can hold, with the non-finite cases named rather than dropped.

    A ratio is legitimately infinite when a feature is constant inside every capture,
    and JSON has no way to write that, so it becomes the word instead of a number
    that would be read back as if it were finite.
    """
    value = float(value)
    if np.isnan(value):
        return None
    if np.isinf(value):
        return "infinite" if value > 0 else "-infinite"
    return value


def holdout_captures(frame: pd.DataFrame, *, capture_col: str, label_col: str) -> dict:
    """The last capture of each class in name order, to be held out.

    Name order is used rather than an arbitrary choice so that the same capture is
    held out on every run, and the split is reproducible without recording it.
    """
    return {
        label: sorted(group[capture_col].unique())[-1]
        for label, group in frame.groupby(label_col, sort=True)
    }
