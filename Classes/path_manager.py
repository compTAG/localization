# The PathManager object deals with knowledge of pathing/folder structure

import os
from pathlib import Path

class PathManager:
    
    def __init__(self):
        print("PathManager loaded.")
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.cur_dir = None
        
    def set_cur_dir(dir_path):
        self.cur_dir = dir_path
        
    def get_cur_dir():
        # TODO: Check if cur_dir is None, or an invalid path, and then ask them to re-enter a valid path.
        pass
        
    # TODO: Move functionality from PCPDS to here
    
        