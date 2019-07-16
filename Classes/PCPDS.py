# PCPDS stands for Point Cloud Persistance Diagram Section.
# This class is effectively a 'section', or 'chunk', of the larger point cloud data set being used.
# It contains both a 'chunk' of the larger point cloud, and the 'chunk's processed persistance diagram.

import numpy as np
import dionysus as d
import filtrations.py

class PCPDS:

    def __init__(self, cell_id, distance = 1):
        # The point cloud should be set up a set of Points. Points possibly
        # being represented by touples of three values.
        self.point_cloud = None

        self.persistance_diagram = None

        # cell_id is not only the filename, but the xyz coordinates in string form
        self.cell_id = cell_id
        print(f"my cellid is {self.cell_id}")

        # determines n skeleton for rips filtration
        self.skeleton = 1

        # scales distances for rips filtration
        self.scalar = 0.2

        # rips filt distance
        self.distance = distance

    def set_point_cloud(self, point_cloud):
        self.point_cloud = point_cloud

    def get_point_cloud(self):
        return self.point_cloud


    def distances(self, box_width):
        # Temporary - we should play with this to determine best distance
        return box_width*self.scalar


    def get_persistance_diagram(self):
        return persistance_diagram

    def generate_persistance_diagram(self):
        diagram_gen = Filtration.get_rips_diagram
        self.persistance_diagram = diagram_gen(self.point_cloud, self.distance)
