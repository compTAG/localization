from Classes.filtrations import Filtration
from Classes.menu import menu
from Classes.PCPDS_manager import PCPDS_Manager
import Classes.file_manager as file_manager
import os

# This file targets a directory with pcpds files stored inside and generates their persistance diagram.

def generate_persistance_diagrams():
    
    pcpds_manager = PCPDS_Manager()
    
    # List the directories
    
    # Ask for the directory
    print("Enter the Collection of pcpds objects you wish to generate persistance diagramsfor.")
    collection = menu.get_input("Directory: ")
    
    pcpds_manager.get_path_manager().set_cur_dir(collection)
    
    valid = pcpds_manager.get_collection_dir()
    while(not valid):
        print("Invalid collection name:", pcpds_manager.get_path_manager().get_cur_dir() ,"try again.", valid)
        collection = menu.get_input("Directory: ")
        pcpds_manager.get_path_manager().set_cur_dir(collection)
        valid = pcpds_manager.get_collection_dir()
    
    # Verify the directory
    
    print("Valid Directory Confirmed:", pcpds_manager.get_path_manager().get_full_cur_dir())
    
    # Loop for choosing filtration method:
    print("Choose a filtration method: [0] Rips, [1] Upper Star, [2] Lower Star.")
    choice = menu.get_int_input()
    while not (choice < 3 and choice > -1):
        print("Please enter a valid number between 0-2.")
        choice = menu.get_int_input()
    
    # Selects the filter function to be used.
    filter = None
    if choice is 0:
        filter = Filtration.get_rips_diagram
    elif choice is 1:
        filter = Filtration.get_upper_star
    elif choice is 2:
        filter = Filtration.get_lower_star
        
    # TODO: Add filter for '.json' objects as it will have problems on macs otherwise?
    
    # TOOD: FOR MULTITHREADING: Use this iterator only to pass off the processing tasks to each avalible thread!
    for file in os.listdir(pcpds_manager.get_path_manager().get_full_cur_dir_var(collection)):
         # TODO: Hand off pcpds object here to multithread function
         
         print("File_Name:", file)
         file_path = os.path.join(pcpds_manager.get_path_manager().get_full_cur_dir(), file)
         print("File_Path:", file_path)
         pcpds_obj = file_manager.load(file_path)
         
         # TODO: Add capabilitiy to select filtration method using abstract functino stuff.
         result = filter(pcpds_obj)
         file_manager.save(result, pcpds_manager.get_path_manager().get_full_cur_dir(), pcpds_obj.get_cellID())
         print(file, "Saved.")
         
         # TODO: Add progress bar?
         # menu.progress()

generate_persistance_diagrams()