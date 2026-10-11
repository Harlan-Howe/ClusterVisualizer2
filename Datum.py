from dataclasses import dataclass
from typing import Tuple

@dataclass
class Datum:
    location: Tuple[float,float]
    color_index: int
    id: int # a value to distinguish between two points at the same location.

    def __hash__(self) -> int:
        return hash(self.location) + hash(id) # we aren't including color_index, since that might change!

    def __eq__(self, value: object, /) -> bool:
        if type(value) is not Datum:
            return False
        return self.location == value.location and self.id == value.id

