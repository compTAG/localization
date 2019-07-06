from os import walk
import os

class reference:
    
    # This class serves as a means of statically referencing variables so they 
    # don't have to be passed around everywhere, but only set once here instead.
    
    # Variables that will serve to be set statically for looser coupling
    cur_dir_name = None
    
    # TO NOTE: When setting the current directory name, be sure to make it the full path
    @staticmethod
    def set_cur_dir_name(dir_name):
        reference.cur_dir_name = dir_name
        
    @staticmethod
    def get_cur_dir_name():
        return reference.cur_dir_name
    
    # Generic functions that might be used anywhere
    
    # Returns a list of filenames in a specified directory
    def get_files_in_folder(dir):
        
        files = []
        for (dirpath, dirnames, filenames) in walk(dir):
            files.extend(filenames)
            break
        
        return files
    
    # Returns a list of filenames in the currently selected directory
    def get_files_in_folder():
        
        if reference.cur_dir_name is not None:
            files = []
            for (dirpath, dirnames, filenames) in walk(reference.cur_dir_name):
                files.extend(filenames)
                break
            return files
        
        print("Reference to current directory not set.")
        return None