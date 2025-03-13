from pathlib import Path

import matplotlib.pyplot as plt

from asreviewcontrib.insights.plot import _plot_erf
from asreviewcontrib.insights.plot import _plot_recall
from asreviewcontrib.insights.plot import _plot_wss
from asreviewcontrib.insights.plot import plot_erf
from asreviewcontrib.insights.plot import plot_recall
from asreviewcontrib.insights.plot import plot_wss

TEST_ASREVIEW_FILES = Path(Path(__file__).parent, "asreview_files")
TEST_FIGURES = Path("figures")

SMALL_DATA = [1, 0, 1, 1, 0]


def setup_module():
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
    fp = Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_stop_if_min.asreview")
    fig, ax = plt.subplots()
    plot_recall(ax, fp)
    fig.savefig(
        Path(TEST_FIGURES, "tests_recall_sim_van_de_schoot_2017_stop_if_min.png")
    )


def test_plot_multiple_recall():
    fps = [
        Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_stop_if_min.asreview"),
        Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_logistic.asreview"),
    ]
    fig, ax = plt.subplots()
    plot_recall(ax, fps)
    fig.savefig(Path(TEST_FIGURES, "tests_multiple_recall_sim_van_de_schoot_2017.png"))


def test_plot_wss():
    fp = Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_stop_if_min.asreview")
    fig, ax = plt.subplots()
    plot_wss(ax, fp)
    fig.savefig(
        Path(TEST_FIGURES, "tests_wss_default_sim_van_de_schoot_2017_stop_if_min.png")
    )

    fig, ax = plt.subplots()
    plot_wss(ax, fp)
    fig.savefig(
        Path(TEST_FIGURES, "tests_wss_default_sim_van_de_schoot_2017_stop_if_min.png")
    )

    fig, ax = plt.subplots()
    plot_wss(ax, fp, x_absolute=True)
    fig.savefig(
        Path(TEST_FIGURES, "tests_wss_xabs_sim_van_de_schoot_2017_stop_if_min.png")
    )

    fig, ax = plt.subplots()
    plot_wss(ax, fp, y_absolute=True)
    fig.savefig(
        Path(TEST_FIGURES, "tests_wss_yabs_sim_van_de_schoot_2017_stop_if_min.png")
    )

    fig, ax = plt.subplots()
    plot_wss(ax, fp, x_absolute=True, y_absolute=True)
    fig.savefig(
        Path(TEST_FIGURES, "tests_wss_xyabs_sim_van_de_schoot_2017_stop_if_min.png")
    )


def test_plot_multiple_wss():
    fps = [
        Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_stop_if_min.asreview"),
        Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_logistic.asreview"),
    ]

    fig, ax = plt.subplots()
    plot_wss(ax, fps)

    fig.savefig(Path(TEST_FIGURES, "tests_multiple_wss_sim_van_de_schoot_2017.png"))


def test_plot_erf():
    fp = Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_stop_if_min.asreview")
    fig, ax = plt.subplots()
    plot_erf(ax, fp)
    fig.savefig(
        Path(TEST_FIGURES, "tests_erf_default_sim_van_de_schoot_2017_stop_if_min.png")
    )

    fig, ax = plt.subplots()
    plot_erf(ax, fp)
    fig.savefig(
        Path(TEST_FIGURES, "tests_erf_default_sim_van_de_schoot_2017_stop_if_min.png")
    )

    fig, ax = plt.subplots()
    plot_erf(ax, fp, x_absolute=True)
    fig.savefig(
        Path(TEST_FIGURES, "tests_erf_xabs_sim_van_de_schoot_2017_stop_if_min.png")
    )

    fig, ax = plt.subplots()
    plot_erf(ax, fp, y_absolute=True)
    fig.savefig(
        Path(TEST_FIGURES, "tests_erf_yabs_sim_van_de_schoot_2017_stop_if_min.png")
    )

    fig, ax = plt.subplots()
    plot_erf(ax, fp, x_absolute=True, y_absolute=True)
    fig.savefig(
        Path(TEST_FIGURES, "tests_erf_xyabs_sim_van_de_schoot_2017_stop_if_min.png")
    )


def test_plot_multiple_erf():
    fps = [
        Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_stop_if_min.asreview"),
        Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_logistic.asreview"),
    ]

    fig, ax = plt.subplots()
    plot_erf(ax, fps)

    fig.savefig(Path(TEST_FIGURES, "tests_multiple_erf_sim_van_de_schoot_2017.png"))


def test_plot_with_priors():
    fp = Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_stop_if_min.asreview")

    fig, ax = plt.subplots()
    plot_recall(ax, fp, priors=True)

    fig.savefig(Path(TEST_FIGURES, "tests_priors_recall_sim_van_de_schoot_2017.png"))
