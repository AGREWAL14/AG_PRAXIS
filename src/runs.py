"""Writing a run to disk, and the metrics every run reports.

A run is a directory holding five files: the configuration it was produced under,
its metrics, the true labels, the predicted labels, and the fitted model. Always
the same five, so a result can be re-read later without the notebook that made it.

`fit_and_save` exists so that fitting and saving are a single statement. A cell that
fits in one statement and saves in the next loses the fit if the session drops in
between, and a Colab session drops. Nothing here prints; the notebook keeps the
narrative and the printing.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from sklearn.metrics import accuracy_score, f1_score


# --------------------------------------------------------------------------
# metrics
# --------------------------------------------------------------------------


def classification_metrics(y_true, y_pred) -> dict:
    """Accuracy, macro-F1, weighted-F1 and per-class F1, with the two baselines.

    The baselines are carried alongside the scores because accuracy on its own is
    unreadable when the number of classes changes between runs. Chance is one over
    the number of classes; the majority rate is what always answering the largest
    class would score.
    """
    y_true = np.asarray(y_true).astype(str)
    y_pred = np.asarray(y_pred).astype(str)
    labels = sorted(set(y_true.tolist()) | set(y_pred.tolist()))
    per_class = f1_score(y_true, y_pred, average=None, labels=labels, zero_division=0)
    support = {label: int((y_true == label).sum()) for label in labels}

    return {
        "n_test": int(len(y_true)),
        "n_classes": len(labels),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        "weighted_f1": float(f1_score(y_true, y_pred, average="weighted", zero_division=0)),
        "per_class_f1": {label: float(v) for label, v in zip(labels, per_class)},
        "support": support,
        "chance_rate": 1.0 / max(len(labels), 1),
        "majority_class_rate": max(support.values()) / max(len(y_true), 1),
    }


def feature_importance(model, features, *, top_k: int = 15) -> dict | None:
    """Every importance the model exposes, and the `top_k` largest by name."""
    values = getattr(model, "feature_importances_", None)
    if values is None:
        return None
    pairs = sorted(zip(list(features), [float(v) for v in values]), key=lambda p: -p[1])
    return {
        "all": {name: value for name, value in pairs},
        "top": [{"feature": name, "importance": value} for name, value in pairs[:top_k]],
    }


# --------------------------------------------------------------------------
# saving
# --------------------------------------------------------------------------


def save_run(out_dir, name, *, config, metrics, y_true, y_pred, model=None) -> dict:
    """Write one run into `out_dir/name` and return what was written.

    The model file is `model.keras` for anything with a `save` method and
    `model.joblib` otherwise, so a scikit-learn run and a Keras run leave the same
    five files behind under different extensions.
    """
    run_dir = Path(out_dir) / name
    run_dir.mkdir(parents=True, exist_ok=True)

    (run_dir / "config.json").write_text(json.dumps(config, indent=2, default=str) + "\n")
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, default=str) + "\n")
    np.save(run_dir / "y_true.npy", np.asarray(y_true).astype(str))
    np.save(run_dir / "y_pred.npy", np.asarray(y_pred).astype(str))

    model_file = None
    if model is not None:
        if hasattr(model, "save"):
            model_file = run_dir / "model.keras"
            model.save(model_file)
        else:
            import joblib

            model_file = run_dir / "model.joblib"
            joblib.dump(model, model_file)

    return {
        "name": name,
        "run_dir": str(run_dir),
        "model_file": str(model_file) if model_file else None,
        "config": config,
        "metrics": metrics,
    }


def fit_and_save(
    out_dir,
    name,
    model,
    X_train,
    y_train,
    X_test,
    y_test,
    *,
    features,
    target,
    notes=None,
    extra_config=None,
    top_k: int = 15,
) -> dict:
    """Fit, predict, score, and write the run, in one statement.

    Training and inference time are measured here rather than by the caller, so
    every run in the project records them the same way.
    """
    started = time.perf_counter()
    model.fit(X_train, y_train)
    train_seconds = time.perf_counter() - started

    # Read the parameters the fit actually ran under, before the line below
    # changes one of them.
    params = model.get_params()

    # Predict on one thread. A forest fitted with n_jobs=-1 comes out identical
    # every time, but its prediction does not: the per-tree probabilities are
    # summed into a shared array from several threads, and floating-point
    # addition is not associative, so the totals differ in the last bit and any
    # class the trees split exactly evenly flips. Fitting stays parallel;
    # only the accumulation is serialised.
    if hasattr(model, "n_jobs"):
        model.n_jobs = 1

    started = time.perf_counter()
    y_pred = model.predict(X_test)
    inference_seconds = time.perf_counter() - started

    metrics = classification_metrics(y_test, y_pred)
    metrics["train_seconds"] = round(train_seconds, 3)
    metrics["inference_seconds"] = round(inference_seconds, 3)
    metrics["inference_rows_per_second"] = round(len(y_pred) / max(inference_seconds, 1e-9), 1)

    importance = feature_importance(model, features, top_k=top_k)
    if importance is not None:
        metrics["top_features"] = importance["top"]
        metrics["feature_importances"] = importance["all"]

    config = {
        "run": name,
        "target": target,
        "model": type(model).__name__,
        "params": params,
        "n_features": len(list(features)),
        "features": list(features),
        "n_train": int(len(y_train)),
        "n_test": int(len(y_test)),
        "notes": notes,
    }
    if extra_config:
        config.update(extra_config)

    return save_run(
        out_dir, name, config=config, metrics=metrics, y_true=y_test, y_pred=y_pred, model=model
    )
