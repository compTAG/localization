from Classes.process_las import ProcessLas
import Classes.PCPDS
from Classes.bottleneck_dist import BottleneckDistances
from Classes.menu import menu as order_menu
from Classes.file_manager import FileManager
from Classes.findign_files import FindingFiles
import numpy as np
import os.path
from datetime import datetime

def main():

    #Have the user input their desired file and partition count
    ff = FindingFiles()
    [partition, filename] = ff.partitions()

    # Create las object and calculate corresponding values
    las_obj = ProcessLas(filename, partition, len(str(partition)))

    # Makes a string of the folder path, os.path.join makes it compatible
    # between macs, windows, and linux
    fm = FileManager()
    dir_name = fm.directory(filename, partition)


    # Check if the final persistence diagram for the las object doesn't exist
    # Check under a given timestamp to avoid multiple same files
    points = ff.return_points(las_obj, int(str(partition) + str(partition) + str(partition)), '.json', '.las', dir_name)

    # Create menu object with num of partitions, .las object, and points dictionary
    m = order_menu(partition, las_obj, points)
    m.test_against_file()


# Do Main
if __name__ == '__main__':
    main()
