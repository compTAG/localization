from laspy.file import File
import Classes.PCPDS as section
import math
import random
import numpy as np
import os.path

class ProcessLas:

    def __init__(self, filename, partition, leading_zeros):
        # The name of the file being processed
        self.filename = filename
        # The amount of grids on the x y and z axis
        self.partition = partition
        #Takes into account the digits as to not get confused in the string of x y z
        self.leading_zeros = leading_zeros


    # Returns a boolean if a file.ext exists in dir_name/
    def check_file(self, idx, ext, dir_name):

        temp = self.filename + str(idx) + str(ext)
        if dir_name == None:
            temp = self.filename + str(ext)
            exists = os.path.isfile(temp)
        else:
            dir_name = str('Sections/PCPDS/' + dir_name + '/')
            exists = os.path.isfile(dir_name + temp + ext)

        if exists:
            return True
        else:
            return False


    # Returns a random index in the object
    def random_grid(self):

        xRand = random.randint(0, self.partition)
        yRand = random.randint(0, self.partition)
        zRand = random.randint(0, self.partition)

        xRand = str(xRand).zfill(self.leading_zeros)
        yRand = str(yRand).zfill(self.leading_zeros)
        zRand = str(zRand).zfill(self.leading_zeros)

        return int('1' + xRand + yRand + zRand)

    # Returns an index given from the user
    def find_index(self, x, y, z):

        x = str(x).zfill(self.leading_zeros)
        y = str(y).zfill(self.leading_zeros)
        z = str(z).zfill(self.leading_zeros)

        return int('1' + x + y + z)


    # Hash function that returns the index of the x y and z values
    def __hash_it(self, coord, max_par, min_par):
        h = math.floor((coord - min_par)/ ((max_par - min_par) / self.partition))
        return str(h).zfill(self.leading_zeros)


    # Read the file and split it into partitions and create pcpds objects of
    # each partition, returns the dictionary of pcpds objects
    def input_las(self):

        #Load data, put list of touples in an array
        #TODO?: Change to get file off server
        in_file = File(self.filename + '.las', mode='r')

        # Import coordinates and change them to manipulative type float32
        x_vals = in_file.X
        y_vals = in_file.Y
        z_vals = in_file.Z
        x_vals.dtype = "float32"
        y_vals.dtype = "float32"
        z_vals.dtype = "float32"

        temp = np.array([x_vals,y_vals,z_vals])
        coords = temp.T

        #Set width, height, and depth
        max_x = max(x_vals)
        min_x = min(x_vals)
        max_y = max(y_vals)
        min_y = min(y_vals)
        max_z = max(z_vals)
        min_z = min(z_vals)

        # Dictionary of point cloud coordinates
        points = {'idx':'coords[c]'}
        for c,_  in enumerate(coords):

            x = self.__hash_it(coords[c][0], min_x, max_x)
            y = self.__hash_it(coords[c][1], min_y, max_y)
            z = self.__hash_it(coords[c][2], min_z, max_z)

            idx = int('1' + x + y + z)
            print(idx)

            # Make a dictionary with each [idx].
            # If it already exists, append the coord
            try:
                points[idx]
            except:
                points[idx] = coords[c]
            else:
                points[idx] = np.concatenate((points[idx],coords[c]))

        # Creates parallelograms dictionary to give PCPDS object from idx
        parallelograms = {'idx':'PCPDS(idx)'}

        # Used in rips
        print("Debug")
        iX = (max_x - min_x) / self.partition
        iY = (max_y - min_y) / self.partition
        iZ = (max_z - min_z) / self.partition
        rip_dist = iX * iY * iZ / 2

        # Iterate over concatenations of x, y, z to find all point clouds
        x = 0
        for x in range(self.partition):
            y = 0
            for y in range(self.partition):
                z = 0
                for z in range(self.partition):

                    # Leave format() if you just add leadingZeros to the encode
                    # of x y z, it defeats the point of leadingZeros
                    x = str(x).zfill(self.leading_zeros)
                    y = str(y).zfill(self.leading_zeros)
                    z = str(z).zfill(self.leading_zeros)

                    idx = int('1' + x + y + z)
                    try:
                        #debug
                        print(idx)

                        # Assign a new entry to the parallelograms dict for each idx generated
                        parallelograms[idx] = section.PCPDS(idx, str(idx) + ".json", rip_dist) #where ** is file ext

                        # Add points to PCPDS object
                        parallelograms[idx].set_point_cloud(points[idx])

                        # Generate a persistance diagram for that object
                        parallelograms[idx].get_persistance_diagram()

                        # Pickle the object
                        # parallelograms[idx].save(dir_name)

                        # Temp check
                        print(idx)
                    except:
                        pass

        return parallelograms

                #section.generate_persistance_diagram(points[idx])