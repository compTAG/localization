# PCPDS stands for Point Cloud Persistance Diagram Section.
# This class is effectively a 'section', or 'chunk', of the larger point cloud data set being used.
# It contains both a 'chunk' of the larger point cloud, and the 'chunk's processed persistance diagram.

import numpy as np
import json
import jsonpickle
from Classes.reference import reference as ref
import dionysus as d
import os

class PCPDS:

    def __init__(self, cell_id, distance = 1):
        # The point cloud should be set up a set of Points. Points possibly
        # being represented by touples of three values.
        self.point_cloud = None

        # The persistance diagram will be processed from the point cloud in this class
        self.persistance_diagram = None

        # cell_id is not only the filename, but the xyz coordinates in string form
        self.cell_id = cell_id

        # determines n skeleton for rips filtration
        self.skeleton = 1

        # scales distances for rips filtration
        self.scalar = 0.2

        # rips filt distance
        self.distance = distance

    def set_point_cloud(self, point_cloud):

        # sets point cloud
        self.point_cloud = point_cloud
        
    def get_point_cloud(self):
        return self.point_cloud


    def distances(self, box_width):
        # Temporary - we should play with this to determine best distance
        return box_width*self.scalar


    def get_persistance_diagram(self):
    # if persistance_diagram has not been calculated, create it
        if self.persistance_diagram != None:
            return self.persistance_diagram
        else:
            # Does fill_rips need it to be a linear array?
            f = d.fill_rips(self.point_cloud, self.skeleton , self.distance)
            m = d.homology_persistence(f)
            diagram = d.init_diagrams(m,f)
            self.persistance_diagram = diagram
            return diagram


    # Generate/save into specified folder name w/ timestamp
    # This saves this object in JSON format in the 'Sections' folder
    def save(self, dir_name):
        # Transform this object into JSON string:
        pcpds = jsonpickle.encode(self)

        with open(os.path.join(dir_name, str(self.cell_id)), 'w') as outfile:
            json.dump(pcpds, outfile)

    # Alternate version of save that requires the dir to be set statically in reference class
    def save(self):
        if ref.get_cur_dir_name() is not None:
            # Transform this object into JSON string:
            pcpds = jsonpickle.encode(self)

            with open(os.path.join(ref.get_cur_dir_name(), str(self.cell_id)), 'w') as outfile:
                json.dump(pcpds, outfile)
        else:
            # TODO: Set up project properly so it is easy to then generate the file for storage properly & set it
            print("ERROR: The current directory has not yet been selected, so section will not be saved.")


# NOTE: Notice the indentation here, these methods are not part of the PCPDS object, but rather
# are to be called implicitly as PCPDS.loadsection(), so they are NOT reliant on the PCPDS object
# already being loaded.

# Loads a PCPDS object from the corresponding JSON file provided it exists
def load_section_dir(dir_name, cell_id):

    with open(os.path.join(dir_name, str(cell_id))) as json_file:

        data = json.load(json_file)
        print(data)
        pcpds = jsonpickle.decode(data)

    # This returns the decoded pcpds object
    return pcpds

# This version of the loading method only requires the cell_id to be passed  in,
# as it uses a preset class reference to the directory. This way, we can load in
# sections from a targeted folder in more loosely coupled fasion.
# It does however require that the folder path be set at some point prior to calling.
def load_section(cell_id):

    if ref.get_cur_dir_name() is not None:
        with open(os.path.join(ref.get_cur_dir_name(), str(cell_id))) as json_file:

            data = json.load(json_file)
            print(data)
            pcpds = jsonpickle.decode(data)

        # This returns the decoded pcpds object
        return pcpds

    else:
        print("ERROR: The current directory has not yet been selected, so no section will be loaded.")
        return None

# Parses cell_ID string into X, Y, & Z touple and returns them.
def get_xyz(cell_id):
    
    # Removes the 1 from the beginning of the string
    cell_id = cell_id[1:]
    
    # Cast cell ID to an int
    xyz = int(cell_id)

    # Checks if the value is zero
    if xyz is 0:
        return (0, 0, 0)

    trunc_val = 10**(int(len(cell_id)/3))

    Z = xyz % trunc_val
    xyz = int(xyz/trunc_val)

    Y = xyz % trunc_val
    xyz = int(xyz/trunc_val)

    X = xyz

    result = (X, Y, Z)
    # Returns a touple of X, Y, & Z
    return result