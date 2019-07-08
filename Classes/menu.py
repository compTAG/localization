from Classes.process_las import ProcessLas
from Classes.reference import reference as ref
import Classes.PCPDS
from Classes.bottleneck_dist import BottleneckDistances
import numpy as np
import os.path

class menu:

    def __init__(self, partition, las_obj, points):

        self.partition = partition

        self.las_obj = las_obj

        self.points = points

    def num_results(self):

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

    def choice_1(self):

        # grabs a random section that is nonempty
        # TODO: have a check for None and index out of bounds in here
        while True:
            try:
                test_idx = self.las_obj.random_grid()
                test_grid = self.points[test_idx]
            except:
                continue
            if test_grid != None:
                break

        # prints information about the selected section
        print(f"points are {test_grid.point_cloud}")
        print(f"filt is {test_grid.persistance_diagram}")

        # prints the idx of the section
        print('The random index is: ' + str(test_idx) + '.')

        n_results = self.num_results(self.partition)

        #generate bottleneck distances object
        test_bottleneck = BottleneckDistances(self.points, self.test_grid)
        # searches for least bottleneck distances
        guess_grid = test_bottleneck.naive_search_distances(n_results)
        # prints out the idx values of the lowest bottleneck distances
        print('The indexes with the closest match to the random is index are: \n')
        for i in guess_grid:
            print(str(i[0]) + ' (bottleneck distance of ' + str(i[1]) + ')\n')

        return False

    def choice_2(self):

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

    def choice_3(self):

        # Loop over until a variable test_idx is found
        # Return random index and calculate PCPDS
        test_grid = None
        while test_grid == None:

            search_x = input("Enter the x value of the search index.\n")
            search_y = input("Enter the y value of the search index.\n")
            search_z = input("Enter the z value of the search index.\n")

            search_xyz = self.las_obj.find_index(search_x, search_y, search_z)
            test_grid = self.points[search_xyz]

            if test_grid == None:
                print("Please enter values between 0 and " + str(self.partition) + "\n")

        # Get desired number of results from user
        n_results = self.num_results()

        # Calculate bottleneck distance
        test_bottleneck = BottleneckDistances(self.points, test_grid)
        guess_grid = test_bottleneck.naive_search_distances(n_results)
        print('The indexes with the closest match to the random is index are: \n')
        for i in guess_grid:
            # TODO: Make index print out x, y, z
            print(str(i[0]) + ' (bottleneck distance of ' + str(i[1]) + ')\n')

        return False
