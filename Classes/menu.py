from Classes.process_las import ProcessLas
import Classes.PCPDS
from Classes.bottleneck_dist import BottleneckDistances
import numpy as np
import Classes.file_manager as fm
import Classes.path_manager as path_manager

# TODO: Change these to reflect how bottleneck is called

class menu:

    def __init__(self, partition, las_obj, dir_name):

        # Save number of partitions on each side of grid
        self.partition = partition

        # Save the las object created in main
        self.las_obj = las_obj

        # Save the dictionary of PCDPS objects
        self.dir_name = dir_name

    # Return the desired number of results the user wants, given n <= partition^3
    def __num_results(self):

        n_results = (self.partition**3)+1
        while n_results > self.partition**3:

            n_results = int(input('How many match results would you like?'))

            # If there are more results then there are amount of partitions,
            # Then get a new number
            if n_results > self.partition**3:
                print('Please enter an int smaller than ' + str(self.partition**3) + '.')
            elif n_results%1 != 0:
                print('Please enter an integer.')

        return n_results

    # Select a random, non-empty grid from the dictionary of points
    # TODO: Return the loaded random index's PCPDS obj
    def __random_test_grid(self):
        # TODO: have a check for None and index out of bounds in here
        test_idx = self.las_obj.random_grid()
        path_manager = pm()
        dir = path_manager.get_path_manager().get_full_cur_dir(dir_name)
        test_pcpds = fm.load(os.path.join(dir, str(test_idx)))
        return [test_pcpds, test_idx]

    # Choice 1: Select an unknown grid and test against all points
    def random_idx_normal(self, collection_path):

        # Grab a random section that is nonempty
        [test_pcpds, test_idx] = self.__random_test_grid()

        # Prints information about the selected section
        print(f"points are {test_pcpds.point_cloud}")
        print(f"filt is {test_pcpds.persistance_diagram}")

        # Prints the idx of the section
        print('The random index is: ' + str(test_idx) + '.')

        n_results = self.__num_results()

        # Calculate bottleneck distance, print n_result matches
        get_distance = BottleneckDistances.search_distances
        guess_grid  = get_distance(n_results, test_pcpds.get_persistance_diagram(), collection_path)
        for idx, _ in guess_grid:
            print(str(idx)  + '. ' + str(guess_grid[idx]))

    # Choice 2: Import another file, calculate new PCPDS and test against all points
    def test_against_file(self):

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


    # Choice 3: Manually select a grid and test against all points
    def manual_idx_normal(self, collection_path):

        path_manager = pm()
        dir = path_manager.get_path_manager().get_full_cur_dir(dir_name)

        # Loop over until a variable test_idx is found
        # Return random index and calculate PCPDS
        test_pcpds = None
        while test_pcpds == None:

            search_x = input("Enter the x value of the search index.\n")
            search_y = input("Enter the y value of the search index.\n")

            search_xyz = self.las_obj.find_index(search_x, search_y)
            print(str(search_xyz))
            test_pcpds = fm.load(os.path.join(dir, str(test_idx)))

            if test_pcpds == None:
                print("Please enter values between 0 and " + str(self.partition) + "\n")

        n_results = self.__num_results()

        # Calculate bottleneck distance, print n_result matches
        get_distance = BottleneckDistances.search_distances
        guess_grid  = get_distance(n_results, test_pcpds.get_persistance_diagram(), collection_path)
        for idx, _ in guess_grid:
            print(str(idx)  + '. ' + str(guess_grid[idx]))


    # Choice 4: Rotate an unknown grid and test against all points
    def random_idx_rotated(self, collection_path):

        # Grab a random section that is nonempty
        [test_pcpds, test_idx] = self.__random_test_grid()

        # TODO: Rotate test_pcpds

        # Get desired number of results from user
        n_results = self.__num_results()

        # Calculate bottleneck distance, print n_result matches
        get_distance = BottleneckDistances.search_distances
        guess_grid  = get_distance(n_results, test_pcpds.get_persistance_diagram(), collection_path)
        for idx, _ in guess_grid:
            print(str(idx)  + '. ' + str(guess_grid[idx]))
