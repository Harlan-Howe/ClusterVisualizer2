from typing import List
from Datum import Datum


class Cluster:
    def __init__(self, attractor_id:int, datum:Datum = None, data_list: List[Datum] = None):
        if datum is None and (data_list is None or len(data_list) == 0):
            raise Exception("Cluster needs to start with at least one Datum.")
        if datum is not None and data_list is not None:
            raise Exception("Cluster should be created with either a point or a point list.")
        if datum is not None:
            self.data_list: List[Datum] = [datum]
            self.mean_location = datum.location
            self.attractor_id = attractor_id
        else:
            x_sum = 0
            y_sum = 0
            self.data_list: List[Datum] = []
            for d in data_list:
                x_sum += d.location[0]
                y_sum += d.location[1]
                self.data_list.append(d)
            self.mean_location = (x_sum/len(data_list),y_sum/len(data_list))
            self.attractor_id = attractor_id


