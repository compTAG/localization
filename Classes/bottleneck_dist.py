from laspy.file import File
import numpy as np
import dionysus as d
from sys         import argv, exit
import PCPDS

class BottleneckDistances:

    def __init__(self, parallelograms, testGrid):
        self.parallelograms = parallelograms
        self.testGrid = testGrid

    def naive_search_distances(self):
        found_idx = 'Error'
        # improve this later
        best_dist = 10000000000

        # generates persistance diagram to search for
        pd1 = self.testGrid.get_persistance_diagram()

        #loops through all IDX in parallelograms dictionary and compares their bottleneck distance to pd1
        for i in parallelograms:
            # gets persistance diagram for i which should be an idx
            pd2 = parallelograms[i].get_persistance_diagram()
            #checks bottleneck distance against current lowest, if it is lower, saves new distance and that idx value
            result = .bottleneck_distance(pd1[0],pd2[0])
            if result < best_dist:
                best_dist = result
                found_idx = i
        # returns idx of lowest bottleneck distance to search_idx
        return found_idx
