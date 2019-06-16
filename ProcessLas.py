from laspy.file import File
import PCPDS as section
import math
import numpy as np

def input_las():

    #Load data, put list of touples in an array
    #TODO?: Change to get file off server
    inFile = File('test.las', mode='r')

    Xvals = inFile.X
    Yvals = inFile.Y
    Zvals = inFile.Z
    Xvals.dtype = "float32"
    Yvals.dtype = "float32"
    Zvals.dtype = "float32"

    Coords = np.array([Xvals,Yvals,Zvals])
    Points = [] #PCPDS array of point clouds in each section

    #TODO: Sort Coords? Overwirte operator for x low to high, then y, then z

    #Set width, height, and depth
    maxX = max(Xvals)
    minX = min(Xvals)
    maxY = max(Yvals)
    minY = min(Yvals)
    maxZ = max(Zvals)
    minZ = min(Zvals)

    #Get dimensions
    dimX = maxX - minX
    dimY = maxY - minY
    dimZ = maxZ - minZ

    #TEMP hardcoded window dim. in perc
    windowSize = .20
    iX = dimX * windowSize
    iY = dimY * windowSize
    iZ = dimZ * windowSize

    #Amount of "cubes" in the grid split - ie. 125 grids with .20 window size
    #gridSize = (1.0 / windowSize)**3.0
    dim = math.ceil(1.0 / windowSize)

    #Takes into account the digits as to not get confused in the string of x y z
    leadingZeros = len(str(dim))
    #Iterate over the x, y, z combinations to make the grid Sections
    #then save them in a PCPDS at Points[concatenate x y z] where i < gridSize
    for c  in Coords:

        #X/Y/ZVals needs to be changed to the X/Y/Z identifiers
        x = math.floor(c.Xvals / iX)
        y = math.floor(c.Yvals / iY)
        z = math.floor(c.Zvals / iZ)

        x = format(x, str(leadingZeros))
        y = format(y, str(leadingZeros))
        z = format(z, str(leadingZeros))

        idx = int(str(x) + str(y) + str(z))
        Points[idx].append(c)

    #Iterate over concatenations of x, y, z to find all point clouds
    x = 0
    # used in rips distances
    rip_dist = iX * iY * iZ / 2
    for x in dim:
        y = 0
        for y in dim:
            z = 0
            for z in dim:

                x = format(x, str(leadingZeros))
                y = format(y, str(leadingZeros))
                z = format(z, str(leadingZeros))

                idx = int(str(x) + str(y) + str(z))
                # are the x, y, and z here each from a 'cube' of the pointcloud?
                # if so, the following code should work to save them to pcpds


                # TO DO:  how to make differently named objects iteratively using idx?
                #cube = PCPDS(idx)
                #cube.generate_persistance_diagram(rip_dist)
                #cube.save()

                #not sure what this does
                section.generate_persistance_diagram(Points[idx])
    #Save Point clouds with PCPDS

    # Temp test for pcpds
    test = section.PCPDS(1,1,1)
    test.save()

    temp = section.load_section(1,1,1)

    # temp now has the ability to call methods from the PCPDS object that has been loaded
