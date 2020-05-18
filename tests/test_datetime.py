from datalize import serialize, deserialize
from datetime import datetime, timezone, timedelta


def test_datetime_notz():
    date_str = "2020-05-18T13:37:00.000666"
    date_obj = datetime(2020, 5, 18, 13, 37, 0, 666)
    assert serialize(date_obj) == date_str
    assert deserialize(date_str, target_type=datetime) == date_obj


def test_datetime_tz():
    date_str = "2020-05-18T13:37:00.000666+03:00"
    tzinfo = timezone(timedelta(seconds=10800))
    date_obj = datetime(2020, 5, 18, 13, 37, 0, 666, tzinfo=tzinfo)
    assert serialize(date_obj) == date_str
    assert deserialize(date_str, target_type=datetime) == date_obj
