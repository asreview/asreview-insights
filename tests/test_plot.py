from pathlib import Path

from pytest import mark

import matplotlib.pyplot as plt

from asreview import open_state

from asreviewcontrib.insights import plot_recall, plot_wss, plot_recall_wss
from asreviewcontrib.insights.recall import _plot_recall, _plot_wss, _plot_recall_wss

TEST_ASREVIEW_FILES = Path("tests", "asreview_files")
TEST_FIGURES = Path("figures")


def test_plot_recall_small_data():

    fig, ax = plt.subplots()
    _plot_recall(ax, [1,1,1,0])

    fig.savefig(Path(TEST_FIGURES, "tests_recall_small_dataset.png"))


def test_plot_recall():

    with open_state(Path(TEST_ASREVIEW_FILES, "sim_ptsd_2.asreview")) as s:

        fig, ax = plt.subplots()
        plot_recall(ax, s)

        fig.savefig(Path(TEST_FIGURES, "tests_recall_sim_ptsd_2.png"))


def test_plot_wss_small_data():

    fig, ax = plt.subplots()
    _plot_wss(ax, [1,1,1,0])

    fig.savefig(Path(TEST_FIGURES, "tests_wss_small_dataset.png"))


def test_plot_wss():

    with open_state(Path(TEST_ASREVIEW_FILES, "sim_ptsd_2.asreview")) as s:

        fig, ax = plt.subplots()
        plot_wss(ax, s)

        fig.savefig(Path(TEST_FIGURES, "tests_wss_sim_ptsd_2.png"))


def test_plot_recall_wss_small_data():

    fig, ax = plt.subplots()
    _plot_recall_wss(ax, [1,1,1,0])

    fig.savefig(Path(TEST_FIGURES, "tests_recall_wss_small_dataset.png"))


def test_plot_recall_wss():

    with open_state(Path(TEST_ASREVIEW_FILES, "sim_ptsd_2.asreview")) as s:

        fig, ax = plt.subplots()
        plot_recall_wss(ax, s)

        fig.savefig(Path(TEST_FIGURES, "tests_recall_wss_sim_ptsd_2.png"))
