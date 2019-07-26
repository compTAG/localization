import random
from Classes.process_las import ProcessLas
import Classes.PCPDS
from Classes.filtrations import Filtration as filtration
from Classes.menu import menu as menu
from Classes.PCPDS_manager import PCPDS_Manager
import Classes.file_manager as file_manager
import Classes.bottleneck_dist as bottleneck_distances
import os.path
from xlwt import Workbook

def main():

    pfm = PCPDS_Manager()
    number_of_data = 400

    print("Please enter a collection that has already been filtered:")
    #TODO: list collections
    # Loop here for valid directory
    collection = menu.get_input("Directory: ")

    pfm.get_path_manager().set_cur_dir(collection)

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

    cur_dir = pfm.get_path_manager().get_full_cur_dir()

    wb = Workbook()
    excel_sheet = wb.add_sheet('Sheet 1')

    for n in range(number_of_data):

        # Find random valid index with valid slide pcpds
        test_idx = file_manager.get_random_file(cur_dir, '.json')[:-5]

        valid_idx = False
        while valid_idx == False:

            # Find valid center pcpds
            test_idx =file_manager.get_random_file(cur_dir, '.json')[:-5]
            while pfm.get_path_manager().validate_file(os.path.join(cur_dir, test_idx+".json")) == False:
                test_idx = file_manager.get_random_file(cur_dir, '.json')[:-5]

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
        test_pcpds = filtration.get_rips_diagram(test_pcpds)
        test_pd = test_pcpds.get_persistance_diagram()

        results = [0]*11
        num_dir = 4

        slide_left_X = pfm.get_pcpds(slide_left_X)
        slide_right_X = pfm.get_pcpds(slide_right_X)
        slide_up_Y = pfm.get_pcpds(slide_up_Y)
        slide_down_Y = pfm.get_pcpds(slide_down_Y)

        # Slide frame 10% across each direction
        for overlay in range(1, 10):

            # Left
            bounds_left_X = menu.transform(bounds, dimX, -1, True, overlay)
            left_X_pcpds = menu.within_point_cloud(test_pcpds, slide_left_X, bounds_left_X)
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
            results[overlay-1] = bottleneck_distances.get_distances(left_X_pd, test_pd)
            results[overlay-1] = results[overlay] + bottleneck_distances.get_distances(right_X_pd, test_pd)
            results[overlay-1] = results[overlay] + bottleneck_distances.get_distances(up_Y_pd, test_pd)
            results[overlay-1] = (results[overlay] + bottleneck_distances.get_distances(down_Y_pd, test_pd)) / num_dir


        # Write results .xls file
        num = 1
        excel_sheet.write(n, 0, str(test_idx))
        for overlay_avg in results:
            excel_sheet.write(n, num, str(overlay_avg))
            num = num + 1
        wb.save(dir_name + '.xls')

        menu.progress(n, number_of_data, ("Processing random grid: "+str(test_idx)+"..."))

    print("Job done.")

# Do Main
if __name__ == '__main__':
    main()
