from laspy.file import File
import PCPDS as section

def main():

    #Load data, put list of touples in an array
    inFile = File('test.las', mode='r')

    Xvals = inFile.X
    Yvals = inFile.Y
    Zvals = inFile.Z
    Xvals.dtype = "float32"
    Yvals.dtype = "float32"
    Zvals.dtype = "float32"

    Coords = np.array([Xvals,Yvals,Zvals])
    Points = [] #PCPDS array of point clouds in each section

    #Sort Coords? Overwirte operator for x low to high, then y, then z

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
    windowSize = .10
    iX, iY, iZ = windowSize

    #Amount of "cubes" in the grid split
    (1.0 / windowSize)**3.0 = gridSize
    i = 0

    #Iterate through array, section off grid
    for c in Coords:
        #Iterate over the x, y, z combinations to make the grid Sections
        #then save them in a PCPDS at Points[i] where i > gridSize

    # Temp test for pcpds
    test = section.PCPDS(1,1,1)
    test.save()

    temp = section.load_section(1,1,1)

    # temp now has the ability to call methods from the PCPDS object that has been loaded

if __name__ == '__main__':
    main()
