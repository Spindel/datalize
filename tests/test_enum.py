import enum

import pytest

from datalize import serialize, deserialize


class TrollCount(enum.Enum):
    one = 1
    two = 2
    many = 3


class Alphabet(enum.Enum):
    a = "alpha"
    b = "beta"
    g = "gamma"


def test_string_enums():
    assert serialize(Alphabet.g) == "gamma"
    # Pass by value
    assert deserialize("gamma", target_type=Alphabet) == Alphabet.g
    # pass by name
    assert deserialize("g", target_type=Alphabet) == Alphabet.g


def test_int_enums():
    assert serialize(TrollCount.many) == 3
    # pass by value
    assert deserialize(3, target_type=TrollCount) == TrollCount.many
    # pass by name
    assert deserialize("many", target_type=TrollCount) == TrollCount.many

    # Missing int
    with pytest.raises(ValueError):
        deserialize(5, target_type=TrollCount)

    # Strings-like indices dont work
    with pytest.raises(ValueError):
        deserialize("3", target_type=TrollCount)

    # Missing string
    with pytest.raises(ValueError):
        deserialize("three", target_type=TrollCount)
