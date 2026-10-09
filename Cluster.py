import copy
from typing import List
from Datum import Datum


class Cluster:
    def __init__(self, attractor_id:int, datum:Datum = None, data_list: List[Datum] = None):
        if datum is None and (data_list is None or len(data_list) == 0):
            raise Exception("Cluster needs to start with at least one Datum.")
        if datum is not None and data_list is not None:
            raise Exception("Cluster should be created with either a point or a point list.")
        if datum is not None:
            self.__data_list: List[Datum] = [datum]
            self.__mean_location = datum.location
            self.__attractor_id = attractor_id
        else:
            x_sum = 0
            y_sum = 0
            self.__data_list: List[Datum] = []
            for d in data_list:
                x_sum += d.location[0]
                y_sum += d.location[1]
                self.__data_list.append(d)
            self.__mean_location = (x_sum / len(data_list), y_sum / len(data_list))
            self.__attractor_id = attractor_id

    @property
    def data_list(self):
        return copy.deepcopy(self.__data_list)

    @property
    def mean_location(self):
        return self.__mean_location

    @property
    def attractor_id(self):
        return self.__attractor_id

    def __len__(self) -> int:
        return len(self.__data_list)

    def add_datum(self, datum:Datum):
        old_N = len(self.__data_list)
        self.__mean_location = ((old_N*self.__mean_location[0] + datum.location[0])/(old_N+1),
                                (old_N*self.__mean_location[1] + datum.location[1])/(old_N+1))
        self.__data_list.append(datum)
        datum.color_index = self.__attractor_id

    def absorb_cluster(self, other:Cluster):
        for d in other.data_list:
            self.add_datum(d)

    def remove_datum(self, datum:Datum):
        if len(self.__data_list) == 1:
            raise Exception("Cannot create an empty cluster. Delete this cluster, instead.")
        if datum in self.__data_list:
            old_N = len(self.__data_list)
            self.__mean_location= ((old_N * self.__mean_location[0] - datum.location[0])/(old_N-1),
                                   (old_N * self.__mean_location[1] - datum.location[1])/(old_N-1))
            self.__data_list.remove(datum)
        else:
            raise Exception(f"Asked to remove {datum} from cluster, but it is not contained in the cluster.")

    def __delete__(self, instance):
        self.remove_datum(instance)

    def __repr__(self) -> str:
        return f"Cluster {self.__attractor_id} @ {self.__mean_location} contains {self.__data_list}"
