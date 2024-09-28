import numpy as np

from asreviewcontrib.insights.algorithms import _erf_values
from asreviewcontrib.insights.algorithms import _recall_values
from asreviewcontrib.insights.algorithms import _wss_values
from asreviewcontrib.insights.utils import _pad_simulation_labels


def plot_recall(
    ax,
    state_obj,
    priors=False,
    x_absolute=False,
    y_absolute=False,
    show_random=True,
    show_optimal=True,
    show_legend=True,
    legend_values=None,
    legend_kwargs=None,
):
    """Plot the recall@T for all thresholds T.

    Arguments
    ---------
    state_obj: (list of) asreview.state.SQLiteState
        State object from which to get the labels for the plot, or a list of
        state objects.
    priors: bool
        Include the prior in plot or not.
    x_absolute: bool
        If True, the number of records is on the x-axis.
        If False, the fraction of the whole dataset is on the x-axis.
    y_absolute: bool
        If True, the number of included records found is on the y-axis.
        If False, the fraction of all included records found is on the y-axis.
    show_random: bool
        Show the random curve in the plot.
    show_optimal: bool
        Show the optimal recall in the plot.
    show_legend: bool
        If state_obj contains multiple states, show a legend in the plot.
    legend_values: list[str]
        List of values to show in the legend if state_obj contains multiple
        states and show_legend=True.
    legend_kwargs: dict
        Dictionary of keyword arguments that are passed to the legend. See
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html
        for the options.
    Returns
    -------
    matplotlib.axes.Axes

    Notes
    -----
    The recall at T statistic is defined as the number of relevant records
    found after reviewing T records.
    """

    labels = _pad_simulation_labels(state_obj, priors=priors)

    return _plot_recall(
        ax,
        labels,
        x_absolute=x_absolute,
        y_absolute=y_absolute,
        show_random=show_random,
        show_optimal=show_optimal,
        show_legend=show_legend,
        legend_values=legend_values,
        legend_kwargs=legend_kwargs,
    )


def plot_wss(
    ax,
    state_obj,
    priors=False,
    x_absolute=False,
    y_absolute=False,
    show_legend=True,
    legend_values=None,
    legend_kwargs=None,
):
    """Plot the WSS@T for all thresholds T.

    Arguments
    ---------
    state_obj: (list of) asreview.state.SQLiteState
        State object from which to get the labels for the plot, or a list of
        state objects.
    priors: bool
        Include the prior in plot or not.
    x_absolute: bool
        If True, the number of included records is on the x-axis.
        If False, the fraction of the all included records is on the x-axis.
    y_absolute: bool
        If True, the number of records reviewed less is on the y-axis.
        If False, the fraction of all records reviewed less is on the y-axis.
    show_legend: bool
        If state_obj contains multiple states, show a legend in the plot.
    legend_values: list[str]
        List of values to show in the legend if state_obj contains multiple
        states and show_legend=True.
    legend_kwargs: dict
        Dictionary of keyword arguments that are passed to the legend. See
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html
        for the options.

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

    labels = _pad_simulation_labels(state_obj, priors=priors)

    return _plot_wss(
        ax,
        labels,
        x_absolute=x_absolute,
        y_absolute=y_absolute,
        show_legend=show_legend,
        legend_values=legend_values,
        legend_kwargs=legend_kwargs,
    )


def plot_erf(
    ax,
    state_obj,
    priors=False,
    x_absolute=False,
    y_absolute=False,
    show_legend=True,
    legend_values=None,
    legend_kwargs=None,
):
    """Plot the ERF@T for all thresholds T.

    Arguments
    ---------
    state_obj: (list of) asreview.state.SQLiteState
        State object from which to get the labels for the plot, or a list of
        state objects.
    priors: bool
        Include the prior in plot or not.
    x_absolute: bool
        If True, the number of records is on the x-axis.
        If False, the fraction of the whole dataset is on the x-axis.
    y_absolute: bool
        If True, the number of included records found is on the y-axis.
        If False, the fraction of all included records found is on the y-axis.
    show_legend: bool
        If state_obj contains multiple states, show a legend in the plot.
    legend_values: list[str]
        List of values to show in the legend if state_obj contains multiple
        states and show_legend=True.
    legend_kwargs: dict
        Dictionary of keyword arguments that are passed to the legend. See
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html
        for the options.

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

    labels = _pad_simulation_labels(state_obj, priors=priors)

    return _plot_erf(
        ax,
        labels,
        x_absolute=x_absolute,
        y_absolute=y_absolute,
        show_legend=show_legend,
        legend_values=legend_values,
        legend_kwargs=legend_kwargs,
    )


# Plotting using labels.
def _plot_recall(
    ax,
    labels,
    x_absolute=False,
    y_absolute=False,
    show_random=True,
    show_optimal=True,
    show_legend=True,
    legend_values=None,
    legend_kwargs=None,
):
    """Plot the recall.

    labels : list
        List containing labels, or list of lists containing labels.
    """
    if not isinstance(labels[0], list):
        labels = [labels]
        show_legend = False

    if legend_values is None:
        legend_values = [None for _ in labels]

    for i, label_set in enumerate(labels):
        ax = _add_recall_curve(ax, label_set, x_absolute, y_absolute, legend_values[i])
    ax = _add_recall_info(ax, labels, x_absolute, y_absolute)

    if show_random:
        ax = _add_random_curve(ax, labels, x_absolute, y_absolute)

    if show_optimal:
        ax = _add_optimal_recall(ax, labels, x_absolute, y_absolute)

    if show_legend:
        if legend_kwargs is None:
            ax.legend()
        else:
            ax.legend(**legend_kwargs)

    return ax


def _plot_wss(
    ax,
    labels,
    x_absolute=False,
    y_absolute=False,
    show_legend=True,
    legend_values=None,
    legend_kwargs=None,
):
    """Plot for each threshold T in [0,1] the WSS@T.

    labels : list
        List containing labels, or list of lists containing labels.
    """
    if not isinstance(labels[0], list):
        labels = [labels]
        show_legend = False

    if legend_values is None:
        legend_values = [None for _ in labels]

    for i, label_set in enumerate(labels):
        ax = _add_wss_curve(ax, label_set, x_absolute, y_absolute, legend_values[i])
    ax = _add_wss_info(ax, labels, x_absolute, y_absolute)

    if show_legend:
        if legend_kwargs is None:
            ax.legend()
        else:
            ax.legend(**legend_kwargs)

    return ax


def _plot_erf(
    ax,
    labels,
    x_absolute=False,
    y_absolute=False,
    show_legend=True,
    legend_values=None,
    legend_kwargs=None,
):
    """Plot for each threshold T in [0,1] the ERF@T.

    labels : list
        List containing labels, or list of lists containing labels.
    """
    if not isinstance(labels[0], list):
        labels = [labels]
        show_legend = False

    if legend_values is None:
        legend_values = [None for _ in labels]

    for i, label_set in enumerate(labels):
        ax = _add_erf_curve(ax, label_set, x_absolute, y_absolute, legend_values[i])
    ax = _add_erf_info(ax, labels, x_absolute, y_absolute)

    if show_legend:
        if legend_kwargs is None:
            ax.legend()
        else:
            ax.legend(**legend_kwargs)

    return ax


# Adding curves.
def _add_recall_curve(ax, labels, x_absolute, y_absolute, legend_label=None):
    """Add a recall curve to a plot.

    Parameters
    ----------
    ax : plt.axes.Axes
        Axes on which to plot the curve.
    labels : list
        List of labels.
    x_absolute: bool
        If True, the number of records is on the x-axis.
        If False, the fraction of the whole dataset is on the x-axis.
    y_absolute: bool
        If True, the number of included records found is on the y-axis.
        If False, the fraction of all included records found is on the y-axis.
    legend_label : str, optional
        Label to add to the legend for this curve, by default None

    Returns
    -------
    plt.axes.Axes
        Axes with the recall curve added.
    """
    x, y = _recall_values(labels, x_absolute=x_absolute, y_absolute=y_absolute)
    ax.step(x, y, where="post", label=legend_label)
    return ax


def _add_random_curve(ax, labels, x_absolute, y_absolute):
    """Add a random curve to a plot.

    Returns
    -------
    plt.axes.Axes
        Axes with random curve added.
    """
    if isinstance(labels[0], list):
        n_pos_docs = max(sum(label_set) for label_set in labels)
        n_docs = max(len(label_set) for label_set in labels)
    else:
        n_pos_docs = sum(labels)
        n_docs = len(labels)

    # add random line if required
    x = np.arange(1, n_docs + 1)
    recall_random = np.round(np.linspace(0, n_pos_docs, n_docs))

    if not x_absolute:
        x = x / n_docs

    if y_absolute:
        y = recall_random
    else:
        y = recall_random / n_pos_docs

    ax.step(x, y, color="black", where="post")

    return ax


def _add_optimal_recall(ax, labels, x_absolute, y_absolute):
    """Add a optimal recall to a plot using step-wise increments.

    Returns
    -------
    plt.axes.Axes
        Axes with optimal recall added.
    """
    # get total amount of positive labels
    if isinstance(labels[0], list):
        n_pos_docs = max(sum(label_set) for label_set in labels)
        n_docs = max(len(label_set) for label_set in labels)
    else:
        n_pos_docs = sum(labels)
        n_docs = len(labels)

    # Create x and y arrays for step plot
    x = (
        np.arange(0, n_pos_docs + 1)
        if x_absolute
        else np.arange(0, n_pos_docs + 1) / n_docs
    )
    y = (
        np.arange(0, n_pos_docs + 1)
        if y_absolute
        else np.arange(0, n_pos_docs + 1) / n_pos_docs
    )

    # Plot the stepwise optimal recall
    ax.step(x, y, color="grey", where="post")

    return ax


def _add_wss_curve(ax, labels, x_absolute=False, y_absolute=False, legend_label=None):
    x, y = _wss_values(labels, x_absolute=x_absolute, y_absolute=y_absolute)
    ax.step(x, y, where="post", label=legend_label)
    return ax


def _add_erf_curve(ax, labels, x_absolute=False, y_absolute=False, legend_label=None):
    x, y = _erf_values(labels, x_absolute=x_absolute, y_absolute=y_absolute)
    ax.step(x, y, where="post", label=legend_label)
    return ax


# Axes styling and info.
def _add_recall_info(ax, labels, x_absolute=False, y_absolute=False):
    """Add info and set axis for a recall plot.

    Returns
    -------
    plt.axes.Axes
        Axes with title, x-axis and y-axis set for a recall plot.
    """
    if isinstance(labels[0], list):
        n_pos_docs = max(sum(label_set) for label_set in labels)
    else:
        n_pos_docs = sum(labels)

    if y_absolute:
        y_lim = [-n_pos_docs * 0.05, n_pos_docs * 1.05]
        yticks = [int(n_pos_docs * r) for r in [0, 0.2, 0.4, 0.6, 0.8, 1.0]]
    else:
        y_lim = [-0.05, 1.05]
        yticks = [0, 0.2, 0.4, 0.6, 0.8, 1.0]

    if x_absolute:
        xlabel = "Number of labeled records"
    else:
        xlabel = "Proportion of labeled records"

    ax.set_title("Recall")
    ax.set(xlabel=xlabel, ylabel="Recall")
    ax.set_ylim(y_lim)
    ax.set_yticks(yticks)

    if x_absolute:
        ax.xaxis.get_major_locator().set_params(integer=True)

    _fix_start_tick(ax)

    return ax


def _add_wss_info(ax, labels, x_absolute=False, y_absolute=False):
    """Add info and set axis for a WSS plot.

    Returns
    -------
    plt.axes.Axes
        Axes with title, x-axis and y-axis set for a WSS plot.
    """
    if isinstance(labels[0], list):
        n_docs = max(len(label_set) for label_set in labels)
    else:
        n_docs = len(labels)

    if y_absolute:
        y_lim = [-n_docs * 0.05, n_docs * 1.05]
        yticks = [int(n_docs * r) for r in [0, 0.2, 0.4, 0.6, 0.8, 1.0]]
    else:
        y_lim = [-0.05, 1.05]
        yticks = [0, 0.2, 0.4, 0.6, 0.8, 1.0]

    ax.set_title("Work Saved over Sampling (WSS) given Recall")
    ax.set(xlabel="Recall", ylabel="WSS")
    ax.set_ylim(y_lim)
    ax.set_yticks(yticks)

    if x_absolute:
        ax.xaxis.get_major_locator().set_params(integer=True)

        # correct x axis if tick is at position 0
        _fix_start_tick(ax)

    return ax


def _add_erf_info(ax, labels, x_absolute=False, y_absolute=False):
    """Add info and set axis for a ERF plot.

    Returns
    -------
    plt.axes.Axes
        Axes with title, x-axis and y-axis set for a ERF plot.
    """
    if isinstance(labels[0], list):
        n_pos_docs = max(sum(label_set) for label_set in labels)
    else:
        n_pos_docs = sum(labels)

    if y_absolute:
        y_lim = [-n_pos_docs * 0.05, n_pos_docs * 1.05]
        yticks = [int(n_pos_docs * r) for r in [0, 0.2, 0.4, 0.6, 0.8, 1.0]]
    else:
        y_lim = [-0.05, 1.05]
        yticks = [0, 0.2, 0.4, 0.6, 0.8, 1.0]

    if x_absolute:
        xlabel = "Number of labeled records"
    else:
        xlabel = "Proportion of labeled records"

    ax.set_title("Extra Relevant Records Found (ERF)")
    ax.set(xlabel=xlabel, ylabel="ERF")
    ax.set_ylim(y_lim)
    ax.set_yticks(yticks)

    if x_absolute:
        ax.xaxis.get_major_locator().set_params(integer=True)

        # correct x axis if tick is at position 0
        _fix_start_tick(ax)

    return ax


def _fix_start_tick(ax):
    # correct x axis if tick is at position 0
    locs = ax.get_xticks()
    if locs[1] == 0:
        locs[1] = 1
        ax.set_xticks(locs[1:-1])

    return ax
