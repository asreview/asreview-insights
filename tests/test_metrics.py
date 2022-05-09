from pathlib import Path

from pytest import mark

from asreview import open_state

from numpy.testing import assert_almost_equal

from asreviewcontrib.insights.metrics import recall, _recall


TEST_ASREVIEW_FILES = Path("tests", "asreview_files")
TEST_FIGURES = Path("figures")


def setup():

    TEST_FIGURES.mkdir(exist_ok=True)


def test_metric_recall_small_data():

    labels = [1, 1, 1, 0]
    r = _recall(labels, 0.5)
    assert_almost_equal(r, 0.66666667)

    r = _recall(labels, 2, x_relative=False)
    assert_almost_equal(r, 0.66666667)

    r = _recall(labels, 2, x_relative=False, y_relative=False)
    assert_almost_equal(r, 2)

    r = _recall(labels, 0.5, y_relative=False)
    assert_almost_equal(r, 2)


def test_metric_recall_max_values():

    labels = [1, 1, 1, 0]
    r = _recall(labels, 1)
    assert_almost_equal(r, 1)

    r = _recall(labels, 4, x_relative=False)
    assert_almost_equal(r, 1)

    r = _recall(labels, 4, x_relative=False, y_relative=False)
    assert_almost_equal(r, 3)

    r = _recall(labels, 1, y_relative=False)
    assert_almost_equal(r, 3)


def test_metric_recall_min_values():

    labels = [1, 1, 1, 0]
    r = _recall(labels, 0)
    assert_almost_equal(r, 0)

    r = _recall(labels, 0, x_relative=False)
    assert_almost_equal(r, 0)

    r = _recall(labels, 0, x_relative=False, y_relative=False)
    assert_almost_equal(r, 0)

    r = _recall(labels, 0, y_relative=False)
    assert_almost_equal(r, 0)


def test_metric_recall():

    with open_state(
            Path(TEST_ASREVIEW_FILES,
                 "sim_van_de_schoot_2017_1.asreview")) as s:

        assert_almost_equal(recall(s, 0.25), 1)
