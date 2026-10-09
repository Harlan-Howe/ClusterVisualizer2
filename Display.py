from typing import Optional, List, Tuple, Callable

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as mpimg
import matplotlib.collections as collections

from ColorMap import ColorMap
from threading import Lock


class Display:
    def __init__(self, background_filename: Optional[str], color_map: Optional[ColorMap]):
        if color_map is None:
            color_map = ColorMap()
        self.color_map = color_map

        self.fig, self.ax = plt.subplots()

        if background_filename is not None:
            self.load_background_image(background_filename)

        # start off with containers for all parts of the graphics for the data.
        self.data_positions: List[Tuple[int, int]] = []
        self.data_size_list: List[float] = []
        self.data_color_list: List[Tuple[float, float, float, float]] = []
        self.data_circles_collection: Optional[collections.Collection] = None

        # start off with containers for all parts of the graphics for attractors' windows.
        self.window_positions: List[Tuple[int, int]] = []
        self.window_width_list: List[float] = []
        self.window_height_list: List[float] = []
        self.window_angle_list: List[float] = []
        self.window_color_list: List[Tuple[float, float, float, float]] = []
        self.window_collection: Optional[collections.Collection] = None

        # start off with containers for all parts of the graphics for attractor stars.
        self.attractor_star_positions = self.window_positions
        self.attractor_star_size_list: List[float] = []
        self.attractor_star_color_list: List[Tuple[float, float, float, float]] = []
        self.attractor_star_collection: Optional[collections.Collection] = None

        # multithreading stuff...
        self.lock = Lock()
        self.looping_function: Optional[Callable] = None

    def load_background_image(self, background_filename: str):
        self.background = mpimg.imread(background_filename)
        height, width = self.background.shape[:2]
        self.ax.imshow(self.background, extent=(0.0, float(width), float(height), 0.0))

        self.set_bounds(max_x=width, max_y=height, invert_y=True)

    def set_axis_labels(self, x_label:str, y_label:str):
        plt.xlabel(x_label)
        plt.ylabel(y_label)

    def set_bounds(self, min_x:float = 0.0, max_x:float=1.0, min_y:float=0.0, max_y:float=1.0, invert_y:bool = False):
        """
        rescales the window to accommodate the given range.
        :param min_x:
        :param max_x:
        :param min_y:
        :param max_y:
        :param invert_y: whether to put the positive direction of y point down or up. True would put (min_x, min_y) in
                         upper left corner; False would put it in lower left corner.
        """
        self.ax.set_xlim(min_x, max_x)
        if invert_y:
            self.ax.set_ylim(max_y, min_y)
        else:
            self.ax.set_ylim(min_y, max_y)