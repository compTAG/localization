from laspy.file import File
from Classes.PCPDS import PCPDS as pcpds
import Classes.file_manager as file_manager
import math
import random
import numpy as np
import os.path
from Classes.menu import menu

class ProcessLas:

    def __init__(self, filename, partition):

        # The name of the file being processed
        self.filename = filename
        # The amount of grids on the x y and z axis
        self.partition = partition
        #Takes into account the digits as to not get confused in the string of x y z
        self.leading_zeros = len(str(partition))


    def __format_data(self, x_vals, y_vals, z_vals):
        # move data
        minx = min(x_vals)
        miny = min(y_vals)
        minz = min(z_vals)
        x_vals = x_vals - minx
        y_vals = y_vals  - miny
        z_vals = z_vals  - minz
        #scale data between [0,1]
        temp = np.array([max(x_vals),max(y_vals),max(z_vals)])
        scale_factor = 1 / max(temp)
        x_vals = x_vals  * scale_factor
        y_vals = y_vals  * scale_factor
        z_vals = z_vals  * scale_factor
        temp = np.array([x_vals,y_vals,z_vals])
        return temp.T


    # Returns a random index in the object
    def random_grid(self):

        xRand = random.randint(0, self.partition)
        yRand = random.randint(0, self.partition)
        zRand = 1

        xRand = str(xRand).zfill(self.leading_zeros)
        yRand = str(yRand).zfill(self.leading_zeros)
        zRand = str(zRand).zfill(self.leading_zeros)

        return int('1' + xRand + yRand + zRand)


    # Returns an index given from the user
    def find_index(self, x, y):

        x = str(x).zfill(self.leading_zeros)
        y = str(y).zfill(self.leading_zeros)
        z = str(1).zfill(self.leading_zeros)

        return int('1' + x + y + z)


    # Read the file and split it into partitions and create pcpds objects of
    # each partition, returns the dictionary of pcpds objects
    def input_las(self, path):

        #Load data, put list of touples in an array
        #TODO?: Change to get file off server
        in_file = File(self.filename + '.las', mode='r')

        # Import coordinates and change them to manipulative type float32
        x_vals = in_file.X
        y_vals = in_file.Y
        z_vals = in_file.Z

        coords = self.__format_data(x_vals,y_vals,z_vals)
        #Set width, height, and depth
#        max_x = max(x_vals)
#        min_x = min(x_vals)
#        max_y = max(y_vals)
#        min_y = min(y_vals)
#        max_z = max(z_vals)
#        min_z = min(z_vals)

        # Dictionary of point cloud coordinates
        points = {'idx':'coords[c]'}

#        iX = (max_x - min_x) / self.partition
#        iY = (max_y - min_y) / self.partition
#        iZ = (max_z - min_z) / self.partition
#        rip_dist = iX * iY * iZ / 2

        for c,_  in enumerate(coords):

            x = 1 #math.floor((coords[c][0])
            y = 1 #math.floor((coords[c][1])
            z = 1
            idx = int('1' + str(x) + str(y) + str(z))

            # Make a dictionary with each [idx].
            # If it already exists, append the coord
            try:
                points[idx]
            except:
                points[idx] = coords[c]
            else:
                points[idx] = np.vstack((points[idx],coords[c]))
            # Keeps track of the progress of dividing up points
            menu.progress(c, len(coords), ("Processing point: "+str(points[idx])+"..."))

        # Creates a pcpds object for each idx and stores it's respective point cloud in it before saving the file.
        points.pop('idx')
        for id in points:
            print(id)
            temp = pcpds(id)
            print('pcpds set')
            temp.set_point_cloud(points[id])
            # TODO: contemplate seperating the generation of persistance diagrams to another area/file for reducing time complexity here
            print('pointcloud set')
            temp.generate_persistance_diagram()
            print('diagram set')
            file_manager.save(temp, path, id)
            print('saved')

            # Keeps track of the PCPDS objects being generated
            menu.progress(id.index, len(points), "Processing PCPDS object for idx: "+id)
