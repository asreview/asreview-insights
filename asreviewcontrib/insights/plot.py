import numpy as np

from asreviewcontrib.insights.algorithms import _erf_values
from asreviewcontrib.insights.algorithms import _recall_values
from asreviewcontrib.insights.algorithms import _wss_values
from asreviewcontrib.insights.utils import get_labels


def _fix_start_tick(ax):

    # correct x axis if tick is at position 0
    locs = ax.get_xticks()
    if locs[1] == 0:
        locs[1] = 1
        ax.set_xticks(locs[1:-1])

    return ax


def plot_recall(ax, state_obj, priors=False, x_absolute=False, y_absolute=False):
    """Plot the recall@T for all thresholds T.

    Arguments
    ---------
    state_obj: asreview.state.SQLiteState
        State object from which to get the labels for the plot.
    priors: bool
        Include the prior in plot or not.
    x_absolute: bool
        If True, the number of records is on the x-axis.
        If False, the fraction of the whole dataset is on the x-axis.
    y_absolute: bool
        If True, the number of included records found is on the y-axis.
        If False, the fraction of all included records found is on the y-axis.

    Returns
    -------
    matplotlib.axes.Axes

    Notes
    -----
    The recall at T statistic is defined as the number of relevant records
    found after reviewing T records.
    """

    labels = get_labels(state_obj)

    return _plot_recall(ax,
                        labels,
                        x_absolute=x_absolute,
                        y_absolute=y_absolute)


def _plot_recall(ax, labels, x_absolute=False, y_absolute=False):
    """Plot the recall of state object(s).

    labels:
        An ASReview state object.
    """

    x, y = _recall_values(labels, x_absolute=x_absolute, y_absolute=y_absolute)

    if y_absolute:
        n_pos_docs = sum(labels)
        y_lim = [-n_pos_docs * 0.05, n_pos_docs * 1.05]
        yticks = [int(n_pos_docs * r) for r in [0, 0.2, 0.4, 0.6, 0.8, 1.0]]
    else:
        y_lim = [-0.05, 1.05]
        yticks = [0, 0.2, 0.4, 0.6, 0.8, 1.0]

    ax.step(x, y, where='post')
    ax.set_title("Recall")
    ax.set(xlabel='#', ylabel='Recall')
    ax.set_ylim(y_lim)
    ax.set_yticks(yticks)

    if x_absolute:
        ax.xaxis.get_major_locator().set_params(integer=True)

    # add random line if required
    _plot_random_recall(ax,
                        labels,
                        x_absolute=x_absolute,
                        y_absolute=y_absolute)

    # correct x axis if tick is at position 0
    _fix_start_tick(ax)

    return ax


def _plot_random_recall(ax, labels, x_absolute, y_absolute):
    """Plot the recall of state object(s).

    labels:
        An ASReview state object.
    """
    n_docs = len(labels)
    n_pos_docs = sum(labels)

    # add random line if required
    x = np.arange(1, n_docs + 1)
    recall_random = np.round(np.linspace(0, n_pos_docs, n_docs))

    if not x_absolute:
        x = x / n_docs

    if y_absolute:
        y = recall_random
    else:
        y = recall_random / n_pos_docs

    ax.step(x, y, color="black", where='post')

    return ax


def plot_wss(ax, state_obj, priors=False, x_absolute=False, y_absolute=False):
    """Plot the WSS@T for all thresholds T.

    Arguments
    ---------
    state_obj: asreview.state.SQLiteState
        State object from which to get the labels for the plot.
    priors: bool
        Include the prior in plot or not.
    x_absolute: bool
        If True, the number of included records is on the x-axis.
        If False, the fraction of the all included records is on the x-axis.
    y_absolute: bool
        If True, the number of records reviewed less is on the y-axis.
        If False, the fraction of all records reviewed less is on the y-axis.

    Returns
    -------
    matplotlib.axes.Axes

    Notes
    -----
    The Work Saved over Sampling at T (WSS@T) statistic is defined as the number
    of records that were reviewed less to find T included records, compared to
    reviewing in random order.

    The number of included records found after reading k papers when reviewing
    in random order is defined as

        round(n_pos * k / n),

    where n_pos is the number of included records in the dataset and n is the
    total number of records in the dataset. Hence the number or records that
    need to be reviewed to find T included papers, when reviewing in random
    order, is defined as the smallest integer k_T, such that

        round(n_pos * k_T / n) = T

    i.e. it is the smallest integer such that

        n_pos * k_T / n > (T - 0.5).

    If the T'th included record in the dataset is found after reviewing r_T
    records, then we have

        WSS@T = r_T - k_T.

    Example
    -------
    [Can we include the stats_explainer picture in the docs?]
    """

    labels = get_labels(state_obj)

    return _plot_wss(ax, labels, x_absolute=x_absolute, y_absolute=y_absolute)


