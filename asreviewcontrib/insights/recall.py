# Copyright 2020 The ASReview Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np

from asreviewcontrib.insights.utils import _fix_start_tick


def plot_recall(ax,
                state_obj,
                priors=False,
                x_relative=False,
                y_relative=True):
    """Plot the recall of state object(s).

    state_obj:
        An ASReview state object.
    """

    labels = state_obj.get_labels(priors=priors).to_list()

    return _plot_recall(ax,
                        labels,
                        x_relative=x_relative,
                        y_relative=y_relative)


def _plot_recall(ax, labels, x_relative=False, y_relative=True):
    """Plot the recall of state object(s).

    labels:
        An ASReview state object.
    """
    n_docs = len(labels)
    n_pos_docs = sum(labels)

    x = np.arange(1, n_docs + 1)
    recall = np.cumsum(labels)

    if x_relative:
        x = x / n_docs

    if y_relative:
        y = recall / n_pos_docs
        y_lim = [-0.05, 1.05]
        yticks = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    else:
        y = recall
        y_lim = [-n_pos_docs * 0.05, n_pos_docs * 1.05]
        yticks = [int(n_pos_docs * r) for r in [0, 0.2, 0.4, 0.6, 0.8, 1.0]]

    ax.step(x, y, where='post')
    ax.set_title("Recall")
    ax.set(xlabel='#', ylabel='Recall')
    ax.set_ylim(y_lim)
    ax.set_yticks(yticks)

    if not x_relative:
        ax.xaxis.get_major_locator().set_params(integer=True)

    # add random line if required
    _plot_random_recall(ax,
                        labels,
                        x_relative=x_relative,
                        y_relative=y_relative)

    # correct x axis if tick is at position 0
    _fix_start_tick(ax)

    return ax


def _plot_random_recall(ax, labels, x_relative, y_relative):
    """Plot the recall of state object(s).

    labels:
        An ASReview state object.
    """
    n_docs = len(labels)
    n_pos_docs = sum(labels)

    # add random line if required
    x = np.arange(1, n_docs + 1)
    recall_random = np.round(np.linspace(0, n_pos_docs, n_docs))

    if x_relative:
        x = x / n_docs

    if y_relative:
        y = recall_random / n_pos_docs
    else:
        y = recall_random

    ax.step(x, y, color="black", where='post')

    return ax
