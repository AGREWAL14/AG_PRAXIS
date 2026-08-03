"""Describing the features: moments, correlation, mutual information, separability.

Nothing here fits a model that is kept. The two things that look like learning,
mutual information and the single-feature AUC, are measurements of one column at a
time against the label, and neither produces a predictor. The notebook keeps the
narrative and the printing; the logic lives here so it can be reused and tested.

The moment functions exist because the corpus does not fit in memory as one frame.
Each file contributes counts, a mean and two central moments while it is open, and
those combine afterwards into exactly the numbers a summary table needs, without the
rows ever being held together.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import leaves_list, linkage
from scipy.spatial.distance import squareform
from scipy.stats import rankdata
from sklearn.feature_selection import mutual_info_classif


# --------------------------------------------------------------------------
# moments, one file at a time
# --------------------------------------------------------------------------


def file_moments(df: pd.DataFrame, features) -> pd.DataFrame:
    """Count, mean, second and third central moments, range and zero count.

    The moments are computed on centred values rather than from sums of powers of
    the raw values. A feature like `Rate` reaches into the millions, and the cube of
    that summed over a million rows loses most of its precision to cancellation.

    One column is converted at a time rather than the whole frame at once. A capture
    file holds several hundred thousand rows, and the difference between one column in
    memory as float64 and forty-three of them is the difference between a few megabytes
    and a few gigabytes once the squares and cubes are added.
    """
    features = list(features)
    rows = []
    for column in features:
        values = df[column].to_numpy(dtype="float64")
        n = len(values)
        if n == 0:
            rows.append((column, 0, np.nan, 0.0, 0.0, np.nan, np.nan, 0))
            continue
        mean = values.mean()
        centred = values - mean
        rows.append(
            (
                column,
                n,
                mean,
                float((centred**2).sum()),
                float((centred**3).sum()),
                float(values.min()),
                float(values.max()),
                int((values == 0).sum()),
            )
        )
    return pd.DataFrame(
        rows, columns=["feature", "n", "mean", "m2", "m3", "min", "max", "n_zero"]
    )


def combine_moments(frames) -> pd.DataFrame:
    """Fold per-file moments into one set of moments over every row read.

    Two batches of the same feature combine into one by the standard parallel
    formulas: the counts add, the means blend in proportion to the counts, and each
    central moment picks up a correction term for the distance between the two
    means. Applied one file at a time this gives the same answer as reading the
    whole corpus at once.
    """
    combined = None
    for frame in frames:
        frame = frame.set_index("feature")
        if combined is None:
            combined = frame.copy()
            continue

        na, nb = combined["n"], frame["n"]
        n = na + nb
        delta = frame["mean"] - combined["mean"]

        mean = combined["mean"] + delta * nb / n
        m2 = combined["m2"] + frame["m2"] + delta**2 * na * nb / n
        m3 = (
            combined["m3"]
            + frame["m3"]
            + delta**3 * na * nb * (na - nb) / n**2
            + 3 * delta * (na * frame["m2"] - nb * combined["m2"]) / n
        )

        combined = pd.DataFrame(
            {
                "n": n,
                "mean": mean,
                "m2": m2,
                "m3": m3,
                "min": np.minimum(combined["min"], frame["min"]),
                "max": np.maximum(combined["max"], frame["max"]),
                "n_zero": combined["n_zero"] + frame["n_zero"],
            }
        )
    return combined.reset_index()


def summary_table(combined: pd.DataFrame, medians: pd.Series | None = None) -> pd.DataFrame:
    """Turn combined moments into the table a reader wants: spread, shape, emptiness.

    Skewness is the population coefficient, the third central moment over the
    standard deviation cubed. It is undefined for a feature that never varies, and
    is left as missing rather than as a zero that would read as symmetric.
    """
    frame = combined.set_index("feature")
    n = frame["n"].astype("float64")
    variance = frame["m2"] / n
    std = np.sqrt(variance)

    with np.errstate(divide="ignore", invalid="ignore"):
        skew = (frame["m3"] / n) / np.power(variance, 1.5)
    skew = skew.replace([np.inf, -np.inf], np.nan).where(variance > 0)

    out = pd.DataFrame(
        {
            "n": frame["n"],
            "mean": frame["mean"],
            "std": std,
            "min": frame["min"],
            "max": frame["max"],
            "skew": skew,
            "zero_share": frame["n_zero"] / n,
        }
    )
    if medians is not None:
        out.insert(4, "median", medians.reindex(out.index))
    return out.reset_index()


# --------------------------------------------------------------------------
# correlation
# --------------------------------------------------------------------------


def correlation(df: pd.DataFrame, features) -> pd.DataFrame:
    """Pearson correlation between every pair of features.

    A feature that holds one value in the rows given here has no correlation with
    anything, and pandas returns missing for it. Those stay missing; filling them
    with zero would present no relationship and no variation as the same thing.
    """
    return df[list(features)].astype("float64").corr()


def cluster_order(corr: pd.DataFrame, *, method: str = "average") -> list[str]:
    """Order features so that correlated ones sit next to each other.

    The distance between two features is one minus the absolute value of their
    correlation, so a pair moving together and a pair moving exactly opposite are
    both close. That is the right distance here: a feature that is the negative of
    another is as redundant as one that is its copy. Missing correlations become the
    maximum distance, which puts a feature with no variation off on its own.
    """
    distance = 1.0 - corr.abs().to_numpy(dtype="float64")
    distance = np.nan_to_num(distance, nan=1.0)
    distance = (distance + distance.T) / 2.0
    np.fill_diagonal(distance, 0.0)
    order = leaves_list(linkage(squareform(distance, checks=False), method=method))
    return [corr.columns[i] for i in order]


def high_correlation_pairs(corr: pd.DataFrame, threshold: float = 0.95) -> pd.DataFrame:
    """Every pair whose absolute correlation is at or above `threshold`.

    Each pair appears once. Two features this close carry nearly the same
    information, and an attribution method has no way to decide which of them
    deserves the credit, so it usually splits it between them.
    """
    values = corr.to_numpy(dtype="float64")
    upper = np.triu(np.ones_like(values, dtype=bool), k=1)
    rows, cols = np.where(upper & (np.abs(values) >= threshold))
    pairs = pd.DataFrame(
        {
            "feature_a": [corr.columns[i] for i in rows],
            "feature_b": [corr.columns[j] for j in cols],
            "correlation": values[rows, cols],
        }
    )
    pairs["abs_correlation"] = pairs["correlation"].abs()
    return pairs.sort_values("abs_correlation", ascending=False).reset_index(drop=True)


# --------------------------------------------------------------------------
# balanced draws
# --------------------------------------------------------------------------


def balanced_draw(labels, n_per_label: int, rng) -> np.ndarray:
    """Positions of at most `n_per_label` rows for each distinct label.

    Mutual information and AUC both read the label distribution they are given. A
    class holding a fifth of the corpus would otherwise set the answer for every
    feature on its own, and the small classes are the ones the question is about.
    """
    labels = np.asarray(labels)
    keep = []
    for label in np.unique(labels):
        positions = np.flatnonzero(labels == label)
        if len(positions) > n_per_label:
            positions = rng.choice(positions, size=n_per_label, replace=False)
        keep.append(positions)
    return np.sort(np.concatenate(keep))


# --------------------------------------------------------------------------
# single-feature separability
# --------------------------------------------------------------------------


def mutual_information(X, y, features, *, seed: int, n_neighbors: int = 3) -> pd.DataFrame:
    """Mutual information between each feature and the label, ranked.

    Measured one feature at a time, so this says what a column knows on its own and
    nothing about what two of them know together. The estimator is the
    nearest-neighbour one, which draws on random tie-breaking, so it takes the seed.
    """
    scores = mutual_info_classif(
        np.asarray(X, dtype="float64"),
        np.asarray(y),
        discrete_features=False,
        n_neighbors=n_neighbors,
        random_state=seed,
    )
    out = pd.DataFrame({"feature": list(features), "mutual_information": scores})
    out = out.sort_values("mutual_information", ascending=False).reset_index(drop=True)
    out.insert(0, "rank", np.arange(1, len(out) + 1))
    return out


def compare_rankings(left: pd.DataFrame, right: pd.DataFrame, *, left_name: str, right_name: str) -> pd.DataFrame:
    """Put two mutual information rankings side by side and record the movement."""
    merged = (
        left[["feature", "rank", "mutual_information"]]
        .rename(columns={"rank": f"rank_{left_name}", "mutual_information": f"mi_{left_name}"})
        .merge(
            right[["feature", "rank", "mutual_information"]].rename(
                columns={"rank": f"rank_{right_name}", "mutual_information": f"mi_{right_name}"}
            ),
            on="feature",
        )
    )
    merged["rank_change"] = merged[f"rank_{left_name}"] - merged[f"rank_{right_name}"]
    return merged.sort_values(f"rank_{left_name}").reset_index(drop=True)


def _auc_every_feature(values_a: np.ndarray, values_b: np.ndarray) -> np.ndarray:
    """AUC of every feature at once for one pair of classes, direction removed.

    The AUC of a single feature is the rank-sum statistic, so ranking the pooled
    values once gives the answer for all of them together. A feature that separates
    the two classes perfectly the wrong way round is as useful as one that separates
    them perfectly the right way round, and a threshold can be set either way, so
    anything below a half is reflected back above it. Half is then the floor and
    means the two classes are indistinguishable on that feature.
    """
    n_a, n_b = len(values_a), len(values_b)
    ranks = rankdata(np.vstack([values_a, values_b]), axis=0)
    auc = (ranks[:n_a].sum(axis=0) - n_a * (n_a + 1) / 2) / (n_a * n_b)
    return np.maximum(auc, 1.0 - auc)


def pairwise_best_auc(X, y, features, *, class_order=None):
    """For every pair of classes, the best AUC any single feature reaches.

    A pair with a high number is separable by one column and should not be confused
    by any model that reads that column. A pair near a half has no single feature
    telling it apart, and a model that gets it right has to combine several.

    Returns the square matrix of best AUCs and one row per pair naming the feature
    that achieved it.
    """
    X = np.asarray(X, dtype="float64")
    y = np.asarray(y)
    features = list(features)
    classes = list(class_order) if class_order is not None else sorted(np.unique(y).tolist())

    rows_of = {label: X[y == label] for label in classes}
    matrix = pd.DataFrame(np.nan, index=classes, columns=classes, dtype="float64")
    pairs = []

    for i, label_a in enumerate(classes):
        for label_b in classes[i + 1 :]:
            auc = _auc_every_feature(rows_of[label_a], rows_of[label_b])
            best = int(np.argmax(auc))
            order = np.argsort(auc)[::-1]
            matrix.loc[label_a, label_b] = matrix.loc[label_b, label_a] = auc[best]
            pairs.append(
                {
                    "class_a": label_a,
                    "class_b": label_b,
                    "best_auc": float(auc[best]),
                    "best_feature": features[best],
                    "second_feature": features[order[1]] if len(order) > 1 else None,
                    "second_auc": float(auc[order[1]]) if len(order) > 1 else None,
                    "n_features_above_0_9": int((auc >= 0.9).sum()),
                }
            )

    np.fill_diagonal(matrix.values, 1.0)
    return matrix, pd.DataFrame(pairs).sort_values("best_auc").reset_index(drop=True)


# --------------------------------------------------------------------------
# axes
# --------------------------------------------------------------------------


def log_axis(values, *, span_needed: float = 1e2):
    """Whether a feature needs a log axis, and where its linear region should end.

    The test is how far the largest value sits above the typical one, not how far it
    sits above the smallest. A feature scattered around five reaches close to zero
    somewhere in a million rows, and dividing by that would call for a log axis on a
    distribution that has no tail at all.

    The threshold returned is for a symmetric log scale rather than a plain log
    scale, because most of these features take the value zero often and a plain log
    axis drops those rows without saying so. Below the threshold the axis is linear,
    so the zeros are drawn where they belong.
    """
    values = np.asarray(values, dtype="float64")
    values = values[np.isfinite(values)]
    positive = values[values > 0]
    if positive.size == 0:
        return False, None
    typical = np.median(positive)
    if typical <= 0 or positive.max() / typical < span_needed:
        return False, None
    return True, float(max(np.quantile(positive, 0.01), positive.min()))
