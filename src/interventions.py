"""The five ways of making the rare classes visible, one per run.

Each of these is one change to a run that is otherwise the sequence model exactly
as its parent trained it: same windows, same split, same architecture, same ten
epochs at batch 32, same seed. They divide into two kinds, and the difference
matters when reading a result.

Three of them change what the model learns. Weighting the classes in the loss and
replacing the loss with a focal one both change the size of the gradient a rare
window contributes. Oversampling changes how many times the model sees one.

Two of them change nothing about training and only change how a trained model's
output is turned into an answer. Logit adjustment subtracts the class priors from
the scores. Per-class thresholds divide each score by a number chosen for that
class. A run of either kind trains the same model its parent did and then decides
differently.

Nothing here reads the test partition. The priors and the class weights come from
the training rows, and the thresholds are chosen on validation.
"""

from __future__ import annotations

import numpy as np
from sklearn.metrics import f1_score

from src import sequence as sq

# --------------------------------------------------------------------------
# counting the classes
# --------------------------------------------------------------------------


def class_counts(y, n_classes: int) -> np.ndarray:
    """How many rows each class holds, including the classes holding none."""
    return np.bincount(np.asarray(y).astype("int64"), minlength=int(n_classes))


def priors(y, n_classes: int) -> np.ndarray:
    """Each class's share of the rows."""
    counts = class_counts(y, n_classes)
    return counts / max(counts.sum(), 1)


# --------------------------------------------------------------------------
# the three that change what the model learns
# --------------------------------------------------------------------------


def inverse_frequency_weights(y, n_classes: int) -> dict:
    """Weight per class, `N / (K * n_c)`, so the mean weight is 1.

    A class with a thousandth of the rows carries a thousand times the weight per
    row, and the average row carries the same weight it did without any weighting
    at all. Normalising matters: weights that average to something other than 1
    scale every gradient in the run, which would be a second change on top of the
    reweighting.

    A class with no rows would divide by zero. It gets weight 1, which affects
    nothing, because a class with no rows contributes no term to the loss.
    """
    counts = class_counts(y, n_classes)
    total = counts.sum()
    weights = np.ones(int(n_classes), dtype="float64")
    present = counts > 0
    weights[present] = total / (present.sum() * counts[present])
    return {int(code): float(weight) for code, weight in enumerate(weights)}


def focal_loss(gamma: float = 2.0, alpha: float = 0.25):
    """Categorical focal cross-entropy, Keras's own implementation.

    Cross-entropy asks every window for the same amount of attention. Focal loss
    multiplies each window's term by `(1 - p)**gamma`, where `p` is the
    probability the model gave the right answer, so a window it already answers
    confidently contributes almost nothing and a window it gets wrong contributes
    nearly all of its term. On a corpus where a handful of classes hold most of
    the rows, most of the confident windows belong to those classes.

    Keras's version is used rather than one written here, because a loss written
    here would have to be registered by name before a saved model could be loaded
    again, and a run whose model cannot be read back is not much of a record.
    """
    import keras

    return keras.losses.CategoricalFocalCrossentropy(gamma=float(gamma), alpha=float(alpha))


def oversample_index(y, n_classes: int, *, target: int | None = None, seed: int = 42):
    """An index into `y` drawing every class up to `target` rows, with replacement.

    Classes at or above `target` keep every row they have and gain nothing.
    Classes below it are drawn from repeatedly until they reach it, so the model
    sees a rare window several times per epoch rather than once.

    `target` defaults to the median class size. The median is not the largest
    class on purpose: drawing every class up to the largest would multiply the
    training set five times over, and drawing the smallest class up to it would
    repeat two dozen windows sixty thousand times, which is a statement about
    those two dozen windows rather than about the class.

    The returned index is sorted, so the rows keep the order the file has and the
    only difference from the training set it came from is which rows appear more
    than once.
    """
    y = np.asarray(y).astype("int64")
    counts = class_counts(y, n_classes)
    present = counts[counts > 0]
    if target is None:
        target = int(np.median(present))
    rng = np.random.default_rng(int(seed))

    keep = [np.arange(len(y))]
    for code in range(int(n_classes)):
        where = np.flatnonzero(y == code)
        short = int(target) - len(where)
        if len(where) and short > 0:
            keep.append(rng.choice(where, size=short, replace=True))
    return np.sort(np.concatenate(keep)), int(target)


def resampling_record(y_before, y_after, n_classes: int, *, target: int, classes) -> dict:
    """What the oversampling did, per class, for the run's metrics."""
    before = class_counts(y_before, n_classes)
    after = class_counts(y_after, n_classes)
    largest = int(after.max())
    smallest_before = int(before[before > 0].min())
    ratio_before = float(before.max()) / max(smallest_before, 1)
    ratio_after = float(largest) / max(int(target), 1)
    return {
        "rule": "every class drawn up to the median class size, with replacement",
        "target_per_class": int(target),
        "n_train_before": int(before.sum()),
        "n_train_after": int(after.sum()),
        "largest_class_windows": largest,
        "imbalance_before": round(ratio_before, 1),
        "imbalance_after": round(ratio_after, 1),
        "not_class_parity": (
            f"Classes at or above the target keep the count they had, so this is not full "
            f"class parity. The largest class holds {largest:,} windows against a target of "
            f"{int(target):,}, which is {ratio_after:,.1f} to 1 after the resampling against "
            f"{ratio_before:,.0f} to 1 before it. The classes above the target are untouched."
        ),
        "per_class": {
            str(label): {
                "before": int(before[code]),
                "after": int(after[code]),
                "times_repeated": round(float(after[code]) / max(int(before[code]), 1), 2),
            }
            for code, label in enumerate(classes)
        },
    }


