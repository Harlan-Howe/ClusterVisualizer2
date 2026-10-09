from dataclasses import dataclass
from typing import Tuple

@dataclass
class Datum:
    location: Tuple[float,float]
    attractor_num: int
