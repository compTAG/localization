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

    #Sort Coords, overwirte operator for x low to high, then y, then z

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

    #Iterate through array, section off grid
    for c in Coords:


    # Temp test for pcpds
    test = section.PCPDS(1,1,1)
    test.save()

    temp = section.load_section(1,1,1)

    # temp now has the ability to call methods from the PCPDS object that has been loaded

if __name__ == '__main__':
    main()
