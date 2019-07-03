from Classes.process_las import ProcessLas
import Classes.PCPDS
import Classes.bottleneck_dist
import numpy as np
import os.path
from datetime import datetime

def main():

    again = True
    while again == True:

        #Have the user input their desired file and partition count
        partition = 0.1
        while (partition%1) != 0:
            partition = int(input("Enter Partition Count (1D): "))
            if (partition%1) != 0:
                print('Please enter a whole number.')
        filename = input("Enter the name of the file you'd wish to import: ")

        # Create las object and calculate corresponding values
        las_obj = ProcessLas(filename, partition, len(str(partition)))
        idx = int(str(partition) + str(partition) + str(partition))

        dir_name = str(filename + datetime.today().strftime('%Y-%m-%d'))

        points = None
        # Check if the final persistence diagram for the las object doesn't exist
        # Check under a given timestamp to avoid multiple same files
        if not (las_obj.check_file(idx, '.json', dir_name)): #Where ** is the ext of PDs
            #Check if the file exists

            if las_obj.check_file(None, '.las', None):
                # Saves the persistence diagrams of each grid
                # and returns the dict of PCPDS
                points = las_obj.input_las()

                try:
                    os.mkdir(dir_name)
                    print("Directory " + dir_name + " created.")

                except FileExistsError:
                    print("Directory " + dir_name + " already exists")

                # + Save persistence diagrams

            else:
                print('Error. No matching file found.')
                exit()
        else:
            pass
            # Import persistence diagrams/ points array
            # using PCPDS .json files

        # else if the last partition file exists, then continue with the search file

        #Give the user options about what they want to search for
        print('How would you like to add an image to test against your file?')
        menu = {}
        menu[1] = 'Choose from a random grid from the data.'
        menu[2] = 'Enter your own data from an additional lidar file.'
        menu[3] = 'Enter an IDX to search for'
        # ETC, add other options?

        test_grid = null
        while True:
            options = menu.keys()
            options.sort()
            for entry in options:
                print(str(entry)+ str(menu[entry]))
            choice = int(input('Please select an option: '))

            # Choose random from given file
            if choice == 1:

                #Return random index and calculate PCPDS
                test_idx = las_obj.random_grid(partition)
                test_grid = PCPDS(test_idx, las_obj.filename)
                print('The random index is: ' + test_idx + '.')

                #Calculate bottleneck dista
                test_bottleneck = BottleneckDistances(points, test_grid)
                guess_grid = test_bottleneck.compute_distances()
                if guess_grid == test_idx:
                    print('##')
                else:
                    print('The index with the closest match to the random is index ' + guess_grid)

            # Import new file to find location in orig file
            elif choice == 2:
                test_file = input("Enter the name of the file you'd wish to import: ")
                temp = concatenate(test_file, '.las')
                #concatenate('/path/to/'
                exists = os.path.isfile(temp)
                if exists:
                    pass
                    #Save persistence diagram of found file to test_grid
                else:
                    print('Error. No matching file found.')
                    exit()



            # Choice is not a viable option
            else: print('Please choose a number 1 - ' + len(menu))

        play_again = input('Would you like to test another lidar file? (Y/N)')
        if not play_again.lower.find('y'):
            again = False


# Do Main
if __name__ == '__main__':
    main()

#make folder with filename and timestamp and save partitions
