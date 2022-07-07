from pathlib import Path

from asreview import open_state
from numpy import array_equal
from numpy.testing import assert_almost_equal

from asreviewcontrib.insights.metrics import _recall
from asreviewcontrib.insights.metrics import recall
from asreviewcontrib.insights.metrics import _time_to_discovery

TEST_ASREVIEW_FILES = Path(Path(__file__).parent, "asreview_files")


def test_metric_recall_small_data():

    labels = [1, 1, 1, 0]
    r = _recall(labels, 0.5)
    assert_almost_equal(r, 0.66666667)

    r = _recall(labels, 2, x_absolute=True)
    assert_almost_equal(r, 0.66666667)

    r = _recall(labels, 2, x_absolute=True, y_absolute=True)
    assert_almost_equal(r, 2)

    r = _recall(labels, 0.5, y_absolute=True)
    assert_almost_equal(r, 2)


def test_metric_recall_max_values():

    labels = [1, 1, 1, 0]
    r = _recall(labels, 1)
    assert_almost_equal(r, 1)

    r = _recall(labels, 4, x_absolute=True)
    assert_almost_equal(r, 1)

    r = _recall(labels, 4, x_absolute=True, y_absolute=True)
    assert_almost_equal(r, 3)

    r = _recall(labels, 1, y_absolute=True)
    assert_almost_equal(r, 3)


def test_metric_recall_min_values():

    labels = [1, 1, 1, 0]
    r = _recall(labels, 0)
    assert_almost_equal(r, 0)

    r = _recall(labels, 0, x_absolute=True)
    assert_almost_equal(r, 0)

    r = _recall(labels, 0, x_absolute=True, y_absolute=True)
    assert_almost_equal(r, 0)

    r = _recall(labels, 0, y_absolute=True)
    assert_almost_equal(r, 0)


def test_metric_recall_invalid_values_min():

    labels = [1, 1, 1, 0]
    r = _recall(labels, -1)
    assert_almost_equal(r, 0)

    r = _recall(labels, 0.2, x_absolute=True)
    assert_almost_equal(r, 0)


def test_metric_recall_invalid_values_max():

    labels = [1, 1, 1, 0]
    r = _recall(labels, 6, x_absolute=True)
    assert_almost_equal(r, 1)

    r = _recall(labels, 1.2)
    assert_almost_equal(r, 1)


def test_time_to_disc():

    labels = [1, 1, 0, 1]
    td = _time_to_discovery([3, 2, 0, 1], labels)

    assert td == [(3, 1), (2, 2), (1, 4)]


def test_metric_recall():

    with open_state(
            Path(TEST_ASREVIEW_FILES,
                 "sim_van_de_schoot_2017_1.asreview")) as s:

        assert_almost_equal(recall(s, 0.25), 1)


def test_metric_priors():

    with open_state(
            Path(TEST_ASREVIEW_FILES,
                 "sim_van_de_schoot_2017_1.asreview")) as s:

        r_priors = recall(s, 0.01, priors=True)
        r_no_priors = recall(s, 0.01, priors=False)

        assert not array_equal(r_priors, r_no_priors)
