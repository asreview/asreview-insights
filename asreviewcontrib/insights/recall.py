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

import argparse
import logging

import numpy as np
import matplotlib.pyplot as plt


def _fix_start_tick(ax):

    # correct x axis if tick is at position 0
    locs = ax.get_xticks()
    if locs[1] == 0:
        locs[1] = 1
        ax.set_xticks(locs[1:-1])

    return ax



def plot_wss(ax, state_obj, prior="ignore"):

    """Plot the wss of state object(s).

    state_obj:
        An ASReview state object.
    """

    labels = state_obj.get_labels().to_list()

    return _plot_wss(ax, labels, prior=prior)


def _plot_wss(ax, labels, prior="ignore"):

    """Plot the wss of state object(s).

    labels:
        An ASReview state object.
    """

    x = list(range(1, len(labels)+1))
    recall = np.cumsum(labels)/np.sum(labels)
    recall_random = np.linspace(1/max(x), 1, max(x))
    wss = recall - recall_random

    ax.step(x, wss, where='post')
    ax.set_title("Work Saved over Sampling")
    ax.set(xlabel='#', ylabel='WSS')
    # ax.set_ylim([-0.05, 1.05])
    # ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.xaxis.get_major_locator().set_params(integer=True)

    # correct x axis if tick is at position 0
    _fix_start_tick(ax)

    return ax


def plot_recall(ax, state_obj, prior="ignore"):

    """Plot the recall of state object(s).

    state_obj:
        An ASReview state object.
    """

    labels = state_obj.get_labels().to_list()

    return _plot_recall(ax, labels, prior=prior)


def _plot_recall(ax, labels, prior="ignore"):

    """Plot the recall of state object(s).

    labels:
        An ASReview state object.
    """

    x = list(range(1, len(labels)+1))
    recall = np.cumsum(labels)/np.sum(labels)

    ax.step(x, recall, where='post')
    ax.set_title("Recall")
    ax.set(xlabel='#', ylabel='Recall')
    ax.set_ylim([-0.05, 1.05])
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.xaxis.get_major_locator().set_params(integer=True)

    # add random line if required
    _plot_random_recall(ax, labels, prior=prior)

    # correct x axis if tick is at position 0
    _fix_start_tick(ax)

    return ax

def _plot_random_recall(ax, labels, prior="ignore"):

    """Plot the recall of state object(s).

    labels:
        An ASReview state object.
    """

    # add random line if required
    x = list(range(1, len(labels)+1))
    recall_random = np.linspace(1/max(x), 1, max(x))
    ax.step(x, recall_random, color="black", where='post')

    return ax



def plot_recall_wss(ax, state_obj, prior="ignore"):

    """Plot the wss versus the recall of state object(s).

    state_obj:
        An ASReview state object.
    """

    labels = state_obj.get_labels().to_list()

    return _plot_recall_wss(ax, labels, prior=prior)


def _plot_recall_wss(ax, labels, prior="ignore"):

    """Plot the wss of state object(s).

    labels:
        An ASReview state object.
    """

    x = list(range(1, len(labels)+1))
    recall = np.cumsum(labels)/np.sum(labels)
    recall_random = np.linspace(1/max(x), 1, max(x))
    wss = recall - recall_random

    ax.step(recall, wss, where='post')
    ax.set_title("Recall versus Work Saved over Sampling")
    ax.set(xlabel='Recall', ylabel='WSS')
    ax.set_xlim([-0.05, 1.05])
    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylim([-0.05, 1.05])
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    # ax.xaxis.get_major_locator().set_params(integer=True)

    # correct x axis if tick is at position 0
    # _fix_start_tick(ax)

    return ax