def _plot_wss(ax, labels, x_absolute=False, y_absolute=False):
    """Plot for each threshold T in [0,1] the WSS@T."""
    n_docs = len(labels)

    x, y = _wss_values(labels, x_absolute=x_absolute, y_absolute=y_absolute)

    if y_absolute:
        y_lim = [-n_docs * 0.05, n_docs * 1.05]
        yticks = [int(n_docs * r) for r in [0, 0.2, 0.4, 0.6, 0.8, 1.0]]
    else:
        y_lim = [-0.05, 1.05]
        yticks = [0, 0.2, 0.4, 0.6, 0.8, 1.0]

    ax.step(x, y, where='post')
    ax.set_title("WSS")
    ax.set(xlabel='Recall', ylabel='WSS')
    ax.set_ylim(y_lim)
    ax.set_yticks(yticks)

    if x_absolute:
        ax.xaxis.get_major_locator().set_params(integer=True)

        # correct x axis if tick is at position 0
        _fix_start_tick(ax)

    return ax


def plot_erf(ax, state_obj, priors=False, x_absolute=False, y_absolute=False):
    """Plot the ERF@T for all thresholds T.

    Arguments
    ---------
    state_obj: asreview.state.SQLiteState
        State object from which to get the labels for the plot.
    priors: bool
        Include the prior in plot or not.
    x_absolute: bool
        If True, the number of records is on the x-axis.
        If False, the fraction of the whole dataset is on the x-axis.
    y_absolute: bool
        If True, the number of included records found is on the y-axis.
        If False, the fraction of all included records found is on the y-axis.

    Returns
    -------
    matplotlib.axes.Axes

    Notes
    -----
    The Extra Records Found at T (ERF@T) statistic is defined as the number of
    extra included papers that were found more after reviewing T records,
    compared to reviewing in random order.

    The number of included records found after reading T papers when reviewing
    in random order is defined as

        round(n_pos * T / n),

    where n_pos is the number of included records in the dataset and n is the
    total number of records in the dataset. Hence if n_pos_T is the number of
    positive records found after reviewing T records, then

        ERF@T = n_pos_T - round(n_pos * T / n).

    If y_absolute=False, the ERF will be returned as a fraction of the total
    number of included records, in which case we have

        ERF@T = (n_pos_T - round(n_pos * T / n)) / n_pos.

    Example
    -------
    [Can we include the stats_explainer picture in the docs?]
    """

    labels = get_labels(state_obj)

    return _plot_erf(ax, labels, x_absolute=x_absolute, y_absolute=y_absolute)


def _plot_erf(ax, labels, x_absolute=False, y_absolute=False):
    """Plot for each threshold T the ERF@T."""
    n_pos_docs = sum(labels)

    x, y = _erf_values(labels, x_absolute=x_absolute, y_absolute=y_absolute)

    if y_absolute:
        y_lim = [-n_pos_docs * 0.05, n_pos_docs * 1.05]
        yticks = [int(n_pos_docs * r) for r in [0, 0.2, 0.4, 0.6, 0.8, 1.0]]
    else:
        y_lim = [-0.05, 1.05]
        yticks = [0, 0.2, 0.4, 0.6, 0.8, 1.0]

    ax.step(x, y, where='post')
    ax.set_title("ERF")
    ax.set(xlabel='#', ylabel='ERF')
    ax.set_ylim(y_lim)
    ax.set_yticks(yticks)

    if x_absolute:
        ax.xaxis.get_major_locator().set_params(integer=True)

        # correct x axis if tick is at position 0
        _fix_start_tick(ax)

    return ax
