from Classes.process_las import ProcessLas
from Classes.reference import reference as ref
import Classes.PCPDS
from Classes.bottleneck_dist import BottleneckDistances
from Classes.menu import menu
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

        dir_name = str(os.path.join('Sections', dir_name))


        # TODO: Dicuss changing the name of 'Sections' folder to 'Section_Collections' or something similar

        # TODO: Likely will want to handle this in another place in the future,
        # specifically when selecting the 'Section_Collection' we want to work with.
        # Currently just set to default to the directory being made.
        ref.set_cur_dir_name(dir_name)

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
                    print("Directory " + dir_name + " already exists.")

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
        menu_opt = {}
        menu_opt[1] = ': Choose from a random grid from the data.'
        menu_opt[2] = ': Enter your own data from an additional lidar file.'
        menu_opt[3] = ': Enter an IDX to search for'
        # ETC, add other options?

        # Create menu object with num of partitions, .las object, and points dictionary
        m = menu(partition, las_obj, points)

        # TODO: Remove once we can be sure that it properly prints out saved files in this path.
        print(ref.get_cur_dir_name())
        print("files in folder: ", ref.get_files_in_folder())

        play_menu = True
        while play_menu:

            # Print menu options
            options = menu_opt.keys()
            for entry in options:
                print(str(entry)+ str(menu_opt[entry]))
            choice = int(input('Please select an option: '))

            # Choose random from given file
            if choice == 1:
                play_menu = m.choice_1()

            # TODO: make functional
            # Import new file to find location in orig file
            elif choice == 2:
                play_menu = m.choice_2()

            #QUESTION should we chanage this to allow for manual idx entry instead?
            elif choice == 3:
                play_menu = m.choice_3()

            # Choice is not a viable option
            else: print('Please choose a number 1 through ' + str(len(menu)))

        play_again = input('Would you like to test another lidar file? (Y/N) ')
        if (play_again.find('y') == -1) & (play_again.find('Y') == -1):
            again = False

# Do Main
if __name__ == '__main__':
    main()

#make folder with filename and timestamp and save partitions
