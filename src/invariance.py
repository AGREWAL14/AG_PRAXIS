"""A two-head model: the sequence classifier, and an adversary that names the session.

The classifier is the one this project already trains, unchanged: the published record
encoder applied to each record of a window, one LSTM across the fifty results, a softmax
over the classes. What is added is a second head reading the same representation through
a gradient reversal, whose job is to name which recording session the window came from.
Because the gradient is reversed on the way back, the trunk is pushed to make that job
harder while the classifier's job stays the same, and the strength of that push is one
number, `lambda`, which is a variable rather than a constant so a sweep does not rebuild
the model.

Two things about the adversary's task decide whether any of this measures what it is
meant to.

It is conditional on the class. Each capture belongs to exactly one class, so class is a
function of capture identity, and an adversary asked to name the capture with no further
information could satisfy itself by naming the class. A representation made independent of
that is a representation made independent of the label, which is not invariance, it is
destruction. So the true class is an input, and the adversary's output is masked to the
captures of that class: the question it answers is which of *this class's* sessions the
window came from, which is the question NB03 asked of the raw features.

It sees only the windows a session question can be put to. Eleven of the nineteen classes
were recorded once, where the capture and the class are the same set of windows and the
question is empty, and some captures are held back to be probed rather than trained on. A
per-window flag gates the adversary: the reversed representation is multiplied by it, so a
window outside the set contributes no gradient through the reversal at all. The flag is
belt and braces with the sample weight the loss should also carry, and it is the half that
is visible in the graph.

Nothing here trains. `build` returns a compiled-ready model; what to compile it with, how
to weight the two losses, and how to sweep lambda are the caller's.
"""

from __future__ import annotations

import time

import numpy as np

# The offset added to a masked logit. Large enough that the softmax gives it no mass,
# small enough not to produce a NaN when it meets a float32 exponential.
MASK_OFFSET = 1e9

CAPTURE_HIDDEN = 128


def _keras():
    import keras

    return keras


def class_capture_membership(classes, captures, class_of_capture) -> np.ndarray:
    """A `(n_classes, n_captures)` matrix, 1 where that capture belongs to that class.

    This is what turns the adversary's question from "which of all the sessions" into
    "which of this class's sessions". Every capture belongs to exactly one class, so
    every column holds exactly one 1, and a class's row sums to how many sessions it has
    for the adversary to tell apart.
    """
    classes, captures = list(classes), list(captures)
    matrix = np.zeros((len(classes), len(captures)), dtype="float32")
    for column, capture in enumerate(captures):
        label = class_of_capture[capture]
        if label not in classes:
            raise ValueError(f"capture {capture} belongs to {label}, which is not in classes")
        matrix[classes.index(label), column] = 1.0
    per_column = matrix.sum(axis=0)
    if not (per_column == 1).all():
        stray = [captures[i] for i in np.flatnonzero(per_column != 1)]
        raise ValueError(f"these captures do not belong to exactly one class: {stray}")
    empty = [classes[i] for i in np.flatnonzero(matrix.sum(axis=1) == 0)]
    if len(empty) == len(classes):
        raise ValueError("no class holds any of these captures")
    return matrix


def chance_rate(membership) -> float:
    """The rate a guesser reaches, averaged over the classes that have captures here.

    A class with one capture in the set contributes 1.0, because there is nothing to tell
    apart; a class with none contributes nothing to the average.

    Counted in double precision. The membership matrix is float32 because it ends up as a
    layer's weights, and a reciprocal taken in float32 puts 1/7 out by about 1e-8, which
    is enough to make this disagree with the same rate counted from the captures
    themselves. The counts are small integers, so widening them first makes the two
    routes to this number agree exactly rather than nearly.
    """
    counts = np.asarray(membership, dtype="float64").sum(axis=1)
    counts = counts[counts > 0]
    return float(np.mean(1.0 / counts))


def _register(cls):
    keras = _keras()
    return keras.saving.register_keras_serializable(package="ag_praxis")(cls)


def gradient_reversal_layer():
    """The reversal, as a layer class.

    Built inside a function because importing keras at module import time would make
    every module that touches this one pay for it.

    Forward it is the identity. Backward it multiplies the gradient by `-lambda`, so the
    trunk moves away from whatever helps the head above it. `lambda` is a non-trainable
    weight rather than a Python float, so a sweep assigns it and the same built model is
    reused, and so its value is saved with the model rather than remembered.
    """
    keras = _keras()
    from keras import layers

    @_register
    class GradientReversal(layers.Layer):
        def __init__(self, lam: float = 1.0, **kwargs):
            super().__init__(**kwargs)
            self.initial_lam = float(lam)

        def build(self, input_shape):
            self.lam = self.add_weight(
                shape=(),
                initializer=keras.initializers.Constant(self.initial_lam),
                trainable=False,
                dtype="float32",
                name="lam",
            )
            super().build(input_shape)

        def call(self, inputs):
            import tensorflow as tf

            lam = self.lam

            @tf.custom_gradient
            def reverse(x):
                def backward(dy):
                    return -lam * dy

                return tf.identity(x), backward

            return reverse(inputs)

        def compute_output_shape(self, input_shape):
            return input_shape

        def get_config(self):
            return {**super().get_config(), "lam": self.initial_lam}

    return GradientReversal


