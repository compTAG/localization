import random
from Classes.process_las import ProcessLas
import Classes.PCPDS
from Classes.filtrations import Filtration as filtration
from Classes.menu import menu as menu
from Classes.PCPDS_manager import PCPDS_Manager
import Classes.file_manager as file_manager
import Classes.bottleneck_dist as bottleneck_distances
import os.path

def main():

    number_of_data = 400
    # Create las object and calculate corresponding values
    filename = 'tiny'
    partition = 50
    las_obj = ProcessLas(filename, partition)

    # Makes a string of the folder path, os.path.join makes it compatible
    # between macs, windows, and linux
    dir_name = file_manager.make_folder(filename)

    pfm = PCPDS_Manager()
    dir_name = pfm.generate_collection(filename, partition)
    print('Dir:' + str(dir_name))

    las_obj.input_las(dir_name)
    datafile = open("bdripson70partitions.txt", "a")

    for n in range(number_of_data):


        # Find random valid index with valid slide pcpds
        test_idx = str(las_obj.random_grid_edge_case())

        valid_idx = False
        while valid_idx == False:

            # Find valid center pcpds
            test_idx = str(las_obj.random_grid_edge_case())
            while pfm.get_path_manager().validate_file(os.path.join(dir_name, test_idx+".json")) == False:
                test_idx = str(las_obj.random_grid_edge_case())

            test_pcpds = pfm.get_random_pcpds(test_idx)
            (X, Y, Z) = test_pcpds.get_xyz(str(test_idx))

            # Find valid slide directional pcpds objects
            slide_left_X = las_obj.find_index(X-1, Y)
            slide_right_X = las_obj.find_index(X+1, Y)
            slide_up_Y = las_obj.find_index(X, Y+1)
            slide_down_Y = las_obj.find_index(X, Y-1)

            if pfm.get_path_manager().validate_file(os.path.join(dir_name, str(slide_left_X) +".json")) == True:
                if pfm.get_path_manager().validate_file(os.path.join(dir_name, str(slide_right_X) +".json")) == True:
                    if pfm.get_path_manager().validate_file(os.path.join(dir_name, str(slide_up_Y) +".json")) == True:
                        if pfm.get_path_manager().validate_file(os.path.join(dir_name, str(slide_down_Y) +".json")) == True:
                            valid_idx = True
                            print("VALID RANDOM ID: ", test_idx)

        # Get the random pcpds's details
        print('COORDINATES: ' + 'X:' + str(X) + ' Y:' + str(Y)+ ' Z:' + str(Z))
        (dimX, dimY, dimZ) = test_pcpds.get_dimensions()
        bounds = test_pcpds.get_bounds(str(test_idx))
        test_pd = test_pcpds.get_persistance_diagram()

        results = []
        num_dir = 4

        slide_left_X = pfm.get_pcpds(slide_left_X)
        slide_right_X = pfm.get_pcpds(slide_right_X)
        slide_up_Y = pfm.get_pcpds(slide_up_Y)
        slide_down_Y = pfm.get_pcpds(slide_down_Y)

        # Slide frame 10% across each direction
        for overlay in range(10):
            # Left
            bounds_left_X = menu.transform(bounds, dimX, -1, True, overlay)
            left_X_pcpds = menu.within_point_cloud(test_pcpds, slide_left_X, bounds_left_X)
            print(left_X_pcpds.get_point_cloud())
            left_X_pcpds = filtration.get_rips_diagram(left_X_pcpds)
            left_X_pd = left_X_pcpds.get_persistance_diagram()

            # Right
            bounds_right_X = menu.transform(bounds, dimX, 1, True, overlay)
            right_X_pcpds = menu.within_point_cloud(test_pcpds, slide_right_X, bounds_right_X)
            right_X_pcpds = filtration.get_rips_diagram(right_X_pcpds)
            right_X_pd = right_X_pcpds.get_persistance_diagram()

            # Up
            bounds_up_Y = menu.transform(bounds, dimY, 1, False, overlay)
            up_Y_pcpds = menu.within_point_cloud(test_pcpds, slide_up_Y, bounds_up_Y)
            up_Y_pcpds = filtration.get_rips_diagram(up_Y_pcpds)
            up_Y_pd = up_Y_pcpds.get_persistance_diagram()

            # Down
            bounds_down_Y = menu.transform(bounds, dimY, -1, False, overlay)
            down_Y_pcpds = menu.within_point_cloud(test_pcpds, slide_down_Y, bounds_down_Y)
            down_Y_pcpds = filtration.get_rips_diagram(down_Y_pcpds)
            down_Y_pd = down_Y_pcpds.get_persistance_diagram()

            # Find average bottleneck at each overlay percentage
            results[overlay] = bottleneck_distances.get_distances(left_X_pd, test_pd)
            results[overlay] = results[overlay] + bottleneck_distances.get_distances(right_X_pd, test_pd)
            results[overlay] = results[overlay] + bottleneck_distances.get_distances(up_Y_pd, test_pd)
            results[overlay] = (results[overlay] + bottleneck_distances.get_distances(down_Y_pd, test_pd)) / num_dir


        # Write results file
        datafile.write(str(test_idx))
        datafile.write(":")
        num = 1
        for overlay_avg in results:
            datafile.write(str(float(num)/10.0) + ': ' + str(overlay_avg))
            datafile.write(",")
            num = num + 1
        datafile.write('\n')

        menu.progress(n, number_of_data, ("Processing random grid: "+str(test_idx)+"..."))

    print("Job done.")

# Do Main
if __name__ == '__main__':
    main()
