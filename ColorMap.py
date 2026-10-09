import random
from typing import Optional, Tuple


class ColorMap:
    def __init__(self):
        self.__used_colors = [(0.0, 0.0, 0.0, 1.0)]
        self.__default_colors = ((0.0, 0.0, 1.0, 1.0), (0.0, 1.0, 0.0, 1.0), (1.0, 0.0, 0.0, 1.0),
                                 (1.0, 1.0, 0.0, 1.0), (1.0, 0.0, 1.0, 1.0), (0.0, 1.0, 1.0, 1.0),
                                 (0.0, 0.5, 1.0, 1.0), (1.0, 0.0, 0.5, 1.0), (0.5, 0.5, 1.0, 1.0),
                                 (0.5, 1.0, 0.5, 1.0), (1.0, 0.5, 0.5, 1.0))
        self.__default_colors_used = 0

    def __len__(self):
        return len(self.__used_colors)

    def get_color_for_id(self, color_id:int):
        if 0<= color_id <= len(self.__used_colors):
            return self.__used_colors[color_id]
        raise IndexError(f"Id {color_id} is out of bounds for colormap with length {len(self.__used_colors)}.")

    def add_color(self, color:Optional[Tuple[float, float, float, float]] = None) -> int:
        """
        adds a new color to the list and returns the id of that color.
        :param color: the color to add. If this is None, picks a new color, first from the list of default values, but
                      then randomized (darker) colors when the default list is exhausted.
        :return: the id for the color added.
        """
        if color is not None:
            self.__used_colors.append(color)
        else:
            if self.__default_colors_used < len(self.__default_colors):
                self.__used_colors.append(self.__default_colors[self.__default_colors_used])
                self.__default_colors_used += 1
            else:
                self.__used_colors.append((random.random()*0.75, random.random()*0.75,
                                           random.random()*0.75, 1.0))
        return len(self.__used_colors)-1

    def __repr__(self) -> str:
        result = f"{self.__default_colors_used=}\t{len(self.__used_colors)=}"
        for i in range(len(self.__used_colors)):
            result = result +(f"\n{self.__used_colors[i]}")
        return result