# PCPDS stands for Point Cloud Persistance Diagram Section.
# This class is effectively a 'section', or 'chunk', of the larger point cloud data set being used.
# It contains both a 'chunk' of the larger point cloud, and the 'chunk's processed persistance diagram.

import numpy as np
import dionysus as d

class PCPDS:

    def __init__(self, cell_id, dimensions, distance = 1):
        
        # The point cloud should be set up a set of Points. Points possibly
        # being represented by touples of three values.
        self.point_cloud = None

        self.persistance_diagram = None

        # cell_id is not only the filename, but the xyz coordinates in string form
        self.cell_id = cell_id

        self.dimensions = dimensions

        # determines n skeleton for rips filtration
        self.skeleton = 1

        # scales distances for rips filtration
        self.scalar = 0.2

        # rips filt distance
        self.distance = distance

    def get_skeleton(self):
        return self.skeleton

    def get_distance(self):
        return self.distance

    def set_point_cloud(self, point_cloud):
        self.point_cloud = point_cloud

    def get_point_cloud(self):
        return self.point_cloud

    def get_cellID(self):
        return self.cell_id

    def get_dimensions(self):
        return self.dimensions

    # Split cell_id into x and y values assuming there is a leading 1 and
    def get_xyz(self):

        # Removes the 1 from the beginning of the string
        cell_id = self.cell_id[1:]

        xyz = int(cell_id)

        if xyz is 0:
            return (0, 0, 0)

        trunc_val = 10**(int(len(cell_id)/3))

        Z = xyz % trunc_val
        xyz = int(xyz/trunc_val)

        Y = xyz % trunc_val
        xyz = int(xyz/trunc_val)

        X = xyz % trunc_val
        
        return (X, Y, Z)

    # Calculates the boundaries of the point cloud.
    def get_bounds(self):
        x,y,z = self.get_xyz()

        dimensions = self.get_dimensions()

        dimX = dimensions[0]
        dimY = dimensions[1]
        dimZ = dimensions[2]

        low_x_bound = x * dimX
        high_x_bound = x * dimX + dimX
        low_y_bound = y * dimY
        high_y_bound = y * dimY + dimY
        low_z_bound = z * dimZ
        high_z_bound = z * dimZ + dimZ

        bounds = (low_x_bound, high_x_bound, low_y_bound, high_y_bound, low_z_bound, high_z_bound)

        return bounds


    def distances(self, box_width):
        # Temporary - we should play with this to determine best distance
        return box_width * self.scalar

    def get_persistance_diagram(self):
        return self.persistance_diagram

    def set_persistance_diagram(self, pd):
        self.persistance_diagram = pd
