import copy
from typing import List, Optional
from Datum import Datum


class Cluster:
    def __init__(self, color_id:int, datum:Optional[Datum] = None, data_list: Optional[List[Datum]] = None):
        """
        this initializer will create a Cluster with EITHER a single datum or a list of data and assign them all the
        same color_id.
        Note: You must have either a datum XOR a data_list.
        :param color_id: the number of a color in the ColorMap.
        :param datum: a single datum or NONE.
        :param data_list: a list of data   or  NONE
        """

        if datum is not None and data_list is not None:
            raise Exception("Cluster should be created with EITHER a point or a point list.")
        elif datum is not None:
            self.__data_list: List[Datum] = [datum]
            self.__mean_location = datum.location
            self.__color_id = color_id
            datum.color_id = color_id
        elif data_list is not None and len(data_list)>0:
            x_sum = 0
            y_sum = 0
            self.__data_list: List[Datum] = []
            for d in data_list:
                x_sum += d.location[0]
                y_sum += d.location[1]
                d.color_id = color_id
                self.__data_list.append(d)
            self.__mean_location = (x_sum / len(data_list), y_sum / len(data_list))
            self.__color_id = color_id
        else:
            raise Exception("Cluster needs to start with at least one Datum.")

    @property
    def data_list(self):
        return self.__data_list

    @property
    def mean_location(self):
        return self.__mean_location

    @property
    def color_id(self):
        return self.__color_id

    def __len__(self) -> int:
        return len(self.__data_list)

    def add_datum(self, datum:Datum):
        old_N = len(self.__data_list)
        # TODO: if you are using the mean location of this cluster, you'll need to update it here.
        datum.color_id = self.__color_id

    def absorb_cluster(self, other:Cluster):
        for d in other.__data_list:
            self.add_datum(d)

    def remove_datum(self, datum:Datum):
        if len(self.__data_list) == 1:
            raise Exception("Cannot create an empty cluster. Delete this cluster, instead.")
        if datum in self.__data_list:
            old_N = len(self.__data_list)
            # TODO: if you are using the mean location of this cluster and might remove data from a cluster, you'll need
            #       to update the mean location here.
        else:
            raise Exception(f"Asked to remove {datum} from cluster, but it is not contained in the cluster.")

    def __delete__(self, instance):
        self.remove_datum(instance)

    def __repr__(self) -> str:
        return f"Cluster {self.__color_id} @ {self.__mean_location} contains {self.__data_list}"
