import readLas
import PCPDS as section

def main():

    #Load data, put list of touples in an array
    Coords = []
    #Sort Coords, overwirte operator for x low to high, then y, then z

    #Get dimensions

    #Set width, height, and depth
    maxX =
    minX =
    maxY =
    minY =
    maxZ =
    minZ =

    #TEMP hardcoded window dim. in perc
    windowSize = .10
    iX, iY, iZ = windowSize

    #Iterate through array, section off grid

    # Temp test for pcpds
    test = section.PCPDS(1,1,1)
    test.save()

    temp = section.load_section(1,1,1)

    # temp now has the ability to call methods from the PCPDS object that has been loaded

if __name__ == '__main__':
    main()
