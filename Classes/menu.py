from Classes.process_las import ProcessLas
import Classes.PCPDS
from Classes.bottleneck_dist import BottleneckDistances
import numpy as np

class menu:

    def __init__(self, partition, las_obj, points):

        # Save number of partitions on each side of grid
        self.partition = partition

        # Save the las object created in main
        self.las_obj = las_obj

        # Save the dictionary of PCDPS objects
        self.points = points

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
    def __random_test_grid(self):
        # TODO: have a check for None and index out of bounds in here
        while True:
            try:
                test_idx = self.las_obj.random_grid()
                test_grid = self.points[test_idx]
            except:
                continue
            if test_grid != None:
                break
        return [test_grid, test_idx]

    # Choice 1: Select an unknown grid and test against all points
    def random_idx_normal(self):

        # Grab a random section that is nonempty
        [test_grid, test_idx] = self.__random_test_grid()

        # Prints information about the selected section
        print(f"points are {test_grid.point_cloud}")
        print(f"filt is {test_grid.persistance_diagram}")

        # Prints the idx of the section
        print('The random index is: ' + str(test_idx) + '.')

        n_results = self.__num_results()

        # Calculate bottleneck distance, print n_result matches
        test_bottleneck = BottleneckDistances(self.points, test_grid)
        guess_grid = test_bottleneck.naive_search_distances(n_results)
        test_bottleneck.print_matches(guess_grid)

        return False

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

        return False

    # Choice 3: Manually select a grid and test against all points
    def manual_idx_normal(self):

        # Loop over until a variable test_idx is found
        # Return random index and calculate PCPDS
        test_grid = None
        while test_grid == None:

            search_x = input("Enter the x value of the search index.\n")
            search_y = input("Enter the y value of the search index.\n")
            search_z = input("Enter the z value of the search index.\n")

            search_xyz = self.las_obj.find_index(search_x, search_y, search_z)
            print(str(search_xyz))
            test_grid = self.points[search_xyz]

            if test_grid == None:
                print("Please enter values between 0 and " + str(self.partition) + "\n")

        # Get desired number of results from user
        n_results = self.__num_results()

        # Calculate bottleneck distance, print n_result matches
        test_bottleneck = BottleneckDistances(self.points, test_grid)
        guess_grid = test_bottleneck.naive_search_distances(n_results)
        test_bottleneck.print_matches(guess_grid)

        return False

    # Choice 4: Rotate an unknown grid and test against all points
    def random_idx_rotated(self):

        # Grab a random section that is nonempty
        [test_grid, test_idx] = self.__random_test_grid()

        # TODO: Rotate dtest_grid with test_cases.py
        # Get desired number of results from user
        n_results = self.__num_results()

        # Calculate bottleneck distance, print n_result matches
        test_bottleneck = BottleneckDistances(self.points, test_grid)
        guess_grid = test_bottleneck.naive_search_distances(n_results)
        test_bottleneck.print_matches(guess_grid)

        return False
