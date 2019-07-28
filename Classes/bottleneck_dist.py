from laspy.file import File
import numpy as np
import dionysus as d
# from sys import argv, exit
import Classes.PCPDS
import Classes.file_manager as fm
import os.path
from Classes.menu import menu

def get_distances(filt1, filt2):
    return d.bottleneck_distance(filt1[0],filt2[0])

def search_distances(num, searchfilt, collection_path):
    cell_IDs = fm.find_files(collection_path, '.json')
    top_idx = []
    tracker = 0
    for id in cell_IDs:
        pcpds = fm.load(os.path.join(collection_path, id))

        result = get_distances(pcpds.get_persistance_diagram(), searchfilt)
        #print("CURRENT CELL_ID:", id)
        if len(top_idx) < num:
            top_idx.append([id, result])
            top_idx = sorted(top_idx, key=lambda x:x[1])
        elif top_idx[-1][1] > result and not [id, result] in top_idx:
            #print("REPLACING:",top_idx[-1], "LIST LEN:",len(top_idx), top_idx)
            top_idx.pop(-1)
            top_idx.append([id, result])
            #print("\nBEFORE SORT:", top_idx)
            top_idx = sorted(top_idx, key=lambda x:x[1])
            #print("AFTER SORT:", top_idx)
            #print("WITH:", id, result, "LIST LEN:", len(top_idx))

    
        menu.progress(tracker, len(cell_IDs), 'Processing Search_Disantce...')
        tracker = tracker + 1
    print("\n")
    return top_idx