def within_class_softmax_layer():
    """A softmax over only the captures the given class owns.

    Takes the capture logits and the row of the membership matrix the class selects, and
    puts every capture outside that class beyond the reach of the softmax. Without this
    the adversary can answer by naming the class, and a trunk trained against it loses the
    label rather than the session.
    """
    from keras import layers, ops

    @_register
    class WithinClassSoftmax(layers.Layer):
        def call(self, inputs):
            logits, allowed = inputs
            return ops.softmax(logits - (1.0 - allowed) * MASK_OFFSET, axis=-1)

        def compute_output_shape(self, input_shape):
            return input_shape[0]

    return WithinClassSoftmax


def build(
    *,
    encoder,
    n_features: int,
    n_classes: int,
    n_captures: int,
    window: int,
    membership,
    lstm_units: int = 128,
    lam: float = 0.0,
    capture_hidden: int = CAPTURE_HIDDEN,
):
    """The two-head model, ready to compile.

    `encoder` is the published record encoder with its head removed, passed in rather than
    built here so this module cannot drift from the one the rest of the project trains.

    Three inputs. The windows. The true class as a one-hot, which conditions the adversary
    and is not seen by the classifier. And a per-window flag, 1 where the adversary is
    allowed to look, which gates the reversed representation so a window outside the
    adversary's set sends no gradient back through it.

    Two outputs, `attack` over the classes and `capture` over the captures. The trunk
    layers keep the names the rest of the project reads them by, so anything that taps
    `across_the_window` for a representation keeps working.
    """
    keras = _keras()
    from keras import layers

    membership = np.asarray(membership, dtype="float32")
    if membership.shape != (n_classes, n_captures):
        raise ValueError(
            f"membership is {membership.shape}, expected ({n_classes}, {n_captures})"
        )

    GradientReversal = gradient_reversal_layer()
    WithinClassSoftmax = within_class_softmax_layer()

    windows = keras.Input(shape=(int(window), int(n_features), 1), name="windows")
    class_onehot = keras.Input(shape=(int(n_classes),), name="class_onehot")
    in_domain = keras.Input(shape=(1,), name="in_domain")

    # The trunk, layer for layer what the single-head model holds, under the same names.
    per_record = layers.TimeDistributed(encoder, name="per_record")(windows)
    representation = layers.LSTM(int(lstm_units), name="across_the_window")(per_record)

    attack = layers.Dense(int(n_classes), activation="softmax", name="attack")(representation)

    reversed_representation = GradientReversal(lam=float(lam), name="gradient_reversal")(
        representation
    )
    gated = layers.Multiply(name="only_domain_windows")([reversed_representation, in_domain])
    conditioned = layers.Concatenate(name="with_the_class")([gated, class_onehot])
    hidden = layers.Dense(int(capture_hidden), activation="relu", name="capture_hidden")(
        conditioned
    )
    logits = layers.Dense(int(n_captures), name="capture_logits")(hidden)

    # The class picks its own row of the membership matrix: a fixed, untrained projection.
    allowed = layers.Dense(
        int(n_captures), use_bias=False, trainable=False, name="class_to_captures"
    )(class_onehot)
    capture = WithinClassSoftmax(name="capture")([logits, allowed])

    model = keras.Model(
        inputs={"windows": windows, "class_onehot": class_onehot, "in_domain": in_domain},
        outputs={"attack": attack, "capture": capture},
        name="cnn_lstm_two_head",
    )
    model.get_layer("class_to_captures").set_weights([membership])
    return model


def set_lambda(model, value: float) -> float:
    """Assign the reversal strength on a built model, and read it back."""
    layer = model.get_layer("gradient_reversal")
    layer.lam.assign(float(value))
    return float(layer.lam.numpy())


def parameter_split(model) -> dict:
    """How many parameters belong to the trunk and the attack head, and how many the
    adversary adds.

    The first number is what the single-head model has, so a run can say the classifier it
    trains is the same size as the one it is compared against, and the second is the cost
    of the head that is thrown away after training.
    """
    adversary = {"capture_hidden", "capture_logits", "class_to_captures", "gradient_reversal"}
    shared, extra = 0, 0
    for layer in model.layers:
        count = int(sum(int(np.prod(w.shape)) for w in layer.weights))
        if layer.name in adversary:
            extra += count
        else:
            shared += count
    return {
        "trunk_and_attack_head": shared,
        "adversary": extra,
        "total": shared + extra,
    }


