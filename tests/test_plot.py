from pathlib import Path

from pytest import mark

import matplotlib.pyplot as plt

from asreview import open_state

from asreviewcontrib.insights.plot import plot_recall
from asreviewcontrib.insights.plot import plot_erf
from asreviewcontrib.insights.plot import plot_wss
from asreviewcontrib.insights.plot import _plot_recall
from asreviewcontrib.insights.plot import _plot_erf
from asreviewcontrib.insights.plot import _plot_wss

TEST_ASREVIEW_FILES = Path("tests", "asreview_files")
TEST_FIGURES = Path("figures")


def setup():

    TEST_FIGURES.mkdir(exist_ok=True)


def test_plot_recall_small_data():

    fig, ax = plt.subplots()
    _plot_recall(ax, [1, 1, 1, 0])

    fig.savefig(Path(TEST_FIGURES, "tests_recall_small_dataset.png"))


def test_plot_recall():

    with open_state(
            Path(TEST_ASREVIEW_FILES,
                 "sim_van_de_schoot_2017_1.asreview")) as s:

        fig, ax = plt.subplots()
        plot_recall(ax, s)

        fig.savefig(
            Path(TEST_FIGURES, "tests_recall_sim_van_de_schoot_2017_1.png"))


def test_plot_wss_small_data():

    fig, ax = plt.subplots()
    _plot_wss(ax, [1, 1, 1, 0])

    fig.savefig(Path(TEST_FIGURES, "tests_wss_small_dataset.png"))


def test_plot_wss():

    with open_state(
            Path(TEST_ASREVIEW_FILES,
                 "sim_van_de_schoot_2017_1.asreview")) as s:
        fig, ax = plt.subplots()
        plot_wss(ax, s)
        fig.savefig(
            Path(TEST_FIGURES,
                 "tests_wss_default_sim_van_de_schoot_2017_1.png"))

        fig, ax = plt.subplots()
        plot_wss(ax, s)
        fig.savefig(
            Path(TEST_FIGURES,
                 "tests_wss_default_sim_van_de_schoot_2017_1.png"))

        fig, ax = plt.subplots()
        plot_wss(ax, s, x_relative=False)
        fig.savefig(
            Path(TEST_FIGURES, "tests_wss_xabs_sim_van_de_schoot_2017_1.png"))

        fig, ax = plt.subplots()
        plot_wss(ax, s, y_relative=False)
        fig.savefig(
            Path(TEST_FIGURES, "tests_wss_yabs_sim_van_de_schoot_2017_1.png"))

        fig, ax = plt.subplots()
        plot_wss(ax, s, x_relative=False, y_relative=False)
        fig.savefig(
            Path(TEST_FIGURES, "tests_wss_xyabs_sim_van_de_schoot_2017_1.png"))


def test_plot_erf():

    with open_state(
            Path(TEST_ASREVIEW_FILES,
                 "sim_van_de_schoot_2017_1.asreview")) as s:
        fig, ax = plt.subplots()
        plot_erf(ax, s)
        fig.savefig(
            Path(TEST_FIGURES,
                 "tests_erf_default_sim_van_de_schoot_2017_1.png"))

        fig, ax = plt.subplots()
        plot_erf(ax, s)
        fig.savefig(
            Path(TEST_FIGURES,
                 "tests_erf_default_sim_van_de_schoot_2017_1.png"))

        fig, ax = plt.subplots()
        plot_erf(ax, s, x_relative=False)
        fig.savefig(
            Path(TEST_FIGURES, "tests_erf_xabs_sim_van_de_schoot_2017_1.png"))

        fig, ax = plt.subplots()
        plot_erf(ax, s, y_relative=False)
        fig.savefig(
            Path(TEST_FIGURES, "tests_erf_yabs_sim_van_de_schoot_2017_1.png"))

        fig, ax = plt.subplots()
        plot_erf(ax, s, x_relative=False, y_relative=False)
        fig.savefig(
            Path(TEST_FIGURES, "tests_erf_xyabs_sim_van_de_schoot_2017_1.png"))
