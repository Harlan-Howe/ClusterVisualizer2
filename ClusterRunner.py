import random
from typing import List, Optional

from Attractor import Attractor
from Cluster import Cluster
from Datum import Datum

class ClusterRunner:
    def __init__(self):
        self.data:List[Datum] = []
        self.data_bounds = {"x_min":0.0, "y_min":0.0, "x_max":1.0, "y_max":1.0}
        self.attractors:Optional[List[Attractor]] = None
        self.clusters:Optional[List[Cluster]] = None
        self.load_data("mydata.txt")
        self.create_starting_attractors(5)
        self.create_starting_clusters()

    def load_data(self, filename:str):
        with open(filename, "r") as inputFile:
            for line in inputFile:
                parts = line.split("\t")
                d = Datum(location=(float(parts[0]),float(parts[1])),color_index=0)
                self.data.append(d)
                self.data_bounds["x_min"] = min(self.data_bounds["x_min"], float(parts[0]))
                self.data_bounds["x_max"] = max(self.data_bounds["x_max"], float(parts[0]))
                self.data_bounds["y_min"] = min(self.data_bounds["y_min"], float(parts[1]))
                self.data_bounds["y_max"] = min(self.data_bounds["y_max"], float(parts[1]))

    def create_starting_attractors(self, K:int):
        """
        creates K randomly placed attractors within the bounds of the data. If you want, you might modify this to set
        them to K randomly chosen data locations.
        If you are doing mean-shift (regular or tree-climbing), you might replace this with a grid of attractors.
        :param K:
        :return:
        """
        attractors = []
        for i in range(K):
            attractors.append(Attractor(id=i,
                                        location=(random.random()*(self.data_bounds["x_max"]-self.data_bounds["x_min"])+
                                                                                            self.data_bounds["x_min"],
                                                  random.random()*(self.data_bounds["x_max"]-self.data_bounds["x_min"])+
                                                                                            self.data_bounds["x_min"])))
        self.attractors=attractors



if __name__== "__main__":
    cr = ClusterRunner()