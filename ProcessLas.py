from laspy.file import File
import PCPDS as section
import math
import numpy as np

def input_las(filename, dim):

    #Load data, put list of touples in an array
    #TODO?: Change to get file off server
    inFile = File(concatenate(filename, '.las'), mode='r')

    Xvals = inFile.X
    Yvals = inFile.Y
    Zvals = inFile.Z
    Xvals.dtype = "float32"
    Yvals.dtype = "float32"
    Zvals.dtype = "float32"

    temp = np.array([Xvals,Yvals,Zvals])
    Coords = temp.T

    # moved points down - Luke

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


    # Proposed addition of options in 1d splitting - Luke
    windowSize = 1/dim

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

    # changed to a dictionary
    Points = {'idx':'Coords[c]'}
    for c,_  in enumerate(Coords):

        #X/Y/ZVals needs to be changed to the X/Y/Z identifiers

        x = math.floor((Coords[c][0] - minX)/ iX)
        y = math.floor((Coords[c][1] - minY)/ iY)
        z = math.floor((Coords[c][2] - minZ)/ iZ)

        x = format(x, str(leadingZeros))
        y = format(y, str(leadingZeros))
        z = format(z, str(leadingZeros))

        idx = int(str(x) + str(y) + str(z))
        print(idx)

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
    for x in range(dim):
        y = 0
        for y in range(dim):
            z = 0
            for z in range(dim):

                x = format(x, str(leadingZeros))
                y = format(y, str(leadingZeros))
                z = format(z, str(leadingZeros))

                idx = int(str(x) + str(y) + str(z))
                try:
                    points[idx]
                except:
                    continue
                else:
                    # assigns a new entry to the parallelograms dictionary for each idx generated
                    parallelograms[idx] = section.PCPDS()
                    # sends the points from idx to
                    parallelograms[idx].set_point_cloud(Points[idx])
                    #generates a persistance diagram for that object
                    parallelograms[idx].generate_persistance_diagram(rip_dist)
                    # pickles the object
                    parallelograms[idx].save()


                #section.generate_persistance_diagram(Points[idx])
    #Save Point clouds with PCPDS

    # Temp test for pcpds
    test = section.PCPDS(1,1,1)
    test.save()

    temp = section.load_section(1,1,1)

    # temp now has the ability to call methods from the PCPDS object that has been loaded
