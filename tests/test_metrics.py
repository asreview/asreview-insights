from pathlib import Path

from asreview import open_state
from numpy import array_equal
from numpy.testing import assert_almost_equal

from asreviewcontrib.insights.metrics import _recall
from asreviewcontrib.insights.metrics import _time_to_discovery
from asreviewcontrib.insights.metrics import get_metrics
from asreviewcontrib.insights.metrics import recall
from asreviewcontrib.insights.metrics import loss
from asreviewcontrib.insights.algorithms import _loss_value

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
        assert_almost_equal(loss_value, 0.011590940352087164)

def test_loss_value_function():
    # Test case 1: [1, 0] should have a loss of 0
    labels = [1, 0]
    loss_value = _loss_value(labels)
    print(f"Labels: {labels}, Loss: {loss_value}")
    assert_almost_equal(loss_value, 0, decimal=6)

    # Test case 2: [0, 1] should have a loss of 1
    labels = [0, 1]
    loss_value = _loss_value(labels)
    print(f"Labels: {labels}, Loss: {loss_value}")
    assert_almost_equal(loss_value, 1, decimal=6)

    # Test case 3: [1, 1, 0, 0, 0] should have a loss of 0
    labels = [1, 1, 0, 0, 0]
    loss_value = _loss_value(labels)
    print(f"Labels: {labels}, Loss: {loss_value}")
    assert_almost_equal(loss_value, 0, decimal=6)

    # Test case 4: [0, 0, 0, 1, 1] should have a loss of 1
    labels = [0, 0, 0, 1, 1]
    loss_value = _loss_value(labels)
    print(f"Labels: {labels}, Loss: {loss_value}")
    assert_almost_equal(loss_value, 1, decimal=6)

    import random
    for i in range(100):
        length = random.randint(2, 100)
        labels = [random.randint(0, 1) for _ in range(length)]
        loss_value = _loss_value(labels)
        if not (0 <= loss_value <= 1):
            print(f"Test {i+1}: Labels: {labels}, Loss: {loss_value}")
        assert 0 <= loss_value <= 1, f"Loss value {loss_value} not between 0 and 1 for labels {labels}"

    print("All tests passed successfully!")