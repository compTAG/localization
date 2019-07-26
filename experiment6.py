import random
from Classes.process_las import ProcessLas
import Classes.PCPDS
from Classes.filtrations import Filtration as filtration
from Classes.menu import menu as menu
from Classes.PCPDS_manager import PCPDS_Manager
import Classes.file_manager as file_manager
import Classes.bottleneck_dist as bottleneck_distances
import os.path
import xlwt
from xlwt import Workbook

def main():

    pfm = PCPDS_Manager()
    number_of_data = 200 #Max 256 when saving to excel
    num_partitions_to_slide = 3

    print("Please enter a collection that has already been filtrated:")

    # Loop here for valid directory
    filename = menu.get_input("Filename: ")

    partition = int(menu.get_input("Partition: "))

    collection = filename + '_' + str(partition)
    dir_name = collection
    las_obj = ProcessLas(filename, partition)

    pfm.get_path_manager().set_cur_dir(collection)

    pfm.set_collection_dir(dir_name)

    valid = pfm.get_collection_dir()

    # If not a valid directory, ask again saying it is invalid
    while(not valid):
        if not pfm.get_collection_dir():
            print("Invalid collection name:", pfm.get_path_manager().get_cur_dir() ,"try again.")
        collection = menu.get_input("Directory: ")
        pfm.get_path_manager().set_cur_dir(collection)
        valid = pfm.get_collection_dir()

        # Checks the first pcpds object in this directory for if it has a persistance diagram
        pcpds_temp = None
        for file in os.listdir(pfm.get_path_manager().get_full_cur_dir_var(collection)):
            file_path = os.path.join(pfm.get_path_manager().get_full_cur_dir(), file)
            pcpds_temp = file_manager.load(file_path)
            break
        if pcpds_temp is not None:
            if pcpds_temp.get_persistance_diagram() is not None:
                print("Valid Directory Chosen:", valid)
                break
            else:
                valid = False
                print("\nNo persistance diagram present for files @ collection:", pfm.get_path_manager().get_full_cur_dir() + ".\n")
                print("Please Either enter a directory that has been filtrated for persistance diagrams or run 'generate_persistance_diagrams.py' on the collection.")
        else:
            print("Problem loading pcpds file, it loaded as None.")

    # TODO: make a random function based off of count & iteration
    #print("File count:", len(os.listdir(pfm.get_path_manager().get_full_cur_dir_var(collection))))

    wb = Workbook()
    excel_sheet = wb.add_sheet('Sheet 2')

    for n in range(number_of_data):

        # Find random valid index with valid slide pcpds
        test_idx = str(las_obj.random_grid_edge_case(num_partitions_to_slide))

        valid_idx = False
        while valid_idx == False:

            #print(os.path.join(pfm.get_collection_dir(), test_idx + ".json"))

            # Find valid center pcpds
            test_idx = str(las_obj.random_grid_edge_case(num_partitions_to_slide))
            while pfm.get_path_manager().validate_file(os.path.join(pfm.get_collection_dir(), test_idx + ".json")) == False:
                test_idx = str(las_obj.random_grid_edge_case(num_partitions_to_slide))

            test_pcpds = pfm.get_random_pcpds_idx(test_idx)
            (X, Y, Z) = test_pcpds.get_xyz()

            # Find valid slide directional pcpds objects
            slide_left_X = las_obj.find_index(X-1, Y)
            slide_right_X = las_obj.find_index(X+1, Y)
            slide_up_Y = las_obj.find_index(X, Y+1)
            slide_down_Y = las_obj.find_index(X, Y-1)
            slide_left_down = las_obj.find_index(X-1, Y-1)
            slide_right_down = las_obj.find_index(X+1, Y-1)
            slide_right_up = las_obj.find_index(X+1, Y+1)
            slide_left_up = las_obj.find_index(X-1, Y+1)

            if pfm.get_path_manager().validate_file(os.path.join(pfm.get_collection_dir(), str(slide_left_X) +".json")) == True:
                if pfm.get_path_manager().validate_file(os.path.join(pfm.get_collection_dir(), str(slide_right_X) +".json")) == True:
                    if pfm.get_path_manager().validate_file(os.path.join(pfm.get_collection_dir(), str(slide_up_Y) +".json")) == True:
                        if pfm.get_path_manager().validate_file(os.path.join(pfm.get_collection_dir(), str(slide_down_Y) +".json")) == True:
                            valid_idx = True
                            #print("VALID RANDOM ID: ", test_idx)

        # Get the random pcpds's details
        #print('COORDINATES: ' + 'X:' + str(X) + ' Y:' + str(Y)+ ' Z:' + str(Z))
        (dimX, dimY, dimZ) = test_pcpds.get_dimensions()
        bounds = test_pcpds.get_bounds()
        test_pcpds = filtration.get_rips_diagram(test_pcpds)
        test_pd = test_pcpds.get_persistance_diagram()

        slide_left_X = pfm.get_pcpds(slide_left_X)
        slide_right_X = pfm.get_pcpds(slide_right_X)
        slide_up_Y = pfm.get_pcpds(slide_up_Y)
        slide_down_Y = pfm.get_pcpds(slide_down_Y)

        num_slides = 10
        num_directions = 4
        #results = [0]*(num_slides * num_partitions_to_slide)
        excel_sheet.write(0, n, str(test_idx))
        for overlay in range(1, num_slides * num_partitions_to_slide):

            # Left
            bounds_left_X = menu.transform(bounds, dimX, -1, True, overlay, num_slides)
            left_X_pcpds = menu.within_point_cloud(test_pcpds, slide_left_X, bounds_left_X)

            # Right
            bounds_right_X = menu.transform(bounds, dimX, 1, True, overlay, num_slides)
            right_X_pcpds = menu.within_point_cloud(test_pcpds, slide_right_X, bounds_right_X)

            # Up
            bounds_up_Y = menu.transform(bounds, dimY, 1, False, overlay, num_slides)
            up_Y_pcpds = menu.within_point_cloud(test_pcpds, slide_up_Y, bounds_up_Y)

            # Down
            bounds_down_Y = menu.transform(bounds, dimY, -1, False, overlay, num_slides)
            down_Y_pcpds = menu.within_point_cloud(test_pcpds, slide_down_Y, bounds_down_Y)

            overlay_avg = -1
            num_dir = 0

            try:
                left_X_pcpds = filtration.get_rips_diagram(left_X_pcpds)
                left_X_pd = left_X_pcpds.get_persistance_diagram()
                left_bn = bottleneck_distances.get_distances(left_X_pd, test_pd)
                num_dir = num_dir + 1
            except:
                left_bn = 0

            try:
                right_X_pcpds = filtration.get_rips_diagram(right_X_pcpds)
                right_X_pd = right_X_pcpds.get_persistance_diagram()
                right_bn = bottleneck_distances.get_distances(right_X_pd, test_pd)
                num_dir = num_dir + 1
            except:
                right_bn = 0

            try:
                up_Y_pcpds = filtration.get_rips_diagram(up_Y_pcpds)
                up_Y_pd = up_Y_pcpds.get_persistance_diagram()
                up_bn = bottleneck_distances.get_distances(up_Y_pd, test_pd)
                num_dir = num_dir + 1
            except:
                up_bn = 0

            try:
                down_Y_pcpds = filtration.get_rips_diagram(down_Y_pcpds)
                down_Y_pd = down_Y_pcpds.get_persistance_diagram()
                down_bn = bottleneck_distances.get_distances(down_Y_pd, test_pd)
                num_dir = num_dir + 1
            except:
                down_bn = 0


            if (num_dir != 0):
                overlay_avg = (left_bn + right_bn + up_bn + down_bn) / num_dir
            excel_sheet.write(overlay, n, str(overlay_avg))

        menu.progress(n, number_of_data, ("Processing random grid: "+str(test_idx)+"..."))

    # Write results .xls file
    wb.save(dir_name + '.xls')
    print("Job done.")

# Do Main
if __name__ == '__main__':
    main()
