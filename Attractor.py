from dataclasses import dataclass
from typing import Tuple

@dataclass
class Attractor:
    color_id: int
    location: Tuple[float, float]
