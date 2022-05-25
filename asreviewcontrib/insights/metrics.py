import numpy as np

from asreviewcontrib.insights.algorithms import _erf_values
from asreviewcontrib.insights.algorithms import _recall_values
from asreviewcontrib.insights.algorithms import _wss_values
from asreviewcontrib.insights.utils import get_labels


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

    labels = get_labels(state_obj)

    return _recall(labels,
                   intercept,
                   x_absolute=x_absolute,
                   y_absolute=y_absolute)


def _recall(labels, intercept, x_absolute=False, y_absolute=False):

    x, y = _recall_values(labels, x_absolute=x_absolute, y_absolute=y_absolute)

    if intercept < x[0]:
        return 0

    return _slice_metric(x, y, intercept)


def wss(state_obj, intercept, priors=False, x_absolute=False, y_absolute=False):

    labels = get_labels(state_obj)

    return _wss(labels,
                intercept,
                x_absolute=x_absolute,
                y_absolute=y_absolute)


def _wss(labels, intercept, x_absolute=False, y_absolute=False):

    x, y = _wss_values(labels, x_absolute=x_absolute, y_absolute=y_absolute)

    return _slice_metric(x, y, intercept)


def erf(state_obj, intercept, priors=False, x_absolute=False, y_absolute=False):

    labels = get_labels(state_obj)

    return _erf(labels,
                intercept,
                x_absolute=x_absolute,
                y_absolute=y_absolute)


def _erf(labels, intercept, x_absolute=False, y_absolute=False):

    x, y = _erf_values(labels, x_absolute=x_absolute, y_absolute=y_absolute)

    return _slice_metric(x, y, intercept)
