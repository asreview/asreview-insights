
import numpy as np

from asreviewcontrib.insights.algorithms import _recall_values
from asreviewcontrib.insights.algorithms import _wss_values
from asreviewcontrib.insights.algorithms import _erf_values


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


def recall(state_obj, intercept, priors=False, x_relative=True, y_relative=True):

    labels = state_obj.get_labels(priors=priors).to_list()

    return _recall(labels, intercept, x_relative=x_relative, y_relative=y_relative)


def _recall(labels, intercept, x_relative=True, y_relative=True):

    x, y = _recall_values(labels, x_relative=x_relative, y_relative=y_relative)
    print(x, y)

    if intercept < x[0]:
        return 0

    return _slice_metric(x, y, intercept)


def wss(state_obj, intercept, priors=False, x_relative=True, y_relative=True):

    labels = state_obj.get_labels(priors=priors).to_list()

    return _wss(labels, intercept, x_relative=x_relative, y_relative=y_relative)


def _wss(labels, intercept, x_relative=True, y_relative=True):

    x, y = _wss_values(labels, x_relative=x_relative, y_relative=y_relative)

    return _slice_metric(x, y, intercept)


def erf(state_obj, intercept, priors=False, x_relative=True, y_relative=True):

    labels = state_obj.get_labels(priors=priors).to_list()

    return _erf(labels, intercept, x_relative=x_relative, y_relative=y_relative)


def _erf(labels, intercept, x_relative=True, y_relative=True):

    x, y = _erf_values(labels, x_relative=x_relative, y_relative=y_relative)

    return _slice_metric(x, y, intercept)
