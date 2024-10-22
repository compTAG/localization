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
         return input("How many results would you like?\n")

    def get_filename_input():
        return input("Enter file name: ")

    def get_input(hint):
        return input(hint)

    def get_int_input():
        while(True):
            try:
                result = int(input("Enter int: "))
                return result
            except:
                print("Incorrect value type entered, try Again.")

    def get_float_input():
        while(True):
            try:
                result = float(input("Enter theta: "))
                return result
            except:
                print("Incorrect value type entered, try Again.")

    # Acts as a progress bar
    def progress(count, total, status=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('\r[%s] %s%s %s' % (bar, percents, '%', status))
        sys.stdout.flush()

    def transform(bounds, dim, direction, axis, overlay, num_slides):

        (low_x_bound, high_x_bound, low_y_bound, high_y_bound, low_z_bound, high_z_bound) = bounds
        dim_to_move = direction * (dim * ((float(overlay))/num_slides))

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

    def within_point_cloud(og_pcpds, slide_pcpds, bounds):

        (low_x_bound, high_x_bound, low_y_bound, high_y_bound, low_z_bound, high_z_bound) = bounds
        new_pc = []

        points_in_bounds = np.array([0.0,0.0,0.0]) # pop this later

        union = np.vstack((og_pcpds.point_cloud,slide_pcpds.point_cloud))
        for i in range(len(union)):
            #print(str(low_x_bound) + ' ' + str(union[i][0]) + ' ' + str(high_x_bound))
            #print(str(low_y_bound) + ' ' + str(union[i][1]) + ' ' + str(high_y_bound))
            #inp = input("Continue?")
            if low_x_bound <= union[i][0] and union[i][0] < high_x_bound and low_y_bound <= union[i][1] and union[i][1] < high_y_bound:
                points_in_bounds = np.vstack((union[i],points_in_bounds))
                #print(str(i))
        ret_pcpds = pcpds("Dave", (high_x_bound-low_x_bound, high_y_bound-low_y_bound))

        #points_in_bounds = np.delete(points_in_bounds,len(points_in_bounds)-1, 0)
        
        ret_pcpds.set_point_cloud(points_in_bounds[:-1])

        return ret_pcpds

# def within_point_cloud(og_pcpds, slide_pcpds, bounds):
    
#         (low_x_bound, high_x_bound, low_y_bound, high_y_bound, low_z_bound, high_z_bound) = bounds
#         new_pc = []

#         points_in_bounds = np.vstack((np.array([0.0,0.0,0.0]), np.array([0.0,0.0,0.0])))

#         union = np.vstack((og_pcpds.point_cloud,slide_pcpds.point_cloud))
#         for i in range(len(union)):
#             #print(str(low_x_bound) + ' ' + str(union[i][0]) + ' ' + str(high_x_bound))
#             #print(str(low_y_bound) + ' ' + str(union[i][1]) + ' ' + str(high_y_bound))
#             #inp = input("Continue?")
#             if low_x_bound <= union[i][0] and union[i][0] < high_x_bound and low_y_bound <= union[i][1] and union[i][1] < high_y_bound:
#                 points_in_bounds = np.vstack((union[i],points_in_bounds))
#                 #print(str(i))
#         ret_pcpds = pcpds("Dave", (high_x_bound-low_x_bound, high_y_bound-low_y_bound))

#         #points_in_bounds = np.delete(points_in_bounds,len(points_in_bounds)-1, 0)
        
#         print("POINTS IN BOUNDS:", points_in_bounds[:-2])
#         menu.get_input("ENTER:")
#         ret_pcpds.set_point_cloud(points_in_bounds[:-2])

#         return ret_pcpds
