import random
from typing import List, Optional

from matplotlib.animation import FuncAnimation

from Attractor import Attractor
from Cluster import Cluster
from ColorMap import ColorMap
from Datum import Datum
from Display import Display
from Display import WINDOW_RADIUS


class ClusterRunner:
    def __init__(self):
        self.color_map = ColorMap()
        self.data:List[Datum] = []
        self.data_bounds = {"x_min":0.0, "y_min":0.0, "x_max":1.0, "y_max":1.0}
        self.attractors:Optional[List[Attractor]] = None
        self.clusters:Optional[List[Cluster]] = None
        self.display = Display(self.color_map,show_windows=True)
        self.iteration_counter = 0
        self.animation_function_list: List[FuncAnimation] = [] # this is the pointer to control the animation loop.

        self.datum_id_counter = 0

        self.load_data("coordinates.txt")
        self.display.set_data(self.data)
        print(f"{self.data_bounds=}")
        self.display.set_bounds(min_x= self.data_bounds["x_min"],
                                max_x= self.data_bounds["x_max"],
                                min_y= self.data_bounds["y_min"],
                                max_y= self.data_bounds["y_max"],
                                invert_y=True)

        # if you want attractors, activate the following:
        self.create_starting_attractors(5)
        print(self.attractors)
        print(self.color_map)

        if self.attractors is not None:
            self.display.set_attractors(self.attractors)

        # if you want to have clusters at the start of the program, activate the following:
        # self.create_starting_clusters()



    def load_data(self, filename:str):
        with open(filename, "r") as inputFile:
            for line in inputFile:
                parts = line.split("\t")
                d = Datum(location=(float(parts[0]),float(parts[1])),color_index=0, id=self.datum_id_counter)
                self.datum_id_counter += 1
                self.data.append(d)
                self.data_bounds["x_min"] = min(self.data_bounds["x_min"], float(parts[0]))
                self.data_bounds["x_max"] = max(self.data_bounds["x_max"], float(parts[0]))
                self.data_bounds["y_min"] = min(self.data_bounds["y_min"], float(parts[1]))
                self.data_bounds["y_max"] = max(self.data_bounds["y_max"], float(parts[1]))

    def create_starting_attractors(self, K:int):
        """
        creates K randomly placed attractors within the bounds of the data. If you want, you might modify this to set
        them to K randomly chosen data locations.
        If you are doing mean-shift (regular or tree-climbing), you might replace this with a grid of attractors.
        :param K: the number of attractors desired
        """
        attractors = []
        for i in range(K):
            col = self.color_map.add_color()
            attractors.append(Attractor(color_id=col,
                                        location=(random.random()*(self.data_bounds["x_max"]-self.data_bounds["x_min"])+
                                                                                            self.data_bounds["x_min"],
                                                  random.random()*(self.data_bounds["y_max"]-self.data_bounds["y_min"])+
                                                                                            self.data_bounds["y_min"])))
        self.attractors=attractors

    def create_starting_clusters(self):
        """
        creates a list of clusters. For something like agglomeration, you might make one cluster for each data point.
        For something like DBSCAN, you might start with a list of no clusters but create them as part of your process.
        For something like k-Means or mean-shift, this might be something you don't need but could do at the end of
        your program.
        """
        clusters = []
        # write code to create whatever clusters you want here.

        self.clusters = clusters

    def start(self):
        print("Starting.")
        # Tell the Display what method should be called each time it is about to update the graph.
        self.display.set_looping_function(self.iterate_loop)

        # Tell the Disualizer to begin animating.
        self.display.start_animation(animation_list=self.animation_function_list)

    def pause_animation(self):
        if len(self.animation_function_list) > 0:
            self.animation_function_list[0].pause()

    def resume_animation(self):
        if len(self.animation_function_list) > 0:
            self.animation_function_list[0].resume()

    def iterate_loop(self):
        """
        This method gets called over and over again by the animation loop.
        """
        print(f"Iteration: {self.iteration_counter}")
        self.iteration_counter += 1
        if self.iteration_counter == 1:
            return  # we're getting a bogus first iteration before the screen updates, so this skips this one.

        keep_looping = False # unless you change this when your data, attractors or clusters change, or if you haven't
                             # reached the desired K, this will be the last iteration.

        # TODO: here is where you will execute a step of your algorithm.






        if not keep_looping and self.iteration_counter > 0:
            self.pause_animation()
            self.conclude()


    def conclude(self):
        """
        The animation is over - things stopped changing OR you've reached the desired K. Do analysis of the results or
        clean up the image to reflect the results.
        :return:
        """
        print("Program ended.")


if __name__== "__main__":
    cr = ClusterRunner()
    cr.start()