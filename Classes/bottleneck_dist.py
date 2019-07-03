from laspy.file import File
import numpy as np
import dionysus as d
from sys         import argv, exit
import PCPDS

class BottleneckDistances:

    def __init__(self, parallelograms, test_grid):

        # Dictionary of PCPDS objects
        self.parallelograms = parallelograms

        # A single PCPDS object
        self.test_grid = test_grid

    def naive_search_distances(self):
        found_idx = 'Error'

        # Set max bottlenect dist
        best_dist = 1.01

        # Generate persistance diagram to search for
        pd1 = self.test_grid.get_persistance_diagram()

        # Loop through all IDX in parallelograms dictionary and compares
        # their bottleneck distance to pd1
        for i in parallelograms:

            # Get persistance diagram for i which should be an idx
            pd2 = parallelograms[i].get_persistance_diagram()

            # Check bottleneck distance against current lowest, if it is lower, saves new distance and that idx value
            result = .bottleneck_distance(pd1[0],pd2[0])

            # Change this to save a list of top 5 indexes
            if result < best_dist:
                best_dist = result
                found_idx = i

        # Return idx of lowest bottleneck distance to search_idx
        return found_idx
