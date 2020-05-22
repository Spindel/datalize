"""Helper functions to serialize and deserialize dataclasses.

"""

import warnings

from enum import Enum
from uuid import UUID
from datetime import datetime

from dataclasses import is_dataclass, fields, asdict
from typing import Any, Type, Union, Sequence


def get_union_types(type_obj: Type) -> Sequence[Type]:
    """Return the possible union types of the object"""
    return type_obj.__args__


def is_union_type(type_obj: Type) -> bool:
    """Return wether a type is an instance of a typing.Union[....]"""
    return Union == getattr(type_obj, "__origin__", None)


def is_list_type(type_obj: Type) -> bool:
    """Return wether a type is an instance of a typing.List[...]."""
    return getattr(type_obj, "__origin__", None) == list


def list_type_argument(list_type_obj: Type) -> Type:
    """Return type argument X from a typing.List[X]."""
    return list_type_obj.__args__[0]


def deserialize(json: Any, *, target_type: Type) -> Any:
    """Convert data structures loaded from JSON to a specified type."""
    if is_dataclass(target_type):
        # Instantiate a dataclass with its properties deserialized
        # according to their type annotations
        field_types = {f.name: f.type for f in fields(target_type)}
        kwargs = {
            key: deserialize(json[key], target_type=field_types[key])
            for key in json
        }
        return target_type(**kwargs)

    if is_list_type(target_type):
        # Create lists with each item deserialized
        return [
            deserialize(i, target_type=list_type_argument(target_type))
            for i in json
        ]

    if is_union_type(target_type):
        return _deserialize_union(json, target_type=target_type)

    if issubclass(target_type, Enum):
        return _deserialize_enum(json=json, target_type=target_type)

    # Datetimes are encoded as isoformat strings
    if issubclass(target_type, datetime):
        return datetime.fromisoformat(json)

    # Handle target types like str and uuid.UUID
    return target_type(json)


def _deserialize_enum(json: Any, *, target_type: Type) -> Any:
    """Try to deal with Enum data types"""
    assert issubclass(target_type, Enum)

    # If the in-data is an int/float/bool, they were passed as values
    if isinstance(json, (int, float, bool)):
        return target_type(json)

    # Otherwise, assume they were passed as values
    try:
        return target_type(json)
    except ValueError as ex_inner:
        # If not pass-by-value, maybe it was pass-by-name?
        if not hasattr(target_type, json):
            err_msg = f"Unable to convert {json} to {target_type}"
            raise ValueError(err_msg) from ex_inner
        return getattr(target_type, json)


STR_UNION_WARN = "Unions containing 'str' Types will not deserialize properly."


def _deserialize_union(json: Any, *, target_type: Type) -> Any:
    """Try to deal with union datatypes.

    target_type above needs to be type, because...
    """
    assert is_union_type(target_type)

    # Ex: Union[int, str]
    possible_types = get_union_types(target_type)
    assert possible_types, "No types is a real problem"

    # If it's already one of the json-acceptable types, return that.
    # Ex: Union[int, float]

    for t_type in possible_types:
        # Ignore string types as they are the "universal" cast below.
        if isinstance(json, t_type) and (t_type != str):
            return json

    # Warn in case we enter ambiguous territory.
    # ex Union[datetime, str]  could be lossy
    if str in possible_types:
        warnings.warn(STR_UNION_WARN, SyntaxWarning, stacklevel=2)

    # Not already decoded. Try them in-order and return the first possible.
    # Union[str, datetime] will always be lossy, while Union[datetime, str]
    # could work as expected.
    # The warning from before should be considered still
    for t_type in possible_types:
        try:
            return deserialize(json, target_type=t_type)
        except (ValueError, TypeError):
            pass
    raise ValueError(f"Cannot convert {json} to any of {possible_types}")


def serialize(obj: Any) -> Any:
    """Convert a Dataclass to a dict that can be cast to JSON with the python
    built in "json.dumps()" """

    if is_dataclass(obj):
        result = asdict(obj)
        for key, val in result.items():
            result[key] = serialize(val)
        return result

    # Enumerations are primarily pass-by value
    if isinstance(obj, Enum):
        return serialize(obj.value)

    if isinstance(obj, UUID):
        return obj.hex

    if isinstance(obj, datetime):
        return obj.isoformat()

    # Default, trust that json can deal with it
    return obj


__all__ = ["serialize", "deserialize"]
