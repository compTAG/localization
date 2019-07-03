# PCPDS stands for Point Cloud Persistance Diagram Section.
# This class is effectively a 'section', or 'chunk', of the larger point cloud data set being used.
# It contains both a 'chunk' of the larger point cloud, and the 'chunk's processed persistance diagram.

import numpy as np
import json
import jsonpickle

class PCPDS:

    def __init__(self, cell_id, filename, distance = 1):
        # The point cloud should be set up a set of Points. Points possibly
        # being represented by touples of three values.
        self.point_cloud = None

        # The persistance diagram will be processed from the point cloud in this class
        self.persistance_diagram = None
        # TODO: Question, won't that cause missing features
        # to occur at the edges of each section? Will that matter in the long run?

        # cell_id structure to be handled in lasproscessing.py
        self.cell_id = cell_id

        #Tracks the .las file the PD belongs to
        self.filename = filename

        # determines n skeleton for rips filtration
        self.skeleton = 1

        # scales distances for rips filtration
        self.scalar = 0.2

        # rips filt distance
        self.distance = distance

    def get_xyz(self):
        return X, Y, Z

    def set_point_cloud(self, point_cloud):
        # sets point cloud
        self.point_cloud = point_cloud

        # TODO setup XYZ for get_xyz?

    def distances(self, box_width):
        # temporary - we should play with this to determine best distance
        return box_width*self.scalar


    def get_persistance_diagram(self):
    # if persistance_diagram has not been calculated, create it
        try:
            self.persistance_diagram
        except NameError:
            # try to create the persistance diagram
            try:
                f = d.fill_rips(self.point_cloud, self.skeleton , self.distances(self.box_width))
                m = d.homology_persistence(f)
                diagram = d.init_diagrams(m,f)
                self.persistance_diagram = diagram
                return diagram
            # account for input errors
            except:
                print("You forgot to initialize stuff")




    #Generate/save into specified folder name w/ timestamp
    # This saves this object in JSON format in the 'Sections' folder
    def save(self, dir_name):
        # Transform this object into JSON string:
        pcpds = jsonpickle.encode(self)

        with open(dir_name+':'+self.filename+str(self.cell_id), 'w') as outfile:
            json.dump(pcpds, outfile)


    # Loads a PCPDS object from the corresponding JSON file provided it exists
    def load_section(temp_cell_id, dir_name):
        # TODO: check if the file exists, load it in, return it.

        with open(dir_name+':'+self.filename+str(test_cell_id)) as json_file:
            data = json.load(json_file)

            print(data)

            pcpds = jsonpickle.decode(data)

            return pcpds
