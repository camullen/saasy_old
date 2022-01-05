from pandas.core.indexes import interval
from preprocess.interval import ArrInterval
from pandas import Timestamp


def test_equality():
    interval_a = ArrInterval(Timestamp("1/1/2021", tz="UTC"), Timestamp("12/31/2021", tz="UTC"), 100)
    interval_b = ArrInterval(Timestamp("1/1/2021", tz="UTC"), Timestamp("12/31/2021", tz="UTC"), 100)
    assert interval_a == interval_b


def test_empty_interval_equality():
    interval_a = ArrInterval.empty_interval()
    interval_b = ArrInterval.empty_interval()
    assert interval_a == interval_b


def test_empty_interval_identity():
    interval_a = ArrInterval.empty_interval()
    interval_b = ArrInterval.empty_interval()
    assert interval_a is not interval_b
