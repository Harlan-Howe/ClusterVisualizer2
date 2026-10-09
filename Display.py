import math
from typing import Optional, List, Tuple, Callable

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as mpimg
import matplotlib.collections as collections
import numpy as np

from Attractor import Attractor
from ColorMap import ColorMap
from threading import Lock

from Datum import Datum

WINDOW_RADIUS = 100
DATA_POINT_RADIUS = 0.5
STAR_RADIUS = 6
WINDOW_COLOR = (1.0, 1.0, 0.0, 0.33)

class Display:
    def __init__(self, background_filename: Optional[str], color_map: Optional[ColorMap], show_windows:bool =False):
        if color_map is None:
            color_map = ColorMap()
        self.color_map = color_map

        self.show_windows = show_windows

        self.fig, self.ax = plt.subplots()

        if background_filename is not None:
            self.background: Optional[np.ndarray] = None
            self.load_background_image(background_filename)

        self.data: Optional[List[Datum]] = None
        self.attractors: List[Attractor] = None

        # start off with containers for all parts of the graphics for the data.
        self.data_positions: List[Tuple[float, float]] = []
        self.data_size_list: List[float] = []
        self.data_color_list: List[Tuple[float, float, float, float]] = []
        self.data_circles_collection: collections.CircleCollection = None

        # start off with containers for all parts of the graphics for attractors' windows.
        self.window_positions: List[Tuple[float, float]] = []
        self.window_diameter_list: List[float] = []
        self.window_angle_list: List[float] = []
        self.window_color_list: List[Tuple[float, float, float, float]] = []
        self.window_collection: Optional[collections.EllipseCollection] = None

        # start off with containers for all parts of the graphics for attractor stars.
        self.attractor_star_positions = self.window_positions
        self.attractor_star_size_list: List[float] = []
        self.attractor_star_color_list: List[Tuple[float, float, float, float]] = []
        self.attractor_star_collection: Optional[collections.StarPolygonCollection] = None

        # multithreading stuff...
        self.lock = Lock()
        self.looping_function: Optional[Callable] = None

    def load_background_image(self, background_filename: str):
        self.background = mpimg.imread(background_filename)
        if self.background is None:
            print(f"Could not load background image at {background_filename}")
            return
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

    def set_attractors(self, attractors:List[Attractor]):
        """
        This creates the non-empty collection of windows and attractors (large circles and stars).
        Precondition: self.window_collection has length > 0.
        :return: None
        """
        if attractors is None or len(attractors) == 0:
            raise Exception("Attempting to set up attractors in Display, but there must be at least one attractor.")
        with self.lock:
            self.attractors = attractors

            # establish this class's lists of data about the windows and stars.
            if self.show_windows:
                self.window_color_list = [WINDOW_COLOR for _ in range(len(attractors))]
                self.window_diameter_list = [(2*WINDOW_RADIUS) for _ in range(len(attractors))]
                self.window_angle_list = [0 for _ in range(len(attractors))]

            self.attractor_star_color_list.clear()
            self.attractor_star_positions.clear()
            for a in attractors:
                self.attractor_star_color_list.append(self.color_map.get_color_for_id(a.id))
                self.attractor_star_positions.append(a.location)
            self.attractor_star_size_list = [(2*STAR_RADIUS**2) for _ in range(len(attractors))]

            # build a collection of windows in matplotlib
            if self.show_windows and self.window_collection is None:
                self.window_collection = collections.EllipseCollection(widths=np.array([]),
                                                                       heights=np.array([]),
                                                                       angles=np.array([]),
                                                                       offsets=np.array([]).reshape(-1, 2),
                                                                       units="xy",
                                                                       offset_transform=self.ax.transData)
                self.ax.add_collection(self.window_collection)

            # build a collection of stars in matplotlib.
            if self.attractor_star_collection is None:
                self.attractor_star_collection = collections.StarPolygonCollection(numsides=5,
                                                                                   rotation=0.0,
                                                                                   sizes=np.array([]),
                                                                                   offsets=np.array([]).reshape(-1, 2),
                                                                                   offset_transform=self.ax.transData)
                self.ax.add_collection(self.attractor_star_collection)

        # now send the specific information to matplotlib about these shapes.
        self.update_attractor_collections_in_matplotlib()


    def set_data(self, data: List[Datum]):
        if data is None or len(data) == 0:
            raise Exception("Attempting to set up data in Display, but there must be at least one datum.")

        with self.lock:
            self.data = data
            # update this class's lists of size, position, color
            self.data_size_list = [(math.pi * DATA_POINT_RADIUS ** 2) for _ in range(len(data))]
            self.data_positions.clear()
            self.data_color_list.clear()
            for d in data:
                self.data_positions.append(d.location)
                self.data_color_list.append(self.color_map.get_color_for_id(color_id=d.color_index))

            # tell matplotlib about these changed lists.
            self.data_circles_collection = collections.CircleCollection(sizes=self.data_size_list,
                                                                        offsets=[],
                                                                        offset_transform=self.ax.transData)
            self.data_circles_collection.set_offsets(np.array(self.data_positions))
            self.data_circles_collection.set_color(np.array(self.data_color_list))

            self.ax.add_collection(self.data_circles_collection)

    def append_attractor(self, attractor:Attractor):
        if self.attractors is None:
            self.set_attractors([attractor])
        else:
            with self.lock:
                self.attractors.append(attractor)
                # update this class's lists of size, position, color
                if self.show_windows:
                    self.window_color_list.append(WINDOW_COLOR)
                    self.window_diameter_list.append(2 * WINDOW_RADIUS)
                    self.window_angle_list.append(0)
                self.attractor_star_color_list.append(self.color_map.get_color_for_id(attractor.id))
                self.attractor_star_positions.append(attractor.location)
                self.attractor_star_size_list.append(2 * STAR_RADIUS ** 2)
                # tell matplotlib about these changed lists.
            self.update_attractor_collections_in_matplotlib()

    def update_attractor_collections_in_matplotlib(self):
        with self.lock:
            if self.show_windows and self.window_collection is not None:
                self.window_collection.set_color(self.window_color_list)
                self.window_collection.set_widths(self.window_diameter_list)
                self.window_collection.set_heights(self.window_diameter_list)
                self.window_collection.set_angles(self.window_angle_list)
                self.window_collection.set_offsets(self.window_positions)
            if self.attractor_star_collection is not None:
                self.attractor_star_collection.set_color(self.attractor_star_color_list)
                self.attractor_star_collection.set_sizes(self.attractor_star_size_list)
                self.attractor_star_collection.set_offsets(self.attractor_star_positions)

    def attractor_at_index_has_changed_position(self, idx: int):
        with self.lock:
            self.attractor_star_positions[idx] = self.attractors[idx].location
        self.update_attractor_collections_in_matplotlib()

    def removed_attractor_at_index(self, idx: int):
        with self.lock:
            if len(self.attractor_star_positions) == 1:
                raise Exception("You should not remove the last attractor!")
            if self.show_windows:
                self.window_color_list.pop(-1) # we can just remove the last item if they're all the same.
                self.window.diameter_list.pop(-1)
                del(self.window_positions[idx]) # this one varies by attractor, so we need to remove the right one.
                self.window_angle_list.pop(-1)
            del(self.attractor_star_color_list[idx])
            self.attractor_star_size_list.pop(-1)
            del(self.attractor_star_positions[idx])
        self.update_attractor_collections_in_matplotlib()

    def append_data(self, datum:Datum):
        if self.data is None:
            self.set_data([datum])
        else:
            with self.lock:
                self.data.append(datum)
                # update this class's lists of size, position, color
                self.data_size_list.append((math.pi*DATA_POINT_RADIUS**2))
                self.data_positions.append(datum.location)
                self.data_color_list.append(self.color_map.get_color_for_id(color_id=datum.color_index))
                # tell matplotlib about these changed lists.
                self.data_circles_collection.set_offsets(np.array(self.data_positions))
                self.data_circles_collection.set_sizes(self.data_size_list)
                self.data_circles_collection.set_color(self.data_color_list)

    def datum_at_index_has_changed_color(self, idx: int):
        with self.lock:
            self.data_color_list[idx] = self.color_map.get_color_for_id(color_id=self.data[idx].color_index)
            self.data_circles_collection.set_color(self.data_color_list)

    def set_looping_function(self, func:Optional[Callable]):
        """
        Sets which method, if any, should be called whenever the graph is about to update.
        :param func: the method to call, or None
        :return: None
        """
        self.looping_function = func