from laspy.file import File
import numpy as np
import dionysus as d
from sys         import argv, exit
import Classes.PCPDS
import Classes.file_manager as fm
import os.path

def get_distances(filt1, filt2):
    return d.bottleneck_distance(filt1[0],filt2[0])

def get_collectionset(dir_path):
    return fm.find_files(dir_path)

def search_distances(num, searchfilt, collection_path):
    cell_IDs = get_collectionset(collection_path)
    top_idx = []
    for id in cell_IDs:

        temp = os.path.join(collection_path, id)
        #print(temp)
        pcpds = fm.load(temp)

        testfilt = pcpds.get_persistance_diagram()

        result = get_distances(testfilt, searchfilt)

        top_idx.append([id, result])
        top_idx = sorted(top_idx, key=lambda x:x[1])
        if len(top_idx) > num:
            top_idx.pop(num-1)
    return top_idx