def fit_adversarial(
    model,
    *,
    X,
    attack_targets,
    class_onehot,
    in_domain,
    capture_targets,
    epochs: int,
    batch_size: int,
    seed: int,
    rows=None,
    checkpoint_path=None,
    verbose: int = 2,
):
    """The two-head fit, written out because no `model.fit` call expresses it.

    The structure is the one `sequence.fit_group_dro` already uses, for the same reason:
    the objective depends on which capture a window came from, and a Keras loss sees the
    targets and the predictions and nothing else. The batch step is compiled and traced
    once, the optimizer's slot variables are built before that trace so no variable is
    created inside it, and shuffling is seeded per epoch here rather than left to Keras.

    The loss is the attack cross-entropy plus the capture cross-entropy. The second is
    summed over the windows the adversary is allowed to see and divided by how many there
    were, so a batch that happens to hold few of them does not contribute a smaller loss
    per window than one that holds many. Rows outside that set are zeroed by the same flag
    that gates the reversed representation, so they are excluded twice over: no gradient
    reaches the trunk through the adversary, and no loss is counted for them.

    `lambda` is not here. It lives on the reversal layer and is read from the model, so a
    sweep assigns it and calls this again without rebuilding anything.
    """
    import keras
    import tensorflow as tf

    held = len(attack_targets)
    for name, array in (("class_onehot", class_onehot), ("in_domain", in_domain),
                        ("capture_targets", capture_targets), ("X", X)):
        if len(array) != held:
            raise ValueError(f"{name} holds {len(array)} rows against {held} targets")

    # `rows` selects which windows are trained on, as an index rather than a slice of the
    # arrays. Slicing would copy a couple of gigabytes of windows to leave some out, and
    # whether that fits would depend on the runtime rather than on the experiment.
    rows = np.arange(held) if rows is None else np.asarray(rows).astype("int64")
    n = len(rows)
    if n == 0:
        raise ValueError("no rows to train on")

    optimizer = model.optimizer
    if optimizer is None:
        raise ValueError("the model has no optimizer; compile it before fitting")
    optimizer.build(model.trainable_variables)

    @tf.function(reduce_retracing=True)
    def step(windows, classes, domain, attack_true, capture_true, n_domain):
        with tf.GradientTape() as tape:
            out = model(
                {"windows": windows, "class_onehot": classes, "in_domain": domain},
                training=True,
            )
            attack_each = keras.losses.categorical_crossentropy(attack_true, out["attack"])
            capture_each = keras.losses.categorical_crossentropy(capture_true, out["capture"])
            attack_loss = tf.reduce_mean(attack_each)
            # The flag is the sample weight. A batch with no window the adversary may see
            # contributes nothing rather than dividing by zero.
            weighted = tf.reduce_sum(capture_each * tf.squeeze(domain, axis=-1))
            capture_loss = weighted / n_domain
            loss = attack_loss + capture_loss
        optimizer.apply_gradients(
            zip(tape.gradient(loss, model.trainable_variables), model.trainable_variables)
        )
        correct = tf.reduce_sum(
            tf.cast(
                tf.equal(tf.argmax(out["attack"], axis=1), tf.argmax(attack_true, axis=1)),
                tf.float32,
            )
        )
        return attack_loss, capture_loss, correct

    history = {"attack_loss": [], "capture_loss": [], "attack_accuracy": [],
               "domain_windows": [], "seconds": []}
    lam = float(model.get_layer("gradient_reversal").lam.numpy())

    for epoch in range(int(epochs)):
        started = time.perf_counter()
        rng = np.random.default_rng(int(seed) + epoch)
        order = rows[rng.permutation(n)]

        attack_total, capture_total, correct_total = 0.0, 0.0, 0.0
        seen, domain_seen, capture_batches = 0, 0, 0
        for start in range(0, n, int(batch_size)):
            index = order[start : start + int(batch_size)]
            domain_batch = in_domain[index]
            n_domain = float(domain_batch.sum())
            attack_loss, capture_loss, correct = step(
                tf.convert_to_tensor(X[index]),
                tf.convert_to_tensor(class_onehot[index]),
                tf.convert_to_tensor(domain_batch),
                tf.convert_to_tensor(attack_targets[index]),
                tf.convert_to_tensor(capture_targets[index]),
                tf.constant(max(n_domain, 1.0), dtype=tf.float32),
            )
            attack_total += float(attack_loss) * len(index)
            correct_total += float(correct)
            seen += len(index)
            domain_seen += int(n_domain)
            if n_domain > 0:
                capture_total += float(capture_loss)
                capture_batches += 1

        history["attack_loss"].append(attack_total / max(seen, 1))
        history["capture_loss"].append(capture_total / max(capture_batches, 1))
        history["attack_accuracy"].append(correct_total / max(seen, 1))
        history["domain_windows"].append(domain_seen)
        history["seconds"].append(round(time.perf_counter() - started, 2))

        if checkpoint_path is not None:
            model.save(checkpoint_path)
        if verbose:
            print(
                f"  epoch {epoch + 1}/{epochs}  attack loss {history['attack_loss'][-1]:.4f}"
                f"   capture loss {history['capture_loss'][-1]:.4f}"
                f"   attack accuracy {history['attack_accuracy'][-1]:.4f}"
                f"   [{history['seconds'][-1]:,.0f}s, lambda {lam:g}]"
            )

    history["lambda"] = lam
    history["epochs"] = int(epochs)
    history["batch_size"] = int(batch_size)
    history["seed"] = int(seed)
    return history
