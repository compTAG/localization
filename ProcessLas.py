from laspy.file import File
import PCPDS as section
import math
import random
import numpy as np

class ProcessLas:

    def __init__(self, filename, dim, leadingZeros):
        # The name of the file being processed
        self.filename = filename
        # The amount of grids on the x y and z axis
        self.dim = dim
        #Takes into account the digits as to not get confused in the string of x y z
        self.leadingZeros = leadingZeros

    def checkFile(self, idx, ext):

        temp = concatenate(self.filename, idx, ext)
        exists = os.path.isfile(concatenate('/path/to/', temp, **)) #where ** is file ext
        if exists:
            return True
        else:
            return False

    def randomGrid(self):

        xRand = random.randint(0, self.dim)
        yRand = random.randint(0, self.dim)
        zRand = random.randint(0, self.dim)

        xRand = str(xRand).zfill(self.leadingZeros)
        yRand = str(yRand).zfill(self.leadingZeros)
        zRand = str(zRand).zfill(self.leadingZeros)

        return = int(xRand + yRand + zRand)

    def inputLas(self):

        #Load data, put list of touples in an array
        #TODO?: Change to get file off server
        inFile = File(self.filename + '.las', mode='r')

        # Import coordinates and change them to manipulative type float32
        xVals = inFile.X
        yVals = inFile.Y
        zVals = inFile.Z
        xVals.dtype = "float32"
        yVals.dtype = "float32"
        zVals.dtype = "float32"

        temp = np.array([xVals,yVals,zVals])
        Coords = temp.T

        # moved points down - Luke

        #Set width, height, and depth
        maxX = max(xVals)
        minX = min(xVals)
        maxY = max(yVals)
        minY = min(yVals)
        maxZ = max(zVals)
        minZ = min(zVals)

        # Proposed addition of options in 1d splitting - Luke

        iX = (maxX - minX) * self.dim
        iY = (maxY - minY) * self.dim
        iZ = (maxZ - minZ) * self.dim

        # changed to a dictionary
        Points = {'idx':'Coords[c]'}
        for c,_  in enumerate(Coords):


            x = math.floor((Coords[c][0] - minX)/ iX)
            y = math.floor((Coords[c][1] - minY)/ iY)
            z = math.floor((Coords[c][2] - minZ)/ iZ)

            x = str(x).zfill(self.leadingZeros)
            y = str(y).zfill(self.leadingZeros)
            z = str(z).zfill(self.leadingZeros)

            idx = int(x + y + z)
            print(idx)

            # Make a dictionary with each [idx].
            # If it already exists, append the coord
            try:
                Points[idx]
            except:
                Points[idx] = Coords[c]
            else:
                Points[idx] = np.concatenate((Points[idx],Coords[c]))

        # Creates parallelograms dictionary to give PCPDS object from idx
        parallelograms = {'idx':'PCPDS(idx)'}

        # Used in rips
        print("Debug")
        rip_dist = iX * iY * iZ / 2

        # Iterate over concatenations of x, y, z to find all point clouds
        x = 0
        for x in range(self.dim):
            y = 0
            for y in range(self.dim):
                z = 0
                for z in range(self.dim):

                    # Leave format() if you just add leadingZeros to the encode
                    # of x y z, it defeats the point of leadingZeros
                    x = str(x).zfill(self.leadingZeros)
                    y = str(y).zfill(self.leadingZeros)
                    z = str(z).zfill(self.leadingZeros)

                    idx = int(x + y + z)
                    try:
                        print(idx)

                        # Assign a new entry to the parallelograms dict for each idx generated
                        parallelograms[idx] = section.PCPDS(idx, str(idx) + "**", rip_dist) #where ** is file ext

                        # Add points to PCPDS object
                        parallelograms[idx].set_point_cloud(Points[idx])

                        # Generate a persistance diagram for that object
                        parallelograms[idx].get_persistance_diagram()

                        # Pickle the object
                        parallelograms[idx].save()

                        # Temp check
                        print(parallelograms)

        return parallelograms

                #section.generate_persistance_diagram(Points[idx])
