# PCPDS stands for Point Cloud Persistance Diagram Section.
# This class is effectively a 'section', or 'chunk', of the larger point cloud data set being used.
# It contains both a 'chunk' of the larger point cloud, and the 'chunk's processed persistance diagram.

import numpy as np
import json
import jsonpickle
from Classes.reference import reference as ref

class PCPDS:

    def __init__(self, cell_id, filename, distance = 1):
        # The point cloud should be set up a set of Points. Points possibly
        # being represented by touples of three values.
        self.point_cloud = None

        # The persistance diagram will be processed from the point cloud in this class
        self.persistance_diagram = None

        # TODO: Make cell_id & the file name the same thing effectively?
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
        # TODO: parse filename/cell_ID into X, Y, & Z
        return X, Y, Z

    def set_point_cloud(self, point_cloud):
        # sets point cloud
        self.point_cloud = point_cloud


    def distances(self, box_width):
        # Temporary - we should play with this to determine best distance
        return box_width*self.scalar


    def get_persistance_diagram(self):
    # If persistance_diagram has not been calculated, create it
        try:
            self.persistance_diagram
        except NameError:
            # Try to create the persistance diagram
            try:
                f = d.fill_rips(self.point_cloud, self.skeleton , self.distances(self.box_width))
                m = d.homology_persistence(f)
                diagram = d.init_diagrams(m,f)
                self.persistance_diagram = diagram
                return diagram
            # Account for input errors
            except:
                print("You forgot to initialize stuff")


    # Generate/save into specified folder name w/ timestamp
    # This saves this object in JSON format in the 'Sections' folder
    def save(self, dir_name):
        # Transform this object into JSON string:
        pcpds = jsonpickle.encode(self)

        with open(dir_name+':' + self.filename + str(self.cell_id), 'w') as outfile:
            json.dump(pcpds, outfile)

# Loads a PCPDS object from the corresponding JSON file provided it exists

# NOTE: Notice the indentation here, these methods are not part of the PCPDS object, but rather
# are to be called implicitly as PCPDS.loadsection(), so they are NOT reliant on the PCPDS object
# already being loaded.
def load_section(dir_name, cell_id):

    with open(dir_name+':'+str(cell_id)) as json_file:

        data = json.load(json_file)
        print(data)
        pcpds = jsonpickle.decode(data)

    pcpds = jsonpickle.decode(data)

    # This returns the decoded pcpds object
    return pcpds

# This version of the loading method only requires the cell_id to be passed  in, 
# as it uses a preset class reference to the directory. This way, we can load in
# sections from a targeted folder in more loosely coupled fasion.
# It does however require that the folder path be set at some point prior to calling.
def load_section(cell_id):
    
    if ref.get_cur_dir_name() is not None:
        with open(ref.get_cur_dir_name()+':'+str(cell_id)) as json_file:

            data = json.load(json_file)
            print(data)
            pcpds = jsonpickle.decode(data)

        pcpds = jsonpickle.decode(data)

        # This returns the decoded pcpds object
        return pcpds
    
    else:
        print("ERROR: The current directory has not yet been selected, so no section will be loaded.")
        return None
