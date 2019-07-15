import unittest
from Classes.PCPDS_manager import PCPDS_Manager as pm
import os.path

class Manager_Tests(unittest.TestCase):
    
    def set_up(self):
        pcpds_manager = pm()
        pcpds_manager.get_path_manager.set_cols_dir(os.path.join("Unit_Tests","test_collections"))
        
        return 
    
    # TODO: Make unit test cases for the PCPDS_manager, making sure all of it's functions
    # Work as intended, along side the path & file managers.
    def test_pcpds_manager(self):
        pass