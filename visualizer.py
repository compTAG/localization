# TODO: Make it able to take in a PCPDS object and visualize the point cloud

import Classes.file_manager as fm
from Classes.PCPDS_manager import PCPDS_Manager as pm
import pptk
import numpy as np

pcpds_obj = fm.load("/Users/clarekirkland/Documents/REU19/localization/cell_collection/small_3_2019-07-12/1011")
point_cloud = pcpds_obj.get_point_cloud()
print("Showing Visualizer:")
P = np.random.rand(100,3)
v = pptk.viewer(point_cloud)
delay = input("Press any key to exit")
print("Done running")
