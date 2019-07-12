import Classes.file_manager as fm
import Classes.path_manager as pm
from datetime import datetime
import os.path

# This class deals with loading/fetching of PCPDS objects specifically

class PCPDS_Manager:
    
    def __init__(self):
        self.pcpds_collection = []
        self.load_collection()
        self.path_manager = pm()
        
    def load_collection(self):
        self.load_collection.clear()
        self.pcpds_collection = fm.find_files(self.col_dir)
        
    def set_col_dir(self, dir):
        self.col_dir = dir
        
    def get_col_dir(self):
        return self.col_dir
    
    # Can grab the path manager to make changes to it such as changing the collections directory.
    def get_path_manager(self):
        return self.path_manager
    
    def verify_col_dir(self):
        return self.path_manager.validate_dir(self.col_dir)
    
    def generate_collection(self, filename, partition):
        dir_name = str(filename + '_' + str(partition) + '_' + datetime.today().strftime('%Y-%m-%d'))
        dir_name = os.path.join(self.path_manager.get_root_dir(), self.path_manager.get_cols_dir(), dir_name)
        
        fm.make_folder(dir_name)
        self.path_manager.set_cur_dir(dir_name)
