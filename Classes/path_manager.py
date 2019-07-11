# The PathManager object deals with knowledge of pathing/folder structure

import os
from pathlib import Path

class PathManager:
    
    def __init__(self):
        print("PathManager loaded.")
        self.ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.collection_dir = "cell_collection"
        self.cur_dir = None
        
    def set_cur_dir(self, dir_path):
        self.cur_dir = dir_path
        
    def get_cur_dir(self):
        return self.cur_dir
    
    def set_col_dir(self, col_dir):
        self.collection_dir = col_dir
        
    def get_col_dir(self):
        return self.collection_dir
    
    def validate_dir(self, dir):
        if dir is None:
            return False
        elif os.path.isdir(dir):
            return False
        else:
            return True