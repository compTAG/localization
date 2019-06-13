# PCPDS stands for Point Cloud Persistance Diagram Section.
# This class is effectively a 'section', or 'chunk', of the larger point cloud data set being used.
# It contains both a 'chunk' of the larger point cloud, and the 'chunk's processed persistance diagram.

import numpy as np
import json
import jsonpickle

class PCPDS(object):

    def __init__(self, I, J, K, X, Y, Z):
        # The point cloud should be set up a set of Points. Points possibly being represented by touples of three values.
        self.point_cloud = None

        # The persistance diagram will be processed from the point cloud in this class
        self.persistance_diagram = None
        # TODO: Question, won't that cause missing features to occur at the edges of each section? Will that matter in the long run?

        # I, J, & K represent this section's position in regaurds to the larger data set
        self.I = I
        self.J = J
        self.K = K

        # X, Y, Z represents this 'section's dimensional lengths
        self.X = X
        self.Y = Y
        self.Z = Z

    def get_xyz(self):
        return X, Y, Z

    def set_point_cloud(self, point_cloud):
        self.point_cloud = point_cloud

    def generate_persistance_diagram(self):
        # TODO: Process point_cloud via rips filtration here and save it in the persistance_diagram variable
        pass

    def get_persistance_diagram(self):
        return persistance_diagram

    # This saves this object in JSON format in the 'Sections' folder
    def save(self):
        # Transform this object into JSON string:
        pcpds = jsonpickle.encode(self)

        with open('Sections/PCPDS:'+str(self.X)+str(self.Y)+str(self.Z), 'w') as outfile:
            json.dump(pcpds, outfile)

# Loads a PCPDS object from the corresponding JSON file provided it exists
def load_section(X, Y, Z):
    # TODO: check if the file exists, load it in, return it.
    with open('Sections/PCPDS:'+str(X)+str(Y)+str(Z)) as json_file:
        data = json.load(json_file)

        print(data)

        pcpds = jsonpickle.decode(data)

        return pcpds