# --------------------------------------------------------------------------
# the two that change only how a trained model decides
# --------------------------------------------------------------------------


def argmax_decision():
    """The rule every run uses unless it is the thing being changed."""

    def decide(probabilities):
        return np.asarray(probabilities).argmax(axis=1)

    return decide


def logit_adjusted_decision(prior, tau: float = 1.0):
    """Subtract the class priors from the scores before taking the largest.

    A softmax trained on this corpus learns the class sizes along with everything
    else, so a rare class has to clear a bar the common ones do not. Taking
    `log p - tau * log prior` removes that bar: a class is chosen when its score
    is high relative to how often it appears, rather than high outright. At
    `tau` 0 the rule is the ordinary largest-score rule.

    The priors come from the training rows. No validation or test row is read.
    """
    prior = np.asarray(prior, dtype="float64")
    offset = float(tau) * np.log(np.clip(prior, 1e-12, None))

    def decide(probabilities):
        scores = np.log(np.clip(np.asarray(probabilities, dtype="float64"), 1e-12, None))
        return (scores - offset).argmax(axis=1)

    return decide


def threshold_decision(thresholds):
    """Divide each class's score by its own threshold, then take the largest.

    A threshold below 1 makes a class easier to choose and a threshold of 1
    leaves it where it was, so a run with every threshold at 1 decides exactly
    the way the ordinary rule does. Dividing rather than testing each score
    against its threshold in turn means every window still gets exactly one
    answer, with no window left undecided and none claimed by two classes.
    """
    thresholds = np.asarray(thresholds, dtype="float64")

    def decide(probabilities):
        return (np.asarray(probabilities, dtype="float64") / thresholds).argmax(axis=1)

    return decide


def tune_thresholds(probabilities, y_true, *, n_classes: int, grid, labels=None) -> tuple:
    """Choose a threshold per class on the partition it is handed, one pass.

    Every threshold starts at 1, which is the ordinary rule, and the classes are
    visited from the rarest upward. Each class's threshold is set to the grid
    value that gives the best macro-F1 with the other thresholds held where they
    are, and it is only moved if it improves on what the run already has. One
    pass rather than repeated passes, fixed before the run, so the number of
    times the partition is read is not decided by looking at the result.

    Macro-F1 is what is maximised because macro-F1 is what this project reports.

    The caller passes validation probabilities. Nothing here knows what partition
    it has been given, so the caller is the one place that has to be right about
    it.
    """
    probabilities = np.asarray(probabilities, dtype="float64")
    y_true = np.asarray(y_true).astype("int64")
    n_classes = int(n_classes)
    labels_range = list(range(n_classes))
    grid = [float(v) for v in grid]

    def macro(thresholds):
        predicted = threshold_decision(thresholds)(probabilities)
        return float(f1_score(y_true, predicted, labels=labels_range, average="macro", zero_division=0))

    thresholds = np.ones(n_classes, dtype="float64")
    started = macro(thresholds)
    best = started
    order = list(np.argsort(class_counts(y_true, n_classes), kind="stable"))

    trace = []
    for code in order:
        scores = []
        for value in grid:
            trial = thresholds.copy()
            trial[code] = value
            scores.append(macro(trial))
        position = int(np.argmax(scores))
        if scores[position] > best:
            thresholds[code] = grid[position]
            best = scores[position]
        trace.append(
            {
                "class": str(labels[code]) if labels is not None else int(code),
                "threshold": float(thresholds[code]),
                "macro_f1": round(float(best), 6),
            }
        )

    record = {
        "rule": "one score divided by one threshold per class, largest wins",
        "tuned_on": "validation",
        "grid": grid,
        "order": "rarest class first, by count in the partition tuned on",
        "thresholds": {
            (str(labels[code]) if labels is not None else int(code)): float(thresholds[code])
            for code in range(n_classes)
        },
        "validation_macro_f1_before": round(started, 6),
        "validation_macro_f1_after": round(best, 6),
        "n_thresholds_moved": int((thresholds != 1.0).sum()),
        "caveats": [
            "One greedy pass in an order fixed before the run, rarest class first. Each "
            "threshold is chosen with the others held where they are, so a different order "
            "could reach different thresholds. These are not a derived optimum.",
            "The thresholds were chosen to raise macro-F1 on validation. That they raise it "
            "on test is not established here. The test partition is scored once, with these "
            "thresholds already fixed.",
        ],
        "trace": trace,
    }
    return thresholds, record


# --------------------------------------------------------------------------
# the comparison blocks a run reports
# --------------------------------------------------------------------------


def comparison_block(metrics, parent, *, run_id, classes, threshold, note, with_mean=False) -> dict:
    """One comparison against the parent run, on one set of classes.

    The per-class figures come from `sequence.comparison_against`, which is what
    every comparison in this project is built with. Two things are done to what
    it returns. Its line about the two runs being scored on different partitions
    is removed, because here they are not: a run and its parent are scored on the
    same windows, and `note` says so. And a group mean is added where the set of
    classes is one whose average is worth reading as a number in its own right.
    """
    block = sq.comparison_against(
        metrics, parent, run_id=run_id, classes=list(classes), threshold=threshold
    )
    block.pop("test_partitions_differ", None)
    block["test_items"] = note
    if with_mean:
        block["mean_f1"] = mean_f1(metrics, parent, classes)
    return block


def mean_f1(metrics, parent, classes) -> dict:
    """Mean per-class F1 across `classes`, on both sides, and the difference."""
    classes = list(classes)
    here = float(np.mean([metrics["per_class_f1"][c] for c in classes]))
    there = float(np.mean([parent["per_class_f1"][c] for c in classes]))
    return {
        "n_classes": len(classes),
        "classes": classes,
        "parent": there,
        "this_run": here,
        "difference": here - there,
    }
