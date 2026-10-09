from dataclasses import dataclass
from typing import Tuple

@dataclass
class Attractor:
    id: int
    location: Tuple[float, float]
    is_active: bool = True
