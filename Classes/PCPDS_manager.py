import Classes.file_manager as fm
from Classes.path_manager import PathManager as pm
from datetime import datetime
import os.path
import random

# This class deals with loading/fetching of PCPDS objects specifically

class PCPDS_Manager:

    # TODO: move the methods for selecting pcpds objects from a directory to here.

    def __init__(self):

        self.path_manager = pm()

        self.pcpds_collection = []

        self.load_collection()

    def load_collection(self):

        collection_path = self.path_manager.get_cur_dir()
        if collection_path is not None and self.path_manager.validate_dir(collection_path):
            self.pcpds_collection.clear()
            self.pcpds_collection = fm.find_files(collection_path, '.json')


    def set_collection_dir(self, dir):

        if dir is not None:
            path = self.path_manager.get_full_cur_dir_var(dir)
            if self.path_manager.validate_dir(path):
                self.path_manager.set_cur_dir(path)
                print("Collection path set to:", path)
                return True
            else:
                print("Collection Path", path, ", is Invalid.")
                return False


    def get_collection_dir(self):

        result = self.get_path_manager().get_full_cur_dir()
        return result

    # Fetches a pcpds with a specified cell_ID
    def get_pcpds(self, cell_ID):
        dir = self.path_manager.get_full_cur_dir()

        pcpds = fm.load(os.path.join(dir, str(cell_ID) +'.json'))
        return pcpds

    # Fetches a random pcpds object from the idx specified
    def get_random_pcpds_idx(self, random_idx):
        # TODO: have a check for None and index out of bounds in here
        dir = self.path_manager.get_full_cur_dir()

        random_pcpds = fm.load(os.path.join(dir, str(random_idx) +'.json')) #
        return random_pcpds

    def get_random_pcpds(self):
        dir = self.path_manager.get_full_cur_dir()
        file_name = fm.get_random_file(dir, '.json')
        random_pcpds = fm.load(os.path.join(dir, file_name))
        return random_pcpds

    # Checks that the currently selected collection directory exists and is a valid path
    def verify_col_dir(self):

        return self.path_manager.validate_dir(self.path_manager.get_cur_dir())

    # Generates a collection file given the name of the current las file being used, and the partition count.
    def generate_collection(self, filename, partition):

        dir_name = str(filename + '_' + str(partition))
        self.path_manager.set_cur_dir(dir_name)
        dir_name = self.path_manager.get_full_cur_dir_var(dir_name)

        fm.make_folder(dir_name)
        return dir_name


    # Pass in a filename in the collection directory, and get it's supposed full path
    def get_file_path(self, filename):

        path = self.path_manager.get_full_cur_dir()
        if path is not False:
            file_path = os.path.join(path, filename)
            if self.path_manager.validate_file(file_path):
                return file_path
            else:
                print("File name specified not found in directory: ", path)
        else:
            print("Collection path appears to not be set.")
        return False


    # Can grab the path manager to make changes to it such as changing the collections directory.
    def get_path_manager(self):

        return self.path_manager

    def gen_idx(self, x, y, leading_zeros):
        print("Find index X:",x , " Y:", y)
        # Cast x & y to ints perhaps?
        x = str(x).zfill(leading_zeros)
        y = str(y).zfill(leading_zeros)
        z = str(1).zfill(leading_zeros)

        return int('1' + x + y + z)