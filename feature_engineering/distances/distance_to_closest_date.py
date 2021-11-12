from typing import List

import numpy as np


def get_distance(coords1:List[str], coords2:List[str]):
    """
    Computes the average euclidian distance beatween min and max coordinates of two words
    """
    distance_min = np.sqrt((float(coords1[0]) - float(coords2[0]))**2 + (float(coords1[2]) - float(coords2[2]))**2)
    distance_max = np.sqrt((float(coords1[1]) - float(coords2[1]))**2 + (float(coords1[3]) - float(coords2[3]))**2)

    return((distance_max + distance_min)/2)

def get_distance_to_closest_date(entity_coordinates:List[str], dates_coordinates: dict[List[str]]):
    """"""

    distance_min = np.inf
    for coords in dates_coordinates.values():
        distance_min = min(distance_min, get_distance(entity_coordinates, coords))

    return distance_min
