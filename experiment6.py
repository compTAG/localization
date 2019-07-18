import random
from Classes.process_las import ProcessLas
import Classes.PCPDS
from Classes.menu import menu as menu
from Classes.PCPDS_manager import PCPDS_Manager
import Classes.file_manager as file_manager
import Classes.bottleneck_dist as bottleneck_distances

def main():

    number_of_data = 400
    # Create las object and calculate corresponding values
    filename = 'tiny'
    partition = 70
    las_obj = ProcessLas(filename, partition)

    # Makes a string of the folder path, os.path.join makes it compatible
    # between macs, windows, and linux
    dir_name = file_manager.make_folder(filename)

    pfm = PCPDS_Manager()
    dir_name = pfm.generate_collection(filename, partition)
    print('Dir:' + str(dir_name))

    las_obj.input_las(dir_name)
    datafile = open("bdripson70partitions.txt", "a")

    #import functions
    m = menu()

    for n in range(number_of_data):

        test_idx = las_obj.random_grid()
        test_pcpds = pfm.get_random_pcpds(test_idx)

        (X, Y, Z) = test_pcpds.get_xyz(str(test_idx))
        (dimX, dimY, dimZ) = test_pcpds.get_dimensions()
        bounds = test_pcpds.get_bounds(str(test_idx))

        results = []


        # Original Frame
        test_pd = test_pcpds.get_persistance_diagram()

        slide_left_X = pfm.get_pcpds(las_obj.find_index(X-1, Y))
        slide_right_X = pfm.get_pcpds(las_obj.find_index(X+1, Y))
        slide_up_Y = pfm.get_pcpds(las_obj.find_index(X, Y+1))
        slide_down_Y = pfm.get_pcpds(las_obj.find_index(X, Y-1))

        # Slide frame 10% across each direction
        for overlay in range(10):
            # Left
            bounds_left_X = m.transform(bounds, dimX, -1, True, overlay)
            left_X_pcpds = m.within_point_cloud(test_pcpds, slide_left_X, bounds_left_X)
            left_X_pd = left_X_pcpds.get_persistance_diagram()

            # Right
            bounds_right_X = m.transform(bounds, dimX, 1, True, overlay)
            right_X_pcpds = m.within_point_cloud(test_pcpds, slide_right_X, bounds_right_X)
            right_X_pd = right_X_pcpds.get_persistance_diagram()

            # Up
            bounds_up_Y = m.transform(bounds, dimY, 1, False, overlay)
            up_Y_pcpds = m.within_point_cloud(test_pcpds, slide_up_Y, bounds_up_Y)
            up_Y_pd = up_Y_pcpds.get_persistance_diagram()

            # Down
            bounds_down_Y = m.transform(bounds, dimY, -1, False, overlay)
            down_Y_pcpds = m.within_point_cloud(test_pcpds, slide_down_Y, bounds_down_Y)
            down_Y_pd = down_Y_pcpds.get_persistance_diagram()

            # Find average bottleneck at each overlay percentage
            results[overlay] = (results[overlay] + bottleneck_distances.get_distances(left_X_pd, test_pd)) / overlay
            results[overlay] = (results[overlay] + bottleneck_distances.get_distances(right_X_pd, test_pd)) / overlay
            results[overlay] = (results[overlay] + bottleneck_distances.get_distances(up_Y_pd, test_pd)) / overlay
            results[overlay] = (results[overlay] + bottleneck_distances.get_distances(down_Y_pd, test_pd)) / overlay

        #Repeat above for X-1, Y+-1


        datafile.write(str(test_idx))
        datafile.write(":")

        # Calculate bottleneck distance, print n_result matches
        for overlay_perc in guess_grid:
            datafile.write(str(overlay_perc))
            #print(idx)
            datafile.write(",")
        datafile.write('\n')

        m.progress(n, number_of_data, ("Processing random grid: "+str(test_idx)+"..."))

    print("Job done.")

# Do Main
if __name__ == '__main__':
    main()
