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
            return true
        else:
            return false

    def randomGrid(self):

        xRand = random.randint(0,dim)
        yRand = random.randint(0,dim)
        zRand = random.randint(0,dim)

        xRand = format(xRand, str(self.leadingZeros))
        yRand = format(yRand, str(self.leadingZeros))
        zRand = format(zRand, str(self.leadingZeros))

        return = int(str(xRand) + str(yRand) + str(zRand)

    def inputLas(self):

        #Load data, put list of touples in an array
        #TODO?: Change to get file off server
        inFile = File(self.filename, mode='r')

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

            x = format(x, str(self.leadingZeros))
            y = format(y, str(self.leadingZeros))
            z = format(z, str(self.leadingZeros))

            idx = int(str(x) + str(y) + str(z))
            print(idx)


            # logic here is very shoddy
            # the idea is we need to make a dictionary entry for each idx if it determine
            # but we need to append the new cord to that entry if it exists
            try:
                Points[idx]
            except:
                Points[idx] = Coords[c]
            else:
                Points[idx] = np.concatenate((Points[idx],Coords[c]))


        #Iterate over concatenations of x, y, z to find all point clouds

        # creates parallelograms dictionary to give PCPDS object from idx
        parallelograms = {'idx':'PCPDS(idx)'}
        x = 0
        # used in rips
        print("Debug")
        rip_dist = iX * iY * iZ / 2
        for x in range(self.dim):
            y = 0
            for y in range(self.dim):
                z = 0
                for z in range(self.dim):

                    x = str(x) + str(self.leadingZeros)
                    y = str(y) + str(self.leadingZeros)
                    z = str(z) + str(self.leadingZeros)

                    idx = int(x + y + z)
                    try:
                        print(idx)

                        # assigns a new entry to the parallelograms dictionary for each idx generated
                        parallelograms[idx] = section.PCPDS(idx, str(idx) + ".ourfiletype", rip_dist)
                        # adds points to pcpds object
                        parallelograms[idx].set_point_cloud(Points[idx])
                        #generates a persistance diagram for that object
                        parallelograms[idx].get_persistance_diagram()
                        # pickles the object
                        parallelograms[idx].save()
                        print(parallelograms)

                #section.generate_persistance_diagram(Points[idx])
    #Save Point clouds with PCPDS

    # Temp test for pcpds
    test = section.PCPDS(1,1,1)
    test.save()

    temp = section.load_section(1,1,1)

    # temp now has the ability to call methods from the PCPDS object that has been loaded
