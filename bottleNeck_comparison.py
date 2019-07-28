from Classes.menu import menu
from Classes.PCPDS_manager import PCPDS_Manager
import Classes.bottleneck_dist as bottleneck_distances
import Classes.file_manager as file_manager
import Classes.modifiers as modifiers
import os.path
from os import walk
from xlwt import Workbook


def choose_pcpds(pm):
    # Asks the user if they want to specify a pcpds or select a random one.
    print("Enter a specific pcpds number, or enter 'R' for a random one.")
    specification = menu.get_input("PCPDS Num:")
    
    pcpds = None
    valid_pcpds_found = False

    while not valid_pcpds_found:
        try:
            pcpds_num = int(specification)
            # Attempt to load in specified pcpds
            try:
                pcpds = pm.get_pcpds(specification)
                valid_pcpds_found = True
                break
            except:
                # Dosen't exist?
                print("pcpds file for cell_ID:", specification, "dosen't exist.")
        except:
            
            if specification.lower() == "r":
                pcpds = pm.get_random_pcpds()
                valid_pcpds_found = True
                break
                print(specification)
            else:
                print("Invalid pcpds format entered.")
        specification = menu.get_input("PCPDS Num:")
    return pcpds

def modify_pcpds(pcpds):
    modifications = []

    print("What modification would you like to apply to the pcpds object?")
    print("[0] None, [1] Rotation, [2] Add Noise.")
    choice = menu.get_int_input()
    if choice is 0:
        pass
    elif choice is 1:
        print("Rotation theta for X axis:")
        x = menu.get_float_input()
        print("Rotation theta for Y axis:")
        y = menu.get_float_input()
        print("Rotation theta for Z axis:")
        z = menu.get_float_input()
        pcpds = modifiers.rotate_section(pcpds, x, y, z)
        modifications.append("Rotated by: X-theta; " + str(x) + " Y-theta; " + str(y) + " Z-theta; " + str(z))
    elif choice is 2:
        print("Add the Sigma value for noise:")
        sigma = menu.get_float_input()
        pcpds = modifiers.add_noise(pcpds, sigma)
        modifications.append("Noise Applied. Sigma:", sigma)
    else:
        print("Invalid option.")

    if len(modifications) > 0:
        print("Regenerating Persistance Diagram for altered pcpds...")
        pcpds = pcpds.get_filtration_used()(pcpds)

    return pcpds, modifications

# This computes the bottleneck distance using a pre-processed/filtrated collection

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
pcpds = choose_pcpds(pcpds_manager)
print("PCPDS Selected:", pcpds.get_cellID())
pcpds, mods = modify_pcpds(pcpds)

# Calculated closest n matching bottleneck distances.
closest_matches  = bottleneck_distances.search_distances(n_results, pcpds.get_persistance_diagram(), valid)

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
    
wb.save(os.path.join("results", pcpds_manager.get_path_manager().get_cur_dir())+"-"+file_end_tag + '.xls')
print("Results saved as Excel file.")