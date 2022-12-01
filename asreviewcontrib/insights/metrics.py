import json

import asreview
import numpy as np

from asreviewcontrib.insights.algorithms import _erf_values
from asreviewcontrib.insights.algorithms import _recall_values
from asreviewcontrib.insights.algorithms import _wss_values
from asreviewcontrib.insights.utils import pad_simulation_labels


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

    i = np.searchsorted(x, intercept, side='right')
    return y[i - 1]


def recall(state_obj,
           intercept,
           priors=False,
           x_absolute=False,
           y_absolute=False):

    labels = pad_simulation_labels(state_obj, priors=priors)

    return _recall(labels,
                   intercept,
                   x_absolute=x_absolute,
                   y_absolute=y_absolute)


def _recall(labels, intercept, x_absolute=False, y_absolute=False):

    x, y = _recall_values(labels, x_absolute=x_absolute, y_absolute=y_absolute)

    if intercept < x[0]:
        return 0

    return _slice_metric(x, y, intercept)


def wss(state_obj,
        intercept,
        priors=False,
        x_absolute=False,
        y_absolute=False):

    labels = pad_simulation_labels(state_obj, priors=priors)

    return _wss(labels,
                intercept,
                x_absolute=x_absolute,
                y_absolute=y_absolute)


def _wss(labels, intercept, x_absolute=False, y_absolute=False):

    x, y = _wss_values(labels, x_absolute=x_absolute, y_absolute=y_absolute)

    return _slice_metric(x, y, intercept)


def erf(state_obj,
        intercept,
        priors=False,
        x_absolute=False,
        y_absolute=False):

    labels = pad_simulation_labels(state_obj, priors=priors)

    return _erf(labels,
                intercept,
                x_absolute=x_absolute,
                y_absolute=y_absolute)


def _erf(labels, intercept, x_absolute=False, y_absolute=False):

    x, y = _erf_values(labels, x_absolute=x_absolute, y_absolute=y_absolute)

    return _slice_metric(x, y, intercept)


def time_to_discovery(state_obj,
                      priors=False):

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


def get_metrics(state_obj,
                recall=[0.1, 0.25, 0.5, 0.75, 0.9],
                wss=[0.95],
                erf=[0.10],
                priors=False,
                x_absolute=False,
                y_absolute=False,
                version=None):

    recall = [recall] if not isinstance(recall, list) else recall
    wss = [wss] if not isinstance(wss, list) else wss
    erf = [erf] if not isinstance(erf, list) else erf

    labels = pad_simulation_labels(state_obj, priors=priors)

    td = time_to_discovery(state_obj)

    recall_values = [
        _recall(labels, v, x_absolute=x_absolute, y_absolute=y_absolute)
        for v in recall
    ]
    wss_values = [
        _wss(labels, v, x_absolute=x_absolute, y_absolute=y_absolute)
        for v in wss
    ]
    erf_values = [
        _erf(labels, v, x_absolute=x_absolute, y_absolute=y_absolute)
        for v in erf
    ]

    # based on https://google.github.io/styleguide/jsoncstyleguide.xml
    result = {
        "asreviewVersion": asreview.__version__,
        "apiVersion": version,
        "data": {
            "items": [{
                "id": "recall",
                "title": "Recall",
                "value": [(i, v) for i, v in zip(recall, recall_values)]
            }, {
                "id": "wss",
                "title": "Work Saved over Sampling",
                "value": [(i, v) for i, v in zip(wss, wss_values)]
            }, {
                "id": "erf",
                "title": "Extra Relevant record Found",
                "value": [(i, v) for i, v in zip(erf, erf_values)]
            }, {
                "id": "atd",
                "title": "Average time to discovery",
                "value": _average_time_to_discovery(td)
            }, {
                "id": "td",
                "title": "Time to discovery",
                "value": td
            }]
        }
    }

    return result


def print_metrics(stats):

    print(json.dumps(stats, indent=4))
