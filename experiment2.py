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

    # Will need the filtration method for new point cloud filtering later.
    filt_method = None
    leading_zeros = 0
    dir_name = ""

    pfm.get_path_manager().set_cur_dir("")

    valid = False


    print("Please enter a collection that has already been filtered:")
    # If not a valid directory, ask again saying it is invalid
    while(not valid):
        if not pfm.get_collection_dir():
            print("Invalid collection name:", pfm.get_path_manager().get_cur_dir(), "try again.")
        dir_name = menu.get_input("Directory: ")
        pfm.get_path_manager().set_cur_dir(dir_name)
        valid = pfm.get_collection_dir()

        # Checks the first pcpds object in this directory for if it has a persistance diagram
        pcpds_temp = None
        for file in os.listdir(pfm.get_path_manager().get_full_cur_dir_var(dir_name)):
            file_path = os.path.join(pfm.get_path_manager().get_full_cur_dir(), file)
            pcpds_temp = file_manager.load(file_path)
            break
        if pcpds_temp is not None:
            if pcpds_temp.get_persistance_diagram() is not None:
                print("Valid Directory Chosen:", valid)
                # Stores the filtration method used to form the persistence diagram for later use.
                filt_method = pcpds_temp.get_filtration_used()
                # Stores the leading zeros here based on the directory name.
                break
            else:
                valid = False
                print("\nNo persistance diagram present for files @ collection:", pfm.get_path_manager().get_full_cur_dir() + ".\n")
                print("Please Either enter a directory that has been filtrated for persistance diagrams or run 'generate_persistance_diagrams.py' on the collection.")
        else:
            print("Problem loading pcpds file, it loaded as None.")

    wb = Workbook()
    excel_sheet = wb.add_sheet('Sheet 2')

    # Grabs the leading_zeros variable using X from a random idx's cell_ID.
    tmp_cellID = pfm.get_random_pcpds().get_cellID()
    leading_zeros = int((len(str(tmp_cellID))-1)/3)

    print("LEADING ZEROS:", leading_zeros)
    for n in range(number_of_data):

        pcpds = None

        valid_idx = False
        while valid_idx == False:

            # Grabs a random pcpds from the currently selected directory.
            pcpds = pfm.get_random_pcpds()
            (X, Y, Z) = pcpds.get_xyz()

            print("XYZ of random pcpds: Z", X, "Y:", Y, "Z:", Z)
            # Do this to check for if we are on a lower bound to avoid errors from negative values.
            if X < 1 or Y < 1:
                print("Invalid XYZ")
                continue

            slide_left_X = pfm.gen_idx(X-1, Y, leading_zeros)
            slide_right_X = pfm.gen_idx(X+1, Y, leading_zeros)
            slide_up_Y = pfm.gen_idx(X, Y+1, leading_zeros)
            slide_down_Y = pfm.gen_idx(X, Y-1, leading_zeros)
            slide_left_down = pfm.gen_idx(X-1, Y-1, leading_zeros)
            slide_right_down = pfm.gen_idx(X+1, Y-1, leading_zeros)
            slide_right_up = pfm.gen_idx(X+1, Y+1, leading_zeros)
            slide_left_up = pfm.gen_idx(X-1, Y+1, leading_zeros)

            if pfm.get_path_manager().validate_file(os.path.join(pfm.get_collection_dir(), str(slide_left_X) +".json")) == True:
                if pfm.get_path_manager().validate_file(os.path.join(pfm.get_collection_dir(), str(slide_right_X) +".json")) == True:
                    if pfm.get_path_manager().validate_file(os.path.join(pfm.get_collection_dir(), str(slide_up_Y) +".json")) == True:
                        if pfm.get_path_manager().validate_file(os.path.join(pfm.get_collection_dir(), str(slide_down_Y) +".json")) == True:
                            valid_idx = True

        # Get the random pcpds's details
        idx = pcpds.get_cellID()
        print("Random IDX chosen:", str(idx))
        (dimX, dimY, dimZ) = pcpds.get_dimensions()
        bounds = pcpds.get_bounds()

        # Grab persistance diagram of random idx.
        test_pd = pcpds.get_persistance_diagram()

        # TODO: Change how Validation of these slid idx values is done?
        slide_left_X = pfm.get_pcpds(slide_left_X)
        slide_right_X = pfm.get_pcpds(slide_right_X)
        slide_up_Y = pfm.get_pcpds(slide_up_Y)
        slide_down_Y = pfm.get_pcpds(slide_down_Y)

        num_slides = 10
        num_directions = 4
        #results = [0]*(num_slides * num_partitions_to_slide)
        excel_sheet.write(0, n, str(idx))

        # Applies transform to point cloud and generates a persistence diagram to compare for bottleneck distances.
        print("num_slides * num_partitions_to_slide:",num_slides * num_partitions_to_slide)
        for overlay in range(1, num_slides * num_partitions_to_slide):

            # Left
            bounds_left_X = menu.transform(bounds, dimX, -1, True, overlay, num_slides)
            left_X_pcpds = menu.within_point_cloud(pcpds, slide_left_X, bounds_left_X)

            # Right
            bounds_right_X = menu.transform(bounds, dimX, 1, True, overlay, num_slides)
            right_X_pcpds = menu.within_point_cloud(pcpds, slide_right_X, bounds_right_X)

            # Up
            bounds_up_Y = menu.transform(bounds, dimY, 1, False, overlay, num_slides)
            up_Y_pcpds = menu.within_point_cloud(pcpds, slide_up_Y, bounds_up_Y)

            # Down
            bounds_down_Y = menu.transform(bounds, dimY, -1, False, overlay, num_slides)
            down_Y_pcpds = menu.within_point_cloud(pcpds, slide_down_Y, bounds_down_Y)

            overlay_avg = -1
            num_dir = 0
            sum = 0

            try:
                left_X_pcpds = filt_method(left_X_pcpds)
                left_X_pd = left_X_pcpds.get_persistance_diagram()
                sum = sum + bottleneck_distances.get_distances(left_X_pd, test_pd)
                num_dir = num_dir + 1
            except:
                print("ERROR LEFT")
                right_bn = 0

            try:
                right_X_pcpds = filt_method(right_X_pcpds)
                right_X_pd = right_X_pcpds.get_persistance_diagram()
                sum = sum + bottleneck_distances.get_distances(right_X_pd, test_pd)
                num_dir = num_dir + 1
            except:
                print("ERROR RIGHT")
                right_bn = 0

            try:
                up_Y_pcpds = filt_method(up_Y_pcpds)
                up_Y_pd = up_Y_pcpds.get_persistance_diagram()
                sum = sum + bottleneck_distances.get_distances(up_Y_pd, test_pd)
                num_dir = num_dir + 1
            except:
                print("ERROR UP")
                up_bn = 0

            try:
                down_Y_pcpds = filt_method(down_Y_pcpds)
                down_Y_pd = down_Y_pcpds.get_persistance_diagram()
                sum = sum + bottleneck_distances.get_distances(down_Y_pd, test_pd)
                num_dir = num_dir + 1
            except:
                print("ERROR DOWN")
                down_bn = 0


            if (num_dir != 0):
                overlay_avg = sum / num_dir
            else:
                overlay_avg = -1
            excel_sheet.write(overlay, n, str(overlay_avg))

        menu.progress(n, number_of_data, ("Processing random grid: "+str(idx)+"..."))
    menu.progress(1, 1, ("Processing complete."))
    # Write results .xls file
    wb.save(dir_name + '.xls')
    print("Job done.")

# Do Main
if __name__ == '__main__':
    main()
