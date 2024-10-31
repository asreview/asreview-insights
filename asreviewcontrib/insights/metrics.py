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
from asreviewcontrib.insights.utils import _pad_simulation_labels


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


def recall(state_obj, intercept, priors=False, x_absolute=False, y_absolute=False):
    labels = _pad_simulation_labels(state_obj, priors=priors)

    return _recall(labels, intercept, x_absolute=x_absolute, y_absolute=y_absolute)


def _recall(labels, intercept, x_absolute=False, y_absolute=False):
    x, y = _recall_values(labels, x_absolute=x_absolute, y_absolute=y_absolute)

    if intercept < x[0]:
        return 0

    return _slice_metric(x, y, intercept)


def wss(state_obj, intercept, priors=False, x_absolute=False, y_absolute=False):
    labels = _pad_simulation_labels(state_obj, priors=priors)

    return _wss(labels, intercept, x_absolute=x_absolute, y_absolute=y_absolute)


def _wss(labels, intercept, x_absolute=False, y_absolute=False):
    x, y = _wss_values(labels, x_absolute=x_absolute, y_absolute=y_absolute)

    return _slice_metric(x, y, intercept)


def erf(state_obj, intercept, priors=False, x_absolute=False, y_absolute=False):
    labels = _pad_simulation_labels(state_obj, priors=priors)

    return _erf(labels, intercept, x_absolute=x_absolute, y_absolute=y_absolute)


def _erf(labels, intercept, x_absolute=False, y_absolute=False):
    x, y = _erf_values(labels, x_absolute=x_absolute, y_absolute=y_absolute)

    return _slice_metric(x, y, intercept)


def time_to_discovery(state_obj, priors=False):
    labels = state_obj.get_dataset(["record_id", "label"], priors=priors)

    return _time_to_discovery(labels["record_id"], labels["label"])


def _time_to_discovery(record_ids, labels):
    labels = np.array(labels)
    record_ids = np.array(record_ids)

    v_rel = record_ids[labels == 1]
    i_rel = np.arange(len(labels))[labels == 1] + 1

    return list(zip(v_rel.tolist(), i_rel.tolist()))


def average_time_to_discovery(state_obj, priors=False):
    labels = state_obj.get_dataset(["record_id", "label"], priors=priors)

    td = _time_to_discovery(labels["record_id"], labels["label"])
    return _average_time_to_discovery(td)


def _average_time_to_discovery(td):
    return float(np.mean([v for i, v in td]))


def tp(state_obj, intercept, priors=False, x_absolute=False):
    labels = _pad_simulation_labels(state_obj, priors=priors)

    return _tp(labels, intercept, x_absolute=x_absolute)


def _tp(labels, intercept, x_absolute=False):
    x, y = _tp_values(labels, x_absolute=x_absolute)

    return _slice_metric(x, y, intercept)


def fp(state_obj, intercept, priors=False, x_absolute=False):
    labels = _pad_simulation_labels(state_obj, priors=priors)

    return _fp(labels, intercept, x_absolute=x_absolute)


def _fp(labels, intercept, x_absolute=False):
    x, y = _fp_values(labels, x_absolute=x_absolute)

    return _slice_metric(x, y, intercept)


def tn(state_obj, intercept, priors=False, x_absolute=False):
    labels = _pad_simulation_labels(state_obj, priors=priors)

    return _tn(labels, intercept, x_absolute=x_absolute)


def _tn(labels, intercept, x_absolute=False):
    x, y = _tn_values(labels, x_absolute=x_absolute)

    return _slice_metric(x, y, intercept)


def fn(state_obj, intercept, priors=False, x_absolute=False):
    labels = _pad_simulation_labels(state_obj, priors=priors)

    return _fn(labels, intercept, x_absolute=x_absolute)


def _fn(labels, intercept, x_absolute=False):
    x, y = _fn_values(labels, x_absolute=x_absolute)

    return _slice_metric(x, y, intercept)


def tnr(state_obj, intercept, priors=False, x_absolute=False):
    labels = _pad_simulation_labels(state_obj, priors=priors)

    return _tnr(labels, intercept, x_absolute=x_absolute)


def _tnr(labels, intercept, x_absolute=False):
    n_excludes = labels.count(0)
    x, y = _tn_values(labels, x_absolute=x_absolute)
    y = [v / n_excludes for v in y]
    y = np.round(y, 6)

    if intercept < x[0]:
        return 0

    return _slice_metric(x, y, intercept)

def loss(state_obj, priors=False):
    """Compute the loss for active learning problem.

    Computes the loss for active learning problem where all relevant records
    have to be seen by a human.

    See the inline documentation for detailed description of loss calculation.

    Returns:
        float: The loss value.
    """
    labels = _pad_simulation_labels(state_obj, priors=priors)

    return _loss_value(labels)

def get_metrics(
    state_obj,
    recall=None,
    wss=None,
    erf=None,
    cm=None,
    priors=False,
    x_absolute=False,
    y_absolute=False,
    version=None,
):
    recall = (
        [recall]
        if recall and not isinstance(recall, list)
        else [0.1, 0.25, 0.5, 0.75, 0.9]
    )
    wss = [wss] if wss and not isinstance(wss, list) else [0.95]
    erf = [erf] if erf and not isinstance(erf, list) else [0.10]
    cm = [cm] if cm and not isinstance(cm, list) else [0.1, 0.25, 0.5, 0.75, 0.9]

    labels = _pad_simulation_labels(state_obj, priors=priors)

    td = time_to_discovery(state_obj)

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
                    "value": [(i, v) for i, v in zip(recall, recall_values)],
                },
                {
                    "id": "wss",
                    "title": "Work Saved over Sampling",
                    "value": [(i, v) for i, v in zip(wss, wss_values)],
                },
                {
                    "id": "loss",
                    "title": "Loss",
                    "value": _loss_value(labels),
                },
                {
                    "id": "erf",
                    "title": "Extra Relevant record Found",
                    "value": [(i, v) for i, v in zip(erf, erf_values)],
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
                    "value": [(i, v) for i, v in zip(cm, tp_values)],
                },
                {
                    "id": "fp",
                    "title": "False Positives",
                    "value": [(i, v) for i, v in zip(cm, fp_values)],
                },
                {
                    "id": "tn",
                    "title": "True Negatives",
                    "value": [(i, v) for i, v in zip(cm, tn_values)],
                },
                {
                    "id": "fn",
                    "title": "False Negatives",
                    "value": [(i, v) for i, v in zip(cm, fn_values)],
                },
                {
                    "id": "tnr",
                    "title": "True Negative Rate (Specificity)",
                    "value": [(i, v) for i, v in zip(cm, tnr_values)],
                },
            ]
        },
    }

    return result


def print_metrics(stats):
    print(json.dumps(stats, indent=4))
