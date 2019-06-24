import ProcessLas
import PCPDS
from DoRips import BottleneckDistances
import numpy as np
import os

def main():

    again = Ture
    while again == True:

        #Have the user input their desired file and dim count
        dim = 0
        while (dim%1) != 0:
            dim = int(input("Enter Partition Count (1D): "))
            if (dim%1) != 0:
                print('Please enter a whole number.')
        filename = input("Enter the name of the file you'd wish to import: ")

        # Create las object and calculate corresponding values
        lasObj = ProcessLas(filename, dim, len(str(dim)))
        idx = int(str(test) + str(test) + str(test))

        points = null
        # Check if the final persistence diagram for the las object doesn't exist
        # Check under a given timestamp to avoid multiple same files
        if !ProcessLas.checkFile(lasObj, idx, '**'): #Where ** is the ext of PDs
            #Check if the file exists
            if ProcessLas.checkFile(lasObj, null, '.las'):
                # Saves the persistence diagrams of each grid
                # and returns the dict of PCPDS
                points = ProcessLas.inputLas(lasObj)

            else:
                print('Error. No matching file found.')
                exit()

        # else if the last dim file exists, then continue with the search file

        #Give the user options about what they want to search for
        print('How would you like to add an image to test against your file?')
        menu = {}
        menu[1] = 'Choose from a random grid from the data.'
        menu[2] = 'Enter your own data from an additional lidar file.'
        # ETC, add other options?

        testGrid = null
        while True:
            options = menu.keys()
            options.sort()
            for entry in options:
                print str(entry), menu[entry]
            choice = int(input('Please select an option: '))

            # Choose random from given file
            if choice == 1:

                #Return random index and calculate PCPDS
                testIDX = ProcessLas.randomGrid(dim)
                testGrid = PCPDS(testIDX, lasObj.filename)
                print('The random index is: ' + testIDX + '.')

                #Calculate bottleneck dista
                testBottleneck = BottleneckDistances(points, testGrid)
                guessGrid = testBottleneck.compute_distances()
                if guessGrid == testIDX:
                    print('##')
                else:
                    print('The index with the closest match to the random is index ' + guessGrid)

            # Import new file to find location in orig file
            elif choice == 2:
                testFile = input("Enter the name of the file you'd wish to import: ")
                temp = concatenate(testFile, '**')
                exists = os.path.isfile(concatenate('/path/to/', temp)
                if exists:
                    #Save persistence diagram of found file to testGrid
                else:
                    print('Error. No matching file found.')

            # Choice is not a viable option
            else: print('Please choose a number 1 - ' len(menu))

        playAgain = input('Would you like to test another lidar file? (Y/N)')
        if !playAgain.lower.find('y'):
            again = False


# Do Main
if __name__ == '__main__':
    main()

#make folder with filename and timestamp and save partitions
