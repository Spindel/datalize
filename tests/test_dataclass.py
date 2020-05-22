from dataclasses import dataclass
import pytest

from datalize import serialize, deserialize
from typing import Optional, Union, List


@dataclass
class Simple:
    num: int


def test_simple_dataclass():
    obj = Simple(num=12)
    expected = {"num": 12}
    assert serialize(obj) == expected
    assert deserialize(expected, target_type=Simple) == obj


@dataclass
class Outer:
    name: str
    inner: Simple


def test_nested_dataclass():
    obj = Outer(name="testcase", inner=Simple(2))
    expected = {"name": "testcase", "inner": {"num": 2}}
    assert serialize(obj) == expected
    assert deserialize(expected, target_type=Outer) == obj


@dataclass
class HasOption:
    name: str
    extra: Optional[int]


@dataclass
class HasDefaultOption:
    name: str
    extra: Optional[int] = None


def test_optional_dataclass_novalue():
    obj = HasOption(name="optional_without_value", extra=None)
    expected = {"name": "optional_without_value", "extra": None}
    assert serialize(obj) == expected
    assert deserialize(expected, target_type=HasOption) == obj


def test_optional_dataclass_with_value():
    obj = HasOption(name="optional_with_value", extra=123)
    expected = {"name": "optional_with_value", "extra": 123}
    assert serialize(obj) == expected
    assert deserialize(expected, target_type=HasOption) == obj


def test_optional_dataclass_with_absent_in_json():
    causes_error = {"name": "optional_with_no_extra"}
    # optionals may not be _ABSENT_ unless a default value is provided in the
    # dataclass
    with pytest.raises(TypeError):
        deserialize(causes_error, target_type=HasOption)

    expected = HasDefaultOption(name="optional_with_no_extra", extra=None)
    assert deserialize(causes_error, target_type=HasDefaultOption) == expected


@dataclass
class HasUnion:
    name: str
    val: Union[str, int]


@pytest.mark.filterwarnings("ignore:Unions containing")
def test_union_string_and_int():
    obj = HasUnion(name="union_int", val=123)
    expected = {"name": "union_int", "val": 123}

    assert serialize(obj) == expected
    assert deserialize(expected, target_type=HasUnion) == obj

    obj = HasUnion(name="union_val_is_str", val="123")
    expected = {"name": "union_val_is_str", "val": "123"}
    assert serialize(obj) == expected
    assert deserialize(expected, target_type=HasUnion) == obj


@dataclass
class HasUnionNum:
    name: str
    val: Union[float, int]


def test_union_native_int():
    obj = HasUnionNum(name="union_minor_int", val=123)
    expected = {"name": "union_minor_int", "val": 123}
    assert serialize(obj) == expected
    assert deserialize(expected, target_type=HasUnionNum) == obj


def test_union_native_float():
    obj = HasUnionNum(name="union_minor_float", val=123.12)
    expected = {"name": "union_minor_float", "val": 123.12}
    assert serialize(obj) == expected
    assert deserialize(expected, target_type=HasUnionNum) == obj


@pytest.mark.xfail
def test_union_decode_error_on_stringy_float():
    # Technically this could be considered an error, but I do not care atm.
    # since strings can be turned to floats.....
    unexpected = {"name": "union_strings_turn_floaty", "val": "12.3"}
    with pytest.raises(ValueError):
        deserialize(unexpected, target_type=HasUnionNum)


def test_union_deserialize_error():
    error = {"name": "union_string_error", "val": "abc123"}
    with pytest.raises(ValueError):
        deserialize(error, target_type=HasUnionNum)


@dataclass
class IsNotOptional:
    name: str
    val: Union[float, int, None]


def test_not_optional_unions():
    okay = {"name": "this_should_not_be_optional", "val": None}
    obj = IsNotOptional(name="this_should_not_be_optional", val=None)
    deserialize(okay, target_type=IsNotOptional) == obj


@dataclass
class HasListInt:
    name: str
    val: List[int]


def test_lists_of_thing():
    obj = HasListInt(name="two_ints", val=[1, 2])
    expected = {"name": "two_ints", "val": [1, 2]}
    assert serialize(obj) == expected
    assert deserialize(expected, target_type=HasListInt) == obj
