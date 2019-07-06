from laspy.file import File
import numpy as np
import dionysus as d
from sys         import argv, exit
import Classes.PCPDS

class BottleneckDistances:

    def __init__(self, parallelograms, test_grid):

        # Dictionary of PCPDS objects
        self.parallelograms = parallelograms

        # A single PCPDS object
        self.test_grid = test_grid

    def naive_search_distances(self, num):
        found_idx = 'Error'

        # Set max bottlenect dist
        best_dist = 1.01

        top_idx = []

        for i in range(num):
            top_idx.append((0, best_dist))

        # temporary fix to null pointcloud issue
        if np.all(self.test_grid.point_cloud) == None:
            print("Error: No points in this section")
            return "Error"
        # Generate persistance diagram to search for
        pd1 = self.test_grid.get_persistance_diagram()
        # Debug
        print(pd1)

        # Loop through all IDX in parallelograms dictionary and compares
        # their bottleneck distance to pd1
        for i in self.parallelograms:

            # Get persistance diagram for i which should be an idx
            # because of how the dict is defined, there is one object that cant get pd
            try:
                pd2 = self.parallelograms[i].get_persistance_diagram()
            except:
                pass

            # Check bottleneck distance against current lowest,
            # if it is lower, saves new distance and that idx value
            try:
                result = d.bottleneck_distance(pd1[0],pd2[0])
            except:
                continue

            # Save a list of top 5 indexes, keep sorted based off the result dist
            top_idx.append((i, result))

            # Sort from low to high
            top_idx = sorted(top_idx, key=lambda x:x[1])
            if len(top_idx) > num:
                top_idx.pop(num-1)

        # Return idx of lowest bottleneck distance to search_idx
        return top_idx
