import matplotlib.pyplot as plt
import numpy as np

from asreviewcontrib.insights.utils import _fix_start_tick


def plot_erf(ax, state_obj, priors=False, x_relative=True, y_relative=True):
    """Plot the ERF@T for all thresholds T.

    Arguments
    ---------
    state_obj: asreview.state.SQLiteState
        State object from which to get the labels for the plot.
    priors: bool
        Include the prior in plot or not.
    x_relative: bool
        If False, the number of records is on the x-axis.
        If True, the fraction of the whole dataset is on the x-axis.
    y_relative: bool
        If False, the number of included records found is on the y-axis.
        If True, the fraction of all included records found is on the y-axis.

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

    If y_relative=True, the ERF will be returned as a fraction of the total
    number of included records, in which case we have

        ERF@T = (n_pos_T - round(n_pos * T / n)) / n_pos.

    Example
    -------
    [Can we include the stats_explainer picture in the docs?]
    """

    labels = state_obj.get_labels(priors=priors).to_list()

    return _plot_erf(ax, labels, x_relative=x_relative, y_relative=y_relative)


def _plot_erf(ax, labels, x_relative=True, y_relative=True):
    """Plot for each threshold T the ERF@T."""
    n_docs = len(labels)
    n_pos_docs = sum(labels)

    docs_found = np.cumsum(labels)
    docs_found_random = np.round(np.linspace(0, n_pos_docs, n_docs))

    extra_records_found = docs_found - docs_found_random

    x = np.arange(1, n_docs + 1)
    if x_relative:
        x = x / n_docs

    if y_relative:
        y = extra_records_found / n_pos_docs
        y_lim = [-0.05, 1.05]
        yticks = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    else:
        y = extra_records_found
        y_lim = [-n_pos_docs * 0.05, n_pos_docs * 1.05]
        yticks = [int(n_pos_docs * r) for r in [0, 0.2, 0.4, 0.6, 0.8, 1.0]]

    ax.step(x, y, where='post')
    ax.set_title("ERF")
    ax.set(xlabel='#', ylabel='ERF')
    ax.set_ylim(y_lim)
    ax.set_yticks(yticks)

    if not x_relative:
        ax.xaxis.get_major_locator().set_params(integer=True)

        # correct x axis if tick is at position 0
        _fix_start_tick(ax)

    return ax
