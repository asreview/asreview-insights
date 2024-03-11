from pathlib import Path

import matplotlib.pyplot as plt
from asreview import open_state

from asreviewcontrib.insights.plot import _plot_erf
from asreviewcontrib.insights.plot import _plot_recall
from asreviewcontrib.insights.plot import _plot_wss
from asreviewcontrib.insights.plot import plot_erf
from asreviewcontrib.insights.plot import plot_recall
from asreviewcontrib.insights.plot import plot_wss
from asreviewcontrib.insights.utils import _iter_states

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
    with open_state(
        Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_stop_if_min.asreview")
    ) as s:
        fig, ax = plt.subplots()
        plot_recall(ax, s)

        fig.savefig(
            Path(TEST_FIGURES, "tests_recall_sim_van_de_schoot_2017_stop_if_min.png")
        )


def test_plot_multiple_recall():
    fps = [
        Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_stop_if_min.asreview"),
        Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_logistic.asreview"),
    ]

    fig, ax = plt.subplots()
    states = _iter_states(fps)
    legend_values = [fp.stem for fp in fps]
    plot_recall(ax, states, legend_values=legend_values)

    fig.savefig(Path(TEST_FIGURES, "tests_multiple_recall_sim_van_de_schoot_2017.png"))


def test_plot_wss():
    with open_state(
        Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_stop_if_min.asreview")
    ) as s:
        fig, ax = plt.subplots()
        plot_wss(ax, s)
        fig.savefig(
            Path(
                TEST_FIGURES, "tests_wss_default_sim_van_de_schoot_2017_stop_if_min.png"
            )
        )

        fig, ax = plt.subplots()
        plot_wss(ax, s)
        fig.savefig(
            Path(
                TEST_FIGURES, "tests_wss_default_sim_van_de_schoot_2017_stop_if_min.png"
            )
        )

        fig, ax = plt.subplots()
        plot_wss(ax, s, x_absolute=True)
        fig.savefig(
            Path(TEST_FIGURES, "tests_wss_xabs_sim_van_de_schoot_2017_stop_if_min.png")
        )

        fig, ax = plt.subplots()
        plot_wss(ax, s, y_absolute=True)
        fig.savefig(
            Path(TEST_FIGURES, "tests_wss_yabs_sim_van_de_schoot_2017_stop_if_min.png")
        )

        fig, ax = plt.subplots()
        plot_wss(ax, s, x_absolute=True, y_absolute=True)
        fig.savefig(
            Path(TEST_FIGURES, "tests_wss_xyabs_sim_van_de_schoot_2017_stop_if_min.png")
        )


def test_plot_multiple_wss():
    fps = [
        Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_stop_if_min.asreview"),
        Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_logistic.asreview"),
    ]

    fig, ax = plt.subplots()
    states = _iter_states(fps)
    legend_values = [fp.stem for fp in fps]
    plot_wss(ax, states, legend_values=legend_values)

    fig.savefig(Path(TEST_FIGURES, "tests_multiple_wss_sim_van_de_schoot_2017.png"))


def test_plot_erf():
    with open_state(
        Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_stop_if_min.asreview")
    ) as s:
        fig, ax = plt.subplots()
        plot_erf(ax, s)
        fig.savefig(
            Path(
                TEST_FIGURES, "tests_erf_default_sim_van_de_schoot_2017_stop_if_min.png"
            )
        )

        fig, ax = plt.subplots()
        plot_erf(ax, s)
        fig.savefig(
            Path(
                TEST_FIGURES, "tests_erf_default_sim_van_de_schoot_2017_stop_if_min.png"
            )
        )

        fig, ax = plt.subplots()
        plot_erf(ax, s, x_absolute=True)
        fig.savefig(
            Path(TEST_FIGURES, "tests_erf_xabs_sim_van_de_schoot_2017_stop_if_min.png")
        )

        fig, ax = plt.subplots()
        plot_erf(ax, s, y_absolute=True)
        fig.savefig(
            Path(TEST_FIGURES, "tests_erf_yabs_sim_van_de_schoot_2017_stop_if_min.png")
        )

        fig, ax = plt.subplots()
        plot_erf(ax, s, x_absolute=True, y_absolute=True)
        fig.savefig(
            Path(TEST_FIGURES, "tests_erf_xyabs_sim_van_de_schoot_2017_stop_if_min.png")
        )


def test_plot_multiple_erf():
    fps = [
        Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_stop_if_min.asreview"),
        Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_logistic.asreview"),
    ]

    fig, ax = plt.subplots()
    states = _iter_states(fps)
    legend_values = [fp.stem for fp in fps]
    plot_erf(ax, states, legend_values=legend_values)

    fig.savefig(Path(TEST_FIGURES, "tests_multiple_erf_sim_van_de_schoot_2017.png"))


def test_plot_with_priors():
    fp = Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_stop_if_min.asreview")

    fig, ax = plt.subplots()
    with open_state(fp) as s:
        plot_recall(ax, s, priors=True)

    fig.savefig(Path(TEST_FIGURES, "tests_priors_recall_sim_van_de_schoot_2017.png"))
