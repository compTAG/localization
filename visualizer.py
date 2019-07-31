# TODO: Make it able to take in a PCPDS object and visualize the point cloud

import Classes.file_manager as fm
from Classes.PCPDS_manager import PCPDS_Manager as pm
import pptk
import numpy as np
import os.path
import laspy

path_manager = pm()
dir = path_manager.get_path_manager().get_full_cur_dir_var("small_25/")

file_name = "1121601.json"

pcpds_obj = fm.load(os.path.join(dir, file_name))
point_cloud = pcpds_obj.get_point_cloud()
for p in point_cloud:
    print('X: ' + str(p[0]) + ', Y: ' + str(p[1]) + ', Z: ' + str(p[2]))
print("Showing Visualizer:")
P = np.random.rand(100,3)
v = pptk.viewer(point_cloud)
v.set(point_size=.0001)

delay = input("Press any key to exit")

# header = laspy.header.Header()
# outfile = laspy.file.File("output.las", mode="w", header=header)
# outfile.X = [1, 2, 3]
# outfile.Y = [0, 0, 0]
# outfile.Z = [10, 10, 11]
# outfile.close()
# https://gis.stackexchange.com/questions/158708/use-laspy-to-create-las-file-from-scratch-without-opening-an-existing-las-file-f


#Get rid of e^ format
#Scale it between 0 and 1
