import Classes.file_manager as file_manager

# This class deals with loading/fetching of PCPDS objects specifically

class PCPDS_Manager:
    
    def __init__(self, collection_dir):
        self.col_dir = collection_dir
        self.pcpds_collection = []
        self.load_collection()
        
    def load_collection(self):
        # TODO: try to load in every file from that directory into a list of PCPDS object names
        self.load_collection.clear()
        self.pcpds_collection = file_manager.find_files(self.col_dir)
        
    def set_col_dir(self, dir):
        self.col_dir = dir
        
    def get_col_dir(self):
        return self.col_dir
    
    def verify_col_dir():
        # TODO: Verify the folder exists
        pass