# This test file's purpose is to show that the process_las class is capable of
# splitting up a LAS file into 3D 'sections'. It is also used to verify integrity after changing code.

import unittest
from Classes.process_las import ProcessLas as pl

class Test_Splitting(unittest.TestCase):
    def set_up(self, partition):
        # Pass in the amount of partitions we want to split it up into
        self.process = pl("small_test", partition)
        
        # TODO: write Test cases for input_las