# This file tests if all the pcpds objects in a dorectory have the same filtration method saved.

import os
from Classes.PCPDS_manager import PCPDS_Manager
import Classes.file_manager as file_manager
from Classes.menu import menu

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
        
# Go through the pcpds objects in the dir & check that their filtration method is the same

iter = 0
filtration_name = None
files = file_manager.find_files(pcpds_manager.get_collection_dir(), '.json')
menu.progress(iter, 1, "Checking for filtration mismatches...")

for file in files:
    pcpds = file_manager.load(os.path.join(pcpds_manager.get_collection_dir(), file))
    
    if filtration_name is None:
        filtration_name = pcpds.get_filtration_used_name()
        
    if filtration_name in pcpds.get_filtration_used_name():
        pass
        #print("PCPDS:", pcpds.get_cellID(), " is Valid. Filtration:", filtration_name)
    else:
        print("INVALID PCPDS:", pcpds.get_cellID(), "Missmatched Filtration:", pcpds.get_filtration_used_name())
        
    iter += 1
    menu.progress(iter, len(files), "Checking for filtration mismatches for:"+str(pcpds.get_cellID()))

print("Finished Validating Filtrations:", filtration_name)