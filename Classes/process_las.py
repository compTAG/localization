from laspy.file import File
from Classes.PCPDS import PCPDS as pcpds
import Classes.file_manager as file_manager
import math
import random
import numpy as np
import os.path
from Classes.menu import menu
import multiprocessing
from Classes.filtrations import Filtration
import time

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

        dimX = max(x_vals) 
        dimY = max(y_vals)
        dimZ = max(z_vals)
        dimensions = (dimX, dimY, dimZ)

        return temp.T, dimensions


    # Returns a random index in the object
    def random_grid(self):

        xRand = random.randint(0, self.partition)
        yRand = random.randint(0, self.partition)
        zRand = 1

        xRand = str(xRand).zfill(self.leading_zeros)
        yRand = str(yRand).zfill(self.leading_zeros)
        zRand = str(zRand).zfill(self.leading_zeros)

        return int('1' + xRand + yRand + zRand)


    # Returns a random index in the object, not on an edge
    def random_grid_edge_case(self):

        xRand = random.randint(1, self.partition - 1)
        yRand = random.randint(1, self.partition - 1)
        zRand = 1

        xRand = str(xRand).zfill(self.leading_zeros)
        yRand = str(yRand).zfill(self.leading_zeros)
        zRand = str(zRand).zfill(self.leading_zeros)

        print("ATTEMPTING RANDOM ID:", int('1' + xRand + yRand + zRand))
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

        # Load data, put list of touples in an array
        in_file = File(self.filename + '.las', mode='r')

        # Import coordinates and change them to manipulative type float32
        x_vals = in_file.X
        y_vals = in_file.Y
        z_vals = in_file.Z

        coords, grid_dimensions = self.__format_data(x_vals,y_vals,z_vals)

        # Dictionary of point cloud coordinates
        points = {'idx':'coords[c]'}
        
        print("\nWould you like to use multi-processing to attempt to speed things up? [0] No. [1] Yes.")
        print("Please do note that using multiprocessing only speeds up this process with larger data sets.")
        multiproc = menu.get_int_input()
        
        # Start timer
        start_time = time.time()
        
        if multiproc:
            print("Multithreading")
            # split up the list by cpu cores avalible
            cores = multiprocessing.cpu_count()
            
            coords_split_amount = round(len(coords)/cores)
            #print("COORDS SPLIT AMOUNT:", coords_split_amount, "LEN(COORDS):", len(coords), " = CORES:", cores)
            
            chunks = [coords[x:x+coords_split_amount] for x in range(0, len(coords), coords_split_amount)]
            #print("CHUNKS:", len(chunks))
            
            # Sets up the manager to be able to return values properly to the points dict.
            manager = multiprocessing.Manager()
            points = manager.dict()
            
            # Sets up the process
            for chunk in chunks:
                # TODO: Change to use pool
                process = multiprocessing.Process(target=self.split_pointcloud, args=(chunk, points))
                process.start()
                process.join()
                process.terminate()
        else:
            print("Not multi threading.")
            self.split_pointcloud(coords, points, count=True)
            points.pop('idx')

        menu.progress(1, 1, ("Processing points completed."))
        print("\n")
        print("Processing points completed in: ", str(time.time() - start_time))
        
        # Creates a pcpds object for each idx and stores it's respective
        # point cloud in it before saving the file.
        tracker = 0

        # print("STATS:\nLength:",len(points), "\nPoints:",points)

        #pcpds_num = len(points)
        individual_dimensions = (grid_dimensions[0]/self.partition, grid_dimensions[1]/self.partition, grid_dimensions[2]/self.partition)

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

    def split_pointcloud(self, coords, points, count=False):
        # Split up the list into sections depending on how many cpus are avalible
        for c,_  in enumerate(coords):
            x = math.floor(coords[c][0] * self.partition)
            y = math.floor(coords[c][1] * self.partition)

            x = str(x).zfill(self.leading_zeros)
            y = str(y).zfill(self.leading_zeros)
            z = str(1).zfill(self.leading_zeros)

            idx = int('1' + x + y + z)

            # Make a dictionary with each [idx], if it already exists, append the coord
            try:
                points[idx]
            except:
                points[idx] = coords[c]
            else:
                points[idx] = np.vstack((points[idx],coords[c]))
            # Keeps track of the progress of dividing up points
            if count:
                pass
                #menu.progress(c, len(coords), ("Processing point: "+str(idx)+"..."))