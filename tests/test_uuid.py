from uuid import UUID

from datalize import serialize, deserialize

import pytest


def test_uuid_types():

    uuid_str = "d3c78de74eba445081002a600b37017e"
    uuid_obj = UUID("d3c78de7-4eba-4450-8100-2a600b37017e")
    assert deserialize(uuid_str, target_type=UUID) == uuid_obj
    assert serialize(uuid_obj) == uuid_str

    with pytest.raises(ValueError):
        deserialize("abc", target_type=UUID)

    with pytest.raises(ValueError):
        deserialize("d3c78de74eba445081002a600b37017x", target_type=UUID)
