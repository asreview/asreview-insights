import matplotlib.pyplot as plt
import numpy as np

from asreviewcontrib.insights.utils import _fix_start_tick


def plot_wss(ax, state_obj, priors=False, x_relative=True, y_relative=True):
    """Plot the WSS@T for all thresholds T.

    Arguments
    ---------
    state_obj: asreview.state.SQLiteState
        State object from which to get the labels for the plot.
    priors: bool
        Include the prior in plot or not.
    x_relative: bool
        If False, the number of included records is on the x-axis.
        If True, the fraction of the all included records is on the x-axis.
    y_relative: bool
        If False, the number of records reviewed less is on the y-axis.
        If True, the fraction of all records reviewed less is on the y-axis.

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

    labels = state_obj.get_labels(priors=priors).to_list()

    return _plot_wss(ax, labels, x_relative=x_relative, y_relative=y_relative)


def _plot_wss(ax, labels, x_relative=True, y_relative=True):
    """Plot for each threshold T in [0,1] the WSS@T."""
    n_docs = len(labels)
    n_pos_docs = sum(labels)

    docs_found = np.cumsum(labels)
    docs_found_random = np.round(np.linspace(0, n_pos_docs, n_docs))

    # Get the first occurrence of 1, 2, 3, ..., n_pos_docs in both arrays.
    when_found = np.searchsorted(docs_found, np.arange(1, n_pos_docs + 1))
    when_found_random = np.searchsorted(docs_found_random,
                                        np.arange(1, n_pos_docs + 1))
    n_found_earlier = when_found_random - when_found

    x = np.arange(1, n_pos_docs+1)
    if x_relative:
        x = x / n_pos_docs

    if y_relative:
        y = n_found_earlier / n_docs
        y_lim = [-0.05, 1.05]
        yticks = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    else:
        y = n_found_earlier
        y_lim = [-n_docs * 0.05, n_docs * 1.05]
        yticks = [int(n_docs * r) for r in [0, 0.2, 0.4, 0.6, 0.8, 1.0]]

    ax.step(x, y, where='post')
    ax.set_title("WSS")
    ax.set(xlabel='#', ylabel='WSS')
    ax.set_ylim(y_lim)
    ax.set_yticks(yticks)

    if not x_relative:
        ax.xaxis.get_major_locator().set_params(integer=True)

        # correct x axis if tick is at position 0
        _fix_start_tick(ax)

    return ax
