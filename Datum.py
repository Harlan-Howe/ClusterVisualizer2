from dataclasses import dataclass
from typing import Tuple

@dataclass
class Datum:
    location: Tuple[float,float]
    color_index: int
