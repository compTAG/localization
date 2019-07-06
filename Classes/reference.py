from os import walk

class reference:
    
    # This class serves as a means of statically referencing variables so they 
    # don't have to be passed around everywhere, but only set once here instead.
    
    # Variables that will serve to be set statically for looser coupling
    cur_dir_name = None
    
    @staticmethod
    def set_cur_dir_name(dir_name):
        reference.cur_dir_name = dir_name
        
    @staticmethod
    def get_cur_dir_name():
        return reference.cur_dir_name
    
    # Generic functions that might be used anywhere
    
    # Returns a list of filenames in a specified directory
    def get_files_in_folder(folder):
        
        _,_, filenames = walk(folder).next()
        return filenames
    
    # Returns a list of filenames in the currently selected directory
    def get_files_in_folder():
        
        if reference.cur_dir_name is not None:
            _,_, filenames = walk(reference.cur_dir_name).next()
            return filenames
        
        print("Reference to current directory not set.")
        return None