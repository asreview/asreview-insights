import numpy as np


def _recall_values(labels, x_absolute=False, y_absolute=False):
    n_docs = len(labels)
    n_pos_docs = sum(labels)

    x = np.arange(1, n_docs + 1)
    recall = np.cumsum(labels)

    if not x_absolute:
        x = x / n_docs

    if y_absolute:
        y = recall
    else:
        y = recall / n_pos_docs

    return x.tolist(), y.tolist()


def _loss_value(labels):
    Ny = sum(labels)
    Nx = len(labels)

    if Ny == 0 or Nx == Ny:
        raise ValueError("Need both 0 and 1 labels")

    # The normalized loss is computed based on:
    #
    # 1. The "optimal" possible AUC, representing the area under an optimal recall
    #    curve, is the total area, Nx * Ny, minus the area above the stepwise
    #    curve, (Ny * (Ny - 1)) / 2. Combined to Ny * (Nx - (Ny - 1)) / 2.
    #
    # 2. The "actual" AUC is the cumulative recall sum, calculated with
    #    np.cumsum(labels).sum().
    #
    # 3. The "worst" AUC, where all positive labels are clustered at the end, is
    #    calculated as (Ny * (Ny + 1)) / 2. To normalize, we need the difference
    #    between the optimal and worst AUCs. We simplify this difference:
    #
    #        (Nx * Ny - ((Ny * (Ny - 1)) / 2)) - ((Ny * (Ny + 1)) / 2)
    #
    #    This simplifies to the hyperbolic paraboloid Ny * (Nx - Ny), which is
    #    the denominator in our normalized loss.
    #
    # Finally, we compute the normalized loss as: 
    # (optimal - actual) / (optimal - worst).
    return float((Ny * (Nx - (Ny - 1) / 2) - np.cumsum(labels).sum()) / (Ny * (Nx - Ny)))  # noqa: E501


def _wss_values(labels, x_absolute=False, y_absolute=False):
    n_docs = len(labels)
    n_pos_docs = sum(labels)

    docs_found = np.cumsum(labels)
    docs_found_random = np.round(np.linspace(0, n_pos_docs, n_docs))

    # Get the first occurrence of 1, 2, 3, ..., n_pos_docs in both arrays.
    when_found = np.searchsorted(docs_found, np.arange(1, n_pos_docs + 1))
    when_found_random = np.searchsorted(docs_found_random, np.arange(1, n_pos_docs + 1))
    n_found_earlier = when_found_random - when_found

    x = np.arange(1, n_pos_docs + 1)
    if not x_absolute:
        x = x / n_pos_docs

    if y_absolute:
        y = n_found_earlier
    else:
        y = n_found_earlier / n_docs

    return x.tolist(), y.tolist()


def _erf_values(labels, x_absolute=False, y_absolute=False):
    n_docs = len(labels)
    n_pos_docs = sum(labels)

    docs_found = np.cumsum(labels)
    docs_found_random = np.round(np.linspace(0, n_pos_docs, n_docs))

    extra_records_found = docs_found - docs_found_random

    x = np.arange(1, n_docs + 1)
    if not x_absolute:
        x = x / n_docs

    if y_absolute:
        y = extra_records_found
    else:
        y = extra_records_found / n_pos_docs

    return x.tolist(), y.tolist()


def _tp_values(labels, x_absolute=False):
    n_pos_docs = sum(labels)
    tp = np.cumsum(labels, dtype=int)

    x = np.arange(1, n_pos_docs + 1)

    if not x_absolute:
        x = x / n_pos_docs

    when_found = np.searchsorted(tp, np.arange(1, n_pos_docs + 1))
    y = tp[when_found]

    return x.tolist(), y.tolist()


def _fp_values(labels, x_absolute=False):
    n_pos_docs = sum(labels)
    n_docs = len(labels)
    tp = np.cumsum(labels, dtype=int)
    x = np.arange(1, n_docs + 1)
    fp = x - tp

    x = np.arange(1, n_pos_docs + 1)

    if not x_absolute:
        x = x / n_pos_docs

    when_found = np.searchsorted(tp, np.arange(1, n_pos_docs + 1))
    y = fp[when_found]

    return x.tolist(), y.tolist()


def _tn_values(labels, x_absolute=False):
    n_pos_docs = sum(labels)
    n_docs = len(labels)
    tp = np.cumsum(labels, dtype=int)
    x = np.arange(1, n_docs + 1)
    n_excludes = labels.count(0)
    fp = x - tp
    tn = n_excludes - fp

    x = np.arange(1, n_pos_docs + 1)

    if not x_absolute:
        x = x / n_pos_docs

    when_found = np.searchsorted(tp, np.arange(1, n_pos_docs + 1))
    y = tn[when_found]

    return x.tolist(), y.tolist()


def _fn_values(labels, x_absolute=False):
    n_pos_docs = sum(labels)
    n_includes = int(sum(labels))
    tp = np.cumsum(labels, dtype=int)
    fn = n_includes - tp

    x = np.arange(1, n_pos_docs + 1)

    if not x_absolute:
        x = x / n_pos_docs

    when_found = np.searchsorted(tp, np.arange(1, n_pos_docs + 1))
    y = fn[when_found]

    return x.tolist(), y.tolist()
