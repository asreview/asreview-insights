from pathlib import Path

import numpy as np
from asreview import open_state
from numpy import array_equal
from numpy.testing import assert_almost_equal
from numpy.testing import assert_raises

from asreviewcontrib.insights.algorithms import _loss_value
from asreviewcontrib.insights.metrics import _erf
from asreviewcontrib.insights.metrics import _recall
from asreviewcontrib.insights.metrics import _time_to_discovery
from asreviewcontrib.insights.metrics import _wss
from asreviewcontrib.insights.metrics import get_metrics
from asreviewcontrib.insights.metrics import loss
from asreviewcontrib.insights.metrics import recall

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
        Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_stop_if_min.asreview")
    ) as s:
        assert_almost_equal(recall(s, 0.25), 1)


def test_metric_priors():
    with open_state(
        Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_stop_if_min.asreview")
    ) as s:
        r_priors = recall(s, 0.01, priors=True)
        r_no_priors = recall(s, 0.01, priors=False)

        assert not array_equal(r_priors, r_no_priors)


def test_label_padding():
    with open_state(
        Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_stop_if_min.asreview")
    ) as s:
        stop_if_min = get_metrics(s)

    with open_state(
        Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_stop_if_full.asreview")
    ) as s:
        stop_if_full = get_metrics(s)

    assert stop_if_min == stop_if_full

def test_loss():
    with open_state(
        Path(TEST_ASREVIEW_FILES, "sim_van_de_schoot_2017_stop_if_min.asreview")
    ) as s:
        loss_value = loss(s)
        assert_almost_equal(loss_value, 0.011592855205548452)

def test_loss_value_function(seed=None):
    test_cases = [
        ([1, 0], 0),
        ([0, 1], 1),
        ([1, 1, 0, 0, 0], 0),
        ([0, 0, 0, 1, 1], 1),
        ([1, 0, 1], 0.5)
    ]

    for labels, expected_value in test_cases:
        loss_value = _loss_value(labels)
        assert_almost_equal(loss_value, expected_value)

    error_cases = [[0, 0, 0], [0], [1]]
    for labels in error_cases:
        with assert_raises(ValueError):
            _loss_value(labels)

    if seed is not None:
        np.random.seed(seed)

    for _ in range(100):
        length = np.random.randint(2, 100)
        labels = np.random.randint(0, 2, length)
        
        # Ensure labels are not all 0 or all 1
        if np.all(labels == 0) or np.all(labels == 1):
            labels[np.random.randint(0, length)] = 1 - labels[0]
        
        loss_value = _loss_value(labels)
        assert 0 <= loss_value <= 1
    
def test_single_value_formats():
    assert isinstance(_wss([1,1,0,0], 0.5), float)
    assert isinstance(_loss_value([1,1,0,0]), float)
    assert isinstance(_erf([1,1,0,0], 0.5), float)
