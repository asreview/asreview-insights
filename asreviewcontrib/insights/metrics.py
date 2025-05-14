import json

import asreview
import numpy as np

from asreviewcontrib.insights.algorithms import _erf_values
from asreviewcontrib.insights.algorithms import _fn_values
from asreviewcontrib.insights.algorithms import _fp_values
from asreviewcontrib.insights.algorithms import _loss_value
from asreviewcontrib.insights.algorithms import _recall_values
from asreviewcontrib.insights.algorithms import _tn_values
from asreviewcontrib.insights.algorithms import _tp_values
from asreviewcontrib.insights.algorithms import _wss_values
from asreviewcontrib.insights.utils import get_simulation_labels


def _slice_metric(x, y, intercept):
    """Find the first value after the intercept.

    intercept[i-1] <= v < intercept[i]

    Arguments
    ---------
    x: numpy.array or list
        The values of the x-axis.
    y: numpy.array or list
        The values of the y-axis.
    intercept: float
        The value of the x-axis to map to the y-axis. If value
        is not present, the first value greater than the intercept
        is used.

    Returns
    -------
    float
    """

    i = np.searchsorted(x, intercept, side="right")
    return y[i - 1]


def recall(asreview_file, intercept, priors=False, x_absolute=False, y_absolute=False):
    labels = get_simulation_labels(asreview_file=asreview_file, priors=priors)

    return _recall(labels, intercept, x_absolute=x_absolute, y_absolute=y_absolute)


def _recall(labels, intercept, x_absolute=False, y_absolute=False):
    x, y = _recall_values(labels, x_absolute=x_absolute, y_absolute=y_absolute)

    if intercept < x[0]:
        return 0

    return _slice_metric(x, y, intercept)


def wss(asreview_file, intercept, priors=False, x_absolute=False, y_absolute=False):
    labels = get_simulation_labels(asreview_file=asreview_file, priors=priors)

    return _wss(labels, intercept, x_absolute=x_absolute, y_absolute=y_absolute)


def _wss(labels, intercept, x_absolute=False, y_absolute=False):
    x, y = _wss_values(labels, x_absolute=x_absolute, y_absolute=y_absolute)

    return _slice_metric(x, y, intercept)


def erf(asreview_file, intercept, priors=False, x_absolute=False, y_absolute=False):
    labels = get_simulation_labels(asreview_file=asreview_file, priors=priors)

    return _erf(labels, intercept, x_absolute=x_absolute, y_absolute=y_absolute)


def _erf(labels, intercept, x_absolute=False, y_absolute=False):
    x, y = _erf_values(labels, x_absolute=x_absolute, y_absolute=y_absolute)

    return _slice_metric(x, y, intercept)


def time_to_discovery(asreview_file, priors=False):
    with asreview.open_state(asreview_file) as state_obj:
        data = state_obj.get_results_table(
            columns=["record_id", "label"], priors=priors
        )

    return _time_to_discovery(data["record_id"], data["label"])


def _time_to_discovery(record_ids, labels):
    labels = np.array(labels)
    record_ids = np.array(record_ids)

    v_rel = record_ids[labels == 1]
    i_rel = np.arange(len(labels))[labels == 1] + 1

    return list(zip(v_rel.tolist(), i_rel.tolist(), strict=True))


def average_time_to_discovery(asreview_file, priors=False):
    with asreview.open_state(asreview_file) as state_obj:
        data = state_obj.get_dataset(["record_id", "label"], priors=priors)

    td = _time_to_discovery(data["record_id"], data["label"])
    return _average_time_to_discovery(td)


def _average_time_to_discovery(td):
    return float(np.mean([v for i, v in td]))


def tp(asreview_file, intercept, priors=False, x_absolute=False):
    labels = get_simulation_labels(asreview_file=asreview_file, priors=priors)

    return _tp(labels, intercept, x_absolute=x_absolute)


def _tp(labels, intercept, x_absolute=False):
    x, y = _tp_values(labels, x_absolute=x_absolute)

    return _slice_metric(x, y, intercept)


def fp(asreview_file, intercept, priors=False, x_absolute=False):
    labels = get_simulation_labels(asreview_file=asreview_file, priors=priors)

    return _fp(labels, intercept, x_absolute=x_absolute)


def _fp(labels, intercept, x_absolute=False):
    x, y = _fp_values(labels, x_absolute=x_absolute)

    return _slice_metric(x, y, intercept)


def tn(asreview_file, intercept, priors=False, x_absolute=False):
    labels = get_simulation_labels(asreview_file=asreview_file, priors=priors)

    return _tn(labels, intercept, x_absolute=x_absolute)


def _tn(labels, intercept, x_absolute=False):
    x, y = _tn_values(labels, x_absolute=x_absolute)

    return _slice_metric(x, y, intercept)


