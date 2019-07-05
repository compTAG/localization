from Classes.process_las import ProcessLas
import Classes.PCPDS
from Classes.bottleneck_dist import BottleneckDistances
import numpy as np
import os.path
from datetime import datetime

def main():

    again = True
    while again == True:

        #Have the user input their desired file and partition count
        partition = 0.1
        while (partition%1) != 0:
            partition = float(input("Enter Partition Count (1D): "))
            if (partition%1) != 0:
                print('Please enter a whole number.')
        filename = input("Enter the name of the file you'd wish to import: ")
        partition = int(partition)

        # Create las object and calculate corresponding values
        las_obj = ProcessLas(filename, partition, len(str(partition)))
        idx = int(str(partition) + str(partition) + str(partition))

        # Makes a string of the folder path, os.path.join makes it compatible
        # between macs, windows, and linux
        dir_name = str(filename + '_' + str(partition) + '_' + datetime.today().strftime('%Y-%m-%d'))
        dir_name = str(os.path.join('Sections', 'PCPDS', dir_name))

        points = None

        # Check if the final persistence diagram for the las object doesn't exist
        # Check under a given timestamp to avoid multiple same files
        if not (las_obj.check_file(idx, '.json', dir_name)): #Where ** is the ext of PDs
            #Check if the file exists

            if las_obj.check_file(None, '.las', None):
                # Saves the persistence diagrams of each grid
                # and returns the dict of PCPDS

                try:
                    os.makedirs(dir_name)
                    print("Directory " + dir_name + " created.")

                except FileExistsError:
                    print("Directory " + dir_name + " already exists")

                # Save persistence diagrams in the aforementioned folder
                points = las_obj.input_las()

            else:
                print('Error. No matching file found. Exiting.')
                exit()
        else:
            pass
            # Import persistence diagrams/ points array
            # using PCPDS .json files

        print(str(len(points)))

        #Give the user options about what they want to search for
        print('How would you like to add an image to test against your file?')
        menu = {}
        menu[1] = ': Choose from a random grid from the data.'
        menu[2] = ': Enter your own data from an additional lidar file.'
        menu[3] = ': Enter an IDX to search for'
        # ETC, add other options?

        play_menu = True
        while play_menu:
            options = menu.keys()
            for entry in options:
                print(str(entry)+ str(menu[entry]))
            choice = int(input('Please select an option: '))

            # Choose random from given file
            if choice == 1:
                play_menu = False

                # Loop over until a variable test_idx is found
                # Return random index and calculate PCPDS
                test_grid = None
                while test_grid == None:
                    test_idx = las_obj.random_grid()
                    test_grid = points[test_idx]

                # TODO: Make index print out x, y, z
                print('The random index is: ' + str(test_idx) + '.')
                num_results = (partition**3)+1
                while num_results > partition**3:
                    num_results = int(input('How many match results would you like?'))
                    if num_results > partition**3:
                        print('Please enter an int smaller than ' + str(partition**3) + '.')
                    elif num_results%1 != 0:
                        print('Please enter an integer.')

                # Calculate bottleneck distance
                test_bottleneck = BottleneckDistances(points, test_grid)
                guess_grid = test_bottleneck.naive_search_distances(num_results)
                print('The indexes with the closest match to the random is index are: \n')
                for i in guess_grid:
                    # TODO: Make index print out x, y, z
                    print(str(i[0]) + ' (bottleneck distance of ' + str(i[1]) + ')\n')

            # Import new file to find location in orig file
            elif choice == 2:
                play_menu = False

                test_file = input("Enter the name of the file you'd wish to import: ")
                temp = str(test_file + '.las')
                #concatenate('/path/to/'
                exists = os.path.isfile(temp)
                if exists:
                    pass
                    #Save persistence diagram of found file to test_grid
                else:
                    print('Error. No matching file found. Exiting.')
                    exit()

            elif choice == 3:
                play_menu = False

                # TODO: Check the xyz is a valid index
                search_x = input("Enter the x value of the search index.\n")
                search_y = input("Enter the y value of the search index.\n")
                search_z = input("Enter the z value of the search index.\n")

                search_xyz = las_obj.find_index(x, y, z)

                # TODO: Continue...

            # Choice is not a viable option
            else: print('Please choose a number 1 through ' + str(len(menu)))

        play_again = input('Would you like to test another lidar file? (Y/N) ')
        if (play_again.find('y') == -1) & (play_again.find('Y') == -1):
            again = False


# Do Main
if __name__ == '__main__':
    main()

#make folder with filename and timestamp and save partitions
