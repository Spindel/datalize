import dataclasses
import uuid
from datetime import datetime
from typing import List, Optional

import datalize


@dataclasses.dataclass
class Point:
    val: str
    ts: datetime


@dataclasses.dataclass
class OneExample:
    my_id: uuid.UUID
    points: List[Point]
    name: Optional[str] = "Example"


if __name__ == "__main__":
    from_json = {
        "my_id": "029affa6-814e-439a-a61d-2614ad184e0d",
        "points": [
            {"val": "timestamps", "ts": "2020-05-18T13:39:00.000666"},
            {"val": "with timezone", "ts": "2020-05-18T13:37:00.000666+03:00"},
        ],
    }
    obj = datalize.deserialize(from_json, target_type=OneExample)
    assert obj.name == "Example"
    assert obj.points[1].val == "with timezone"
    print(obj)