def fn(asreview_file, intercept, priors=False, x_absolute=False):
    labels = get_simulation_labels(asreview_file=asreview_file, priors=priors)

    return _fn(labels, intercept, x_absolute=x_absolute)


def _fn(labels, intercept, x_absolute=False):
    x, y = _fn_values(labels, x_absolute=x_absolute)

    return _slice_metric(x, y, intercept)


def tnr(asreview_file, intercept, priors=False, x_absolute=False):
    labels = get_simulation_labels(asreview_file=asreview_file, priors=priors)

    return _tnr(labels, intercept, x_absolute=x_absolute)


def _tnr(labels, intercept, x_absolute=False):
    n_excludes = labels.count(0)
    x, y = _tn_values(labels, x_absolute=x_absolute)
    y = [v / n_excludes for v in y]
    y = np.round(y, 6)

    if intercept < x[0]:
        return 0

    return _slice_metric(x, y, intercept)


def loss(asreview_file, priors=False):
    """Compute the loss for active learning problem.

    Computes the loss for active learning problem where all relevant records
    have to be seen by a human.

    See the inline documentation for detailed description of loss calculation.

    Returns:
        float: The loss value.
    """
    labels = get_simulation_labels(asreview_file=asreview_file, priors=priors)

    return _loss_value(labels)


def get_metrics(
    asreview_file,
    recall=None,
    wss=None,
    erf=None,
    cm=None,
    priors=False,
    x_absolute=False,
    y_absolute=False,
    version=None,
):
    def ensure_list_of_floats(value, default):
        if value is None:
            return default
        if isinstance(value, float):
            return [value]
        if isinstance(value, list) and all(isinstance(i, float) for i in value):
            return value
        raise ValueError(
            f"Invalid input: {value}. Must be a float or a list of floats."
        )

    recall = ensure_list_of_floats(recall, [0.1, 0.25, 0.5, 0.75, 0.9])
    wss = ensure_list_of_floats(wss, [0.95])
    erf = ensure_list_of_floats(erf, [0.10])
    cm = ensure_list_of_floats(cm, [0.1, 0.25, 0.5, 0.75, 0.9])

    labels = get_simulation_labels(asreview_file, priors=priors)

    td = time_to_discovery(asreview_file)

    recall_values = [
        _recall(labels, v, x_absolute=x_absolute, y_absolute=y_absolute) for v in recall
    ]
    wss_values = [
        _wss(labels, v, x_absolute=x_absolute, y_absolute=y_absolute) for v in wss
    ]
    erf_values = [
        _erf(labels, v, x_absolute=x_absolute, y_absolute=y_absolute) for v in erf
    ]
    tp_values = [_tp(labels, v, x_absolute=False) for v in cm]
    fp_values = [_fp(labels, v, x_absolute=False) for v in cm]
    tn_values = [_tn(labels, v, x_absolute=False) for v in cm]
    fn_values = [_fn(labels, v, x_absolute=False) for v in cm]
    tnr_values = [_tnr(labels, v, x_absolute=x_absolute) for v in cm]

    # based on https://google.github.io/styleguide/jsoncstyleguide.xml
    result = {
        "asreviewVersion": asreview.__version__,
        "apiVersion": version,
        "data": {
            "items": [
                {
                    "id": "recall",
                    "title": "Recall",
                    "value": [
                        (i, v) for i, v in zip(recall, recall_values, strict=True)
                    ],
                },
                {
                    "id": "wss",
                    "title": "Work Saved over Sampling",
                    "value": [(i, v) for i, v in zip(wss, wss_values, strict=True)],
                },
                {
                    "id": "loss",
                    "title": "Loss",
                    "value": _loss_value(labels),
                },
                {
                    "id": "erf",
                    "title": "Extra Relevant record Found",
                    "value": [(i, v) for i, v in zip(erf, erf_values, strict=True)],
                },
                {
                    "id": "atd",
                    "title": "Average Time to Discovery",
                    "value": _average_time_to_discovery(td),
                },
                {"id": "td", "title": "Time to discovery", "value": td},
                {
                    "id": "tp",
                    "title": "True Positives",
                    "value": [(i, v) for i, v in zip(cm, tp_values, strict=True)],
                },
                {
                    "id": "fp",
                    "title": "False Positives",
                    "value": [(i, v) for i, v in zip(cm, fp_values, strict=True)],
                },
                {
                    "id": "tn",
                    "title": "True Negatives",
                    "value": [(i, v) for i, v in zip(cm, tn_values, strict=True)],
                },
                {
                    "id": "fn",
                    "title": "False Negatives",
                    "value": [(i, v) for i, v in zip(cm, fn_values, strict=True)],
                },
                {
                    "id": "tnr",
                    "title": "True Negative Rate (Specificity)",
                    "value": [(i, v) for i, v in zip(cm, tnr_values, strict=True)],
                },
            ]
        },
    }

    return result


def print_metrics(stats):
    print(json.dumps(stats, indent=4))
