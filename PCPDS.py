# PCPDS stands for Point Cloud Persistance Diagram Section.
# This class is effectively a 'section', or 'chunk', of the larger point cloud data set being used. 
# It contains both a 'chunk' of the larger point cloud, and the 'chunk's processed persistance diagram.

import numpy as np

class PCPDS:

    def __init__(self, X, Y, Z):
        # The point cloud should be set up a set of Points. Points possibly being represented by touples of three values. 
        self.point_cloud = None
        
        # The persistance diagram will be processed from the point cloud in this class
        self.persistance_diagram = None
        # TODO: Question, won't that cause missing features to occur at the edges of each section? Will that matter in the long run?
        
        # X, Y, & Z represent this section's position in regaurds to the larger data set
        self.X = X
        self.Y = Y
        self.Z = Z
        
    def set_point_cloud(self, point_cloud):
        self.point_cloud = point_cloud    

    def generate_persistance_diagram(self):
        # TODO: Process point_cloud via rips filtration here and save it in the persistance_diagram variable
        pass
    
    def get_persistance_diagram(self):
        return persistance_diagram
        
    