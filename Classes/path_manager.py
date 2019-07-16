# The PathManager object deals with knowledge of pathing/folder structure

import os
from pathlib import Path

class PathManager:

    def __init__(self):
        print("PathManager loaded.")
        self.ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.collections_dir = "cell_collection"
        self.cur_dir = None

    def set_cur_dir(self, dir_path):
        self.cur_dir = dir_path

    def get_cur_dir(self):
        return self.cur_dir

    def set_cols_dir(self, col_dir):
        self.collections_dir = col_dir

    def get_cols_dir(self):
        return self.collections_dir

    def get_root_dir(self):
        return self.ROOT_DIR

    def get_full_cur_dir_var(self, dir):
        return os.path.join(self.get_root_dir(), self.get_cols_dir(), dir)

    def get_full_cur_dir(self):
        path = os.path.join(self.get_root_dir(), self.get_cols_dir(), self.get_cur_dir())
        if validate_dir(path):
            if is_collection_path():
                return path
            else:
                print("Collection Path appears to have not been set yet.")
        else:
            print("Current directory path is invalid.")
        return False

    def is_collection_path(self):
        collections_path = os.path.join(self.ROOT_DIR, self.collections_dir)
        full_path = os.path.join(self.ROOT_DIR, self.collections_dir, self.cur_dir)
        if full_path is collections_path:
            return False
        else:
            return True

    def validate_dir(self, dir_path):
        if dir_path is None:
            return False
        elif os.path.isdir(dir_path):
            return False
        else:
            return True

    def validate_file(self, file_path):
        if file_path is None:
            print("file @:", file_path, "already exists.")
            return False
        elif os.path.exists(file_path):
            print("file @:", file_path, "already exists.")
            return False
        else:
            return True
