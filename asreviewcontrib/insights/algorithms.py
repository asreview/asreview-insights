import matplotlib.pyplot as plt
import numpy as np


def _recall_values(labels, x_relative=True, y_relative=True):
    n_docs = len(labels)
    n_pos_docs = sum(labels)

    x = np.arange(1, n_docs + 1)
    recall = np.cumsum(labels)

    if x_relative:
        x = x / n_docs

    if y_relative:
        y = recall / n_pos_docs
    else:
        y = recall

    return x, y


def _wss_values(labels, x_relative=True, y_relative=True):
    n_docs = len(labels)
    n_pos_docs = sum(labels)

    docs_found = np.cumsum(labels)
    docs_found_random = np.round(np.linspace(0, n_pos_docs, n_docs))

    # Get the first occurrence of 1, 2, 3, ..., n_pos_docs in both arrays.
    when_found = np.searchsorted(docs_found, np.arange(1, n_pos_docs + 1))
    when_found_random = np.searchsorted(docs_found_random,
                                        np.arange(1, n_pos_docs + 1))
    n_found_earlier = when_found_random - when_found

    x = np.arange(1, n_pos_docs + 1)
    if x_relative:
        x = x / n_pos_docs

    if y_relative:
        y = n_found_earlier / n_docs
    else:
        y = n_found_earlier

    return x, y


def _erf_values(labels, x_relative=True, y_relative=True):

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
    else:
        y = extra_records_found

    return x, y
