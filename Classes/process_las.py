from laspy.file import File
from Classes.PCPDS import PCPDS as pcpds
import Classes.file_manager as file_manager
import math
import random
import numpy as np
import os.path
from Classes.menu import menu
from Classes.filtrations import Filtration

class ProcessLas:

    def __init__(self, filename, partition):

        # The name of the file being processed
        self.filename = filename

        # The amount of grids on the x y and z axis
        self.partition = partition

        #Takes into account the digits as to not get confused in the string of x y z
        self.leading_zeros = len(str(partition))


    # Format data between 0 and 1
    def __format_data(self, x_vals, y_vals, z_vals):

        # Move data
        minx = min(x_vals)
        miny = min(y_vals)
        minz = min(z_vals)
        x_vals = x_vals - minx
        y_vals = y_vals  - miny
        z_vals = z_vals  - minz

        # Scale data between [0,1]
        temp = np.array([max(x_vals),max(y_vals),max(z_vals)])
        scale_factor = 1 / max(temp)
        x_vals = x_vals  * scale_factor
        y_vals = y_vals  * scale_factor
        z_vals = z_vals  * scale_factor
        temp = np.array([x_vals,y_vals,z_vals])

        dimX = temp[0] - minx
        dimY = temp[1] - miny
        dimZ = temp[2] - minz
        dimensions = (minx, miny, minz)

        return temp.T, dimensions


    # Returns a random index in the object
    def random_grid(self):

        xRand = random.randint(0, self.partition)
        yRand = random.randint(0, self.partition)
        zRand = 1

        xRand = str(xRand).zfill(self.leading_zeros)
        yRand = str(yRand).zfill(self.leading_zeros)
        zRand = str(zRand)

        return int('1' + xRand + yRand + zRand)


    # Returns an index given from the user
    def find_index(self, x, y):

        x = str(x).zfill(self.leading_zeros)
        y = str(y).zfill(self.leading_zeros)
        z = str(1)

        return int('1' + x + y + z)


    # Read the file and split it into partitions and create pcpds objects of
    # each partition, returns the dictionary of pcpds objects
    def input_las(self, path):

        #Load data, put list of touples in an array
        in_file = File(self.filename + '.las', mode='r')

        # Import coordinates and change them to manipulative type float32
        x_vals = in_file.X
        y_vals = in_file.Y
        z_vals = in_file.Z

        coords, grid_dimensions = self.__format_data(x_vals,y_vals,z_vals)

        # Dictionary of point cloud coordinates
        points = {'idx':'coords[c]'}

        for c,_  in enumerate(coords):

            x = math.floor(coords[c][0] * self.partition)
            y = math.floor(coords[c][1] * self.partition)

            x = str(x).zfill(self.leading_zeros)
            y = str(y).zfill(self.leading_zeros)
            z = str(1)

            idx = int('1' + x + y + z)

            # Make a dictionary with each [idx], if it already exists, append the coord
            try:
                points[idx]
            except:
                points[idx] = coords[c]
            else:
                points[idx] = np.vstack((points[idx],coords[c]))
            # Keeps track of the progress of dividing up points
            menu.progress(c, len(coords), ("Processing point: "+str(idx)+"..."))

        menu.progress(1, 1, ("Processing points completed."))
        print("\n")
        
        # Creates a pcpds object for each idx and stores it's respective
        # point cloud in it before saving the file.
        points.pop('idx')
        tracker = 0

        pcpds_num = len(points)
        individual_dimensions = (grid_dimensions[0]/pcpds_num, grid_dimensions[1]/pcpds_num, grid_dimensions[2]/pcpds_num)
        
        for id in points:
            temp = pcpds(id, individual_dimensions)

            temp.set_point_cloud(points[id])
            
            # Generates and sets the persistance diagram
            # temp = Filtration.get_rips_diagram(temp)

            # print('diagram set')
            file_manager.save(temp, path, id)

            # Keeps track of the PCPDS objects being generated
            menu.progress(tracker, len(points), ("Processing PCPDS object for idx: "+str(id)))
            tracker = tracker + 1
            
        menu.progress(1, 1, ("Processing PCPDS files completed."))
        print("\n")
