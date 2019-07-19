from Classes.menu import menu
from Classes.PCPDS_manager import PCPDS_Manager
import Classes.file_manager as file_manager
import os.path

# This computes the bottleneck distance using a pre-processed/filtrated collection

pcpds_manager = PCPDS_Manager()

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
    
print("Ready to process")
        


# Option to force it?

# Catch error where pcpds objects arn't fully processed & Tell the user to re run the process and let it finish this time.