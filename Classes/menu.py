import Classes.PCPDS
import numpy as np
import Classes.file_manager as fm
from Classes.path_manager import PathManager as path_manager
from Classes.PCPDS_manager import PCPDS_Manager as pcpds_manager
import os.path
import sys

# TODO: Change these to reflect how bottleneck is called

class menu:

    # Return the desired number of results the user wants, given n <= partition^3
    def __num_results(partition):

        n_results = (partition**3)+1
        while n_results > partition**3:

            n_results = int(input('How many match results would you like?'))

            # If there are more results then there are amount of partitions,
            # Then get a new number
            if n_results > partition**3:
                print('Please enter an int smaller than ' + str(partition**3) + '.')
            elif n_results%1 != 0:
                print('Please enter an integer.')

        return n_results

    # TODO: Get n_results from the user, verify, and return.
    def get_n_result_input():
        pass
    # Acts as a progress bar
    def progress(count, total, status=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('\r[%s] %s%s %s' % (bar, percents, '%', status))
        sys.stdout.flush()


    # # Choice 2: Import another file, calculate new PCPDS and test against all points
    # def test_against_file():
    #
    #     test_file = input("Enter the name of the file you'd wish to import: ")
    #     temp = str(test_file + '.las')
    #     #concatenate('/path/to/'
    #     exists = os.path.isfile(temp)
    #     if exists:
    #         pass
    #         #Save persistence diagram of found file to test_grid
    #     else:
    #         print('Error. No matching file found. Exiting.')
    #         exit()
    #
    #
    # Choice 3: Manually select a grid and test against all points
    # def manual_idx_normal(partition, collection_path, test_idx):
    #
    #     path_manager = path_manager()
    #     #dir = path_manager.get_path_manager().get_full_cur_dir(dir_name)
    #
    #     # Loop over until a variable test_idx is found
    #     # Return random index and calculate PCPDS
    #     test_pcpds = None
    #     while test_pcpds == None:
    #
    #         search_x = input("Enter the x value of the search index.\n")
    #         search_y = input("Enter the y value of the search index.\n")
    #
    #         search_xyz = self.las_obj.find_index(search_x, search_y)
    #         print(str(search_xyz))
    #         test_pcpds = fm.load(os.path.join(dir, str(search_xyz)))
    #
    #         if test_pcpds == None:
    #             print("Please enter values between 0 and " + str(partition) + "\n")
    #
    #     n_results = self.__num_results(partition)
    #
    #     # Calculate bottleneck distance, print n_result matches
    #     get_distance = bottleneck_distances.search_distances
    #     guess_grid  = get_distance(n_results, test_pcpds.get_persistance_diagram(), collection_path)
    #     for idx, _ in guess_grid:
    #         print(str(idx)  + '. ' + str(guess_grid[idx]))
    #
    #
    # # Choice 4: Rotate an unknown grid and test against all points
    # def random_idx_rotated(self, collection_path):
    #
    #     # Grab a random section that is nonempty
    #     [test_pcpds, test_idx] = self.random_test_grid()
    #
    #     # Get desired number of results from user
    #     n_results = self.__num_results()
    #
    #     # Calculate bottleneck distance, print n_result mat ches
    #     get_distance = bottleneck_distances.search_distances
    #     guess_grid  = get_distance(n_results, test_pcpds.get_persistance_diagram(), collection_path)
    #     for idx, _ in guess_grid:
    #         print(str(idx)  + '. ' + str(guess_grid[idx]))
