from Classes.menu import menu
from Classes.PCPDS_manager import PCPDS_Manager
import Classes.bottleneck_dist as bottleneck_distances
import Classes.file_manager as file_manager
import Classes.modifiers as modifiers
import os.path
from os import walk
from xlwt import Workbook

def modify_pcpds(pcpds, choice, args):
    modifications = []

    if choice is 0:
        pass
    elif choice is 1:
        x = args[0]
        y = args[1]
        z = args[2]
        pcpds = modifiers.rotate_section(pcpds, x, y, z)
        modifications.append("Rotated by: X-theta; " + str(x) + " Y-theta; " + str(y) + " Z-theta; " + str(z))
    elif choice is 2:
        print("Add the Sigma value for noise:")
        sigma = args[0]
        pcpds = modifiers.add_noise(pcpds, sigma)
        modifications.append("Noise Applied. Sigma:", sigma)
    else:
        print("Invalid option.")

    if len(modifications) > 0:
        print("Regenerating Persistance Diagram for altered pcpds...")
        pcpds = pcpds.get_filtration_used()(pcpds)

    return pcpds, modifications

def compute_bottle_neck_dist():
    
    # This computes the bottleneck distance using a pre-processed/filtrated collection for all idx values in a directory.

    pcpds_manager = PCPDS_Manager()
    print("Collections:")
    collections_string = ""
    collections =  os.listdir(pcpds_manager.get_path_manager().get_collections_path())
    collections.sort()
    for directory in collections:
        collections_string += directory + " \t"
    print(collections_string)
    print("Please enter a collection that has already been filtrated:")

    # Loop here for valid directory
    collection = menu.get_input("Directory: ")
        
    pcpds_manager.get_path_manager().set_cur_dir(collection)
        
    valid = pcpds_manager.get_collection_dir()
    while(True):
        
        # If not a valid directory, ask again saying it is invalid
        while(not valid):
            if not pcpds_manager.get_collection_dir():
                print("Invalid collection name:", pcpds_manager.get_path_manager().get_cur_dir() ,"try again.")
            collection = menu.get_input("Directory: ")
            pcpds_manager.get_path_manager().set_cur_dir(collection)
            valid = pcpds_manager.get_collection_dir()
        
        # Checks the first pcpds object in this directory for if it has a persistance diagram
        pcpds_temp = None
        for file in os.listdir(pcpds_manager.get_path_manager().get_full_cur_dir_var(collection)):
            file_path = os.path.join(pcpds_manager.get_path_manager().get_full_cur_dir(), file)
            pcpds_temp = file_manager.load(file_path)
            break
        if pcpds_temp is not None:
            if pcpds_temp.get_persistance_diagram() is not None:
                print("Valid Directory Chosen:", valid)
                break
            else:
                valid = False
                print("\nNo persistance diagram present for files @ collection:", pcpds_manager.get_path_manager().get_full_cur_dir() + ".\n")
                print("Please Either enter a directory that has been filtrated for persistance diagrams or run 'generate_persistance_diagrams.py' on the collection.")
        else:
            print("Problem loading pcpds file, it loaded as None.")
        
    print("Ready to process, how manny n_nearest results would you like?")

    # TODO: Validate that n_results is a valid number for the current dataset.
    n_results = menu.get_int_input()

    # Choose a modifier and apply it here
    print("What modification would you like to apply to the pcpds object?")
    print("[0] None, [1] Rotation, [2] Add Noise.")
    choice = menu.get_int_input()
    args = []
    if choice is 0:
        pass
    elif choice is 1:
        print("Rotation theta for X axis:")
        args.append(menu.get_float_input())
        print("Rotation theta for Y axis:")
        args.append(menu.get_float_input())
        print("Rotation theta for Z axis:")
        args.append(menu.get_float_input())
    elif choice is 2:
        print("Add the Sigma value for noise:")
        args.append(menu.get_float_input())
    else:
        print("Invalid option.")
        
    # TODO: Apply choice on all pcpds objects!
    # TODO: Chose a modifier to apply to all?
    # INSTEAD OF: choosing one, use all in dir.
    for file in file_manager.find_files(pcpds_manager.get_collection_dir(), '.json'):
        pcpds = file_manager.load(os.path.join(pcpds_manager.get_collection_dir(), file))
        print("PCPDS Selected:", pcpds.get_cellID())
        pcpds, mods = modify_pcpds(pcpds, choice, args)

        # Calculated closest n matching bottleneck distances.
        closest_matches = bottleneck_distances.search_distances(n_results, pcpds.get_persistance_diagram(), valid)

        wb = Workbook()
        excel_sheet = wb.add_sheet('Bottle_Neck_Distance_Comparison')

        excel_sheet.write(0, 0, "Closest_" + str(n_results) + "_BD_Matches")
        excel_sheet.write(0, 1, "Bottle_Neck_Distance")

        excel_sheet.write(0, 2, "Cell_ID_Compared_Against:")
        excel_sheet.write(1, 2, pcpds.get_cellID())

        if len(mods) > 0:
            excel_sheet.write(0, 3, str(pcpds.get_cellID())+" Modifications")
            iter = 1
            for mod in mods:
                excel_sheet.write(iter, 3, mod)
                iter+=1

        iter = 1
        for idx in closest_matches:
            
            # Write results .xls file
            excel_sheet.write(iter, 0, idx[0][:-5])
            excel_sheet.write(iter, 1, idx[1])
            iter = iter + 1

        # Adds a tag to make the file name more unique to avoid mindlessly over writing data
        file_end_tag = str(pcpds.get_cellID())
        if len(mods) > 0:
            file_end_tag += ":" + mods[0]
        
        wb.save(os.path.join("results", pcpds_manager.get_path_manager().get_cur_dir())+"-"+file_end_tag + ":" + pcpds.get_filtration_used_name() + '.xls')
        print("Results saved as Excel file.")

compute_bottle_neck_dist()