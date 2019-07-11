import Classes.file_manager as fm
import Classes.path_manager as pm

# This class deals with loading/fetching of PCPDS objects specifically

class PCPDS_Manager:
    
    def __init__(self, collection_dir):
        self.col_dir = collection_dir
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
    
    def verify_col_dir(self):
        return self.path_manager.validate_dir(self.col_dir)