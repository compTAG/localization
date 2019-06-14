# PCPDS stands for Point Cloud Persistance Diagram Section.
# This class is effectively a 'section', or 'chunk', of the larger point cloud data set being used.
# It contains both a 'chunk' of the larger point cloud, and the 'chunk's processed persistance diagram.

import numpy as np
import json
import jsonpickle
import DoRips

class PCPDS(object):

    def __init__(self, X, Y, Z, cellID):
        # The point cloud should be set up a set of Points. Points possibly being represented by touples of three values.
        self.point_cloud = None

        # The persistance diagram will be processed from the point cloud in this class
        self.persistance_diagram = None
        # TODO: Question, won't that cause missing features to occur at the edges of each section? Will that matter in the long run?

        # X, Y, Z are x, y, and z points for section
        self.X = X
        self.Y = Y
        self.Z = Z

        # cellID structure to be handled in lasproscessing.py
        self.cellID = cellID

    def get_xyz(self):
        return X, Y, Z

    def set_point_cloud(self):
        # works iff lasproscessing works the way i think it Does
        temp = np.array([self.X,self.Y,self.Z])
        point_cloud = temp.T
        self.point_cloud = point_cloud

    def generate_persistance_diagram(self, dist = 1):
        # try except statement checks for needed values to generate
        try:
            self.pointcloud
        except NameError:
            set_point_cloud()
        finally:
            R = RipsFilt(dist,self.point_cloud)
            self.persistance_diagram = R.do_persistance('pcpds')

    def get_persistance_diagram(self):
        # if persistance_diagram has not been calculated, create it
        try:
            self.persistance_diagram
        except NameError:
            # creates a filtration object with stored pointcloud
            R = RipsFilt(1,self.point_cloud)
            # returns a persistance diagram
            return R.do_persistance('pcpds')
        else:
            return self.persistance_diagram


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
