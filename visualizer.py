# TODO: Make it able to take in a PCPDS object and visualize the point cloud

import Classes.file_manager as fm
from Classes.PCPDS_manager import PCPDS_Manager as pm
import pptk
import numpy as np
import os.path

path_manager = pm()
dir = path_manager.get_path_manager().get_full_cur_dir("small_3_2019-07-12/")

file_name = "1001"

pcpds_obj = fm.load(os.path.join(dir, file_name))
point_cloud = pcpds_obj.get_point_cloud()
print("Showing Visualizer:")
P = np.random.rand(100,3)
v = pptk.viewer(point_cloud.T)
v.set(point_size=0.01)

delay = input("Press any key to exit")
