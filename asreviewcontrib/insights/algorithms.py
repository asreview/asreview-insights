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

    if Ny == 0 or Nx==1:
        raise ValueError("Need both 0 and 1 labels")

    # The best AUC represents the entire area under the perfect curve, which is
    # the total area Nx * Ny, minus the area above the perfect curve. -1 instead
    # of +1 as a result of the stepwise curve.
    best_auc = Nx * Ny - ((Ny * (Ny - 1)) / 2)

    # The actual AUC is the sum of the recall curve.
    actual_auc = np.cumsum(labels).sum()

    # The worst AUC represents the area under the worst-case step curve, which
    # is the area under the recall curve where all positive labels are clumped
    # at the end. (Ny * (Ny + 1)) / 2. This is simplified together with the best
    # auc in the normalized loss.

    # The normalized loss is the difference between the best AUC and the actual
    # AUC, normalized by the range between the best and worst AUCs.
    normalized_loss = (best_auc - actual_auc) / (Ny * (Nx - Ny))

    return (Ny * (Nx - (Ny - 1) / 2) - np.cumsum(labels).sum()) / (Ny * (Nx - Ny))


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
