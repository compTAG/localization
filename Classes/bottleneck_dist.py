from laspy.file import File
import numpy as np
import dionysus as d
from sys         import argv, exit
import Classes.PCPDS

class BottleneckDistances:

    def __init__(self):
        pass

    def get_distances(filt1, filt2):
        return d.bottleneck_distance(filt1,filt2)

    def get_collectionset():
        # TODO
        # return a list of touples of idx and filtrations from PCPDS objects
        # ex[(identifier1, ripsfilt1), (identifier2, ripsfilt2),...]

    def search_distances(num, searchfilt, collectionfilts = get_collectionset()):
        found_idx = 'Error'
        top_idx = []
        for i in collectionfilts
            testfilt = collectionfilts[i][1]
            result = get_distances(testfilt, searchfilt)
            top_idx.append(collectionfilts[i][0], result)
            top_idx = sorted(top_idx, key=lambda x:x[1])
            if len(top_idx) > num:
                top_idx.pop(num-1)
        return top_idx
