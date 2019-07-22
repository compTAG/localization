from Classes.PCPDS import PCPDS as pcpds
import numpy as np
import Classes.file_manager as fm
from Classes.path_manager import PathManager as path_manager
from Classes.PCPDS_manager import PCPDS_Manager as pcpds_manager
import os.path
import sys

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

    def transform(bounds, dim, direction, axis, overlay):

        (low_x_bound, high_x_bound, low_y_bound, high_y_bound, low_z_bound, high_z_bound) = bounds
        dim_to_move = direction * (dim * ((float(overlay))/10))

        # True = X Axis
        if axis == True:
            low_x_bound = low_x_bound + dim_to_move
            high_x_bound = high_x_bound + dim_to_move

        # False = Y Axis
        else:
            low_y_bound = low_y_bound + dim_to_move
            high_y_bound = high_y_bound + dim_to_move

        bounds = (low_x_bound, high_x_bound, low_y_bound, high_y_bound, low_z_bound, high_z_bound)
        return bounds

    def within_point_cloud(test_pcpds, slide_pcpds, bounds):

        (low_x_bound, high_x_bound, low_y_bound, high_y_bound, low_z_bound, high_z_bound) = bounds
        new_pc = []
        print(test_pcpds.point_cloud, str(range(len(test_pcpds.point_cloud))))
        print(slide_pcpds.point_cloud, str(range(len(slide_pcpds.point_cloud))))

        print(str(bounds))
        points_in_bounds = np.array([0.0,0.0,0.0]) # pop this later
        union = np.vstack((test_pcpds.point_cloud,slide_pcpds.point_cloud))
        for i in range(len(union)):
            if low_x_bound <= union[i][0] and union[i][0] < high_x_bound and low_y_bound <= union[i][1] and union[i][1] < high_y_bound:
                points_in_bounds = np.vstack((union[i],points_in_bounds))
                #import pdb; pdb.set_trace()
            else:
                print(f"I'm empty inside {i}")

        ret_pcpds = pcpds(-1, (high_x_bound-low_x_bound, high_y_bound-low_y_bound))
        ret_pcpds.set_point_cloud(points_in_bounds)

        return ret_pcpds
