from pathlib import Path

from asreview import open_state
import matplotlib.pyplot as plt

from asreviewcontrib.insights.plot import _plot_erf
from asreviewcontrib.insights.plot import _plot_recall
from asreviewcontrib.insights.plot import _plot_wss
from asreviewcontrib.insights.plot import plot_erf
from asreviewcontrib.insights.plot import plot_recall
from asreviewcontrib.insights.plot import plot_wss

TEST_ASREVIEW_FILES = Path("tests", "asreview_files")
TEST_FIGURES = Path("figures")

SMALL_DATA = [1, 0, 1, 1, 0]


def setup():

    TEST_FIGURES.mkdir(exist_ok=True)


def test_plot_erf_small_data():

    fig, ax = plt.subplots()
    _plot_erf(ax, SMALL_DATA)

    fig.savefig(Path(TEST_FIGURES, "tests_small_dataset_erf.png"))


def test_plot_wss_small_data():

    fig, ax = plt.subplots()
    _plot_wss(ax, SMALL_DATA)

    fig.savefig(Path(TEST_FIGURES, "tests_small_dataset_wss.png"))


def test_plot_recall_small_data():

    fig, ax = plt.subplots()
    _plot_recall(ax, SMALL_DATA)

    fig.savefig(Path(TEST_FIGURES, "tests_small_dataset_recall.png"))


def test_plot_recall():

    with open_state(
            Path(TEST_ASREVIEW_FILES,
                 "sim_van_de_schoot_2017_1.asreview")) as s:

        fig, ax = plt.subplots()
        plot_recall(ax, s)

        fig.savefig(
            Path(TEST_FIGURES, "tests_recall_sim_van_de_schoot_2017_1.png"))


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
        plot_wss(ax, s, x_absolute=True)
        fig.savefig(
            Path(TEST_FIGURES, "tests_wss_xabs_sim_van_de_schoot_2017_1.png"))

        fig, ax = plt.subplots()
        plot_wss(ax, s, y_absolute=True)
        fig.savefig(
            Path(TEST_FIGURES, "tests_wss_yabs_sim_van_de_schoot_2017_1.png"))

        fig, ax = plt.subplots()
        plot_wss(ax, s, x_absolute=True, y_absolute=True)
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
        plot_erf(ax, s, x_absolute=True)
        fig.savefig(
            Path(TEST_FIGURES, "tests_erf_xabs_sim_van_de_schoot_2017_1.png"))

        fig, ax = plt.subplots()
        plot_erf(ax, s, y_absolute=True)
        fig.savefig(
            Path(TEST_FIGURES, "tests_erf_yabs_sim_van_de_schoot_2017_1.png"))

        fig, ax = plt.subplots()
        plot_erf(ax, s, x_absolute=True, y_absolute=True)
        fig.savefig(
            Path(TEST_FIGURES, "tests_erf_xyabs_sim_van_de_schoot_2017_1.png"))
