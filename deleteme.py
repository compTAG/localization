from ProcessLas import ProcessLas
import PCPDS
import DoRips
import numpy as np
import os



def naive_search_distances(self):
    found_idx = 'Error'
    # improve this later
    best_dist = 10000000000

    # generates persistance diagram to search for
    pd1 = parallelograms[search_idx].get_persistance_diagram()

    #loops through all IDX in parallelograms dictionary and compares their bottleneck distance to pd1
    for i in parallelograms:
        # gets persistance diagram for i which should be an idx
        pd2 = parallelograms[i].get_persistance_diagram()
        #checks bottleneck distance against current lowest, if it is lower, saves new distance and that idx value
        if d.bottleneck_distance(pd1[0],pd2[0]) < best_dist:
            best_dist = d.bottleneck_distance(pd1[0],pd2[0])
            found_idx = i
    # returns idx of lowest bottleneck distance to search_idx
    print(parallelograms)
    return found_idx

dim = int(input("Enter Partition Count (1D): "))
m = ProcessLas("test.las", dim, 0)
m.inputLas()
