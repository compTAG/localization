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
    
    print("Success")
    # TODO: try and use iterator to go through every pcpds file?
    # TODO: Add filter for '.json' objects as it will have problems on macs otherwise?
    
    # TOOD: FOR MULTITHREADING: Use this iterator only to pass off the processing tasks to each avalible thread!
    for file in os.listdir(pcpds_manager.get_path_manager().get_full_cur_dir_var(collection)):
         # Hand off pcpds object here to multithread function
         print("File_Name:", file)
         file_path = os.path.join(pcpds_manager.get_path_manager().get_full_cur_dir(), file)
         print("File_Path:", file_path)
         pcpds_obj = file_manager.load(file_path)
         
         # TODO: Add capabilitiy to select filtration method using abstract functino stuff.
         temp = Filtration.get_rips_diagram(pcpds_obj)
         file_manager.save(pcpds_obj, pcpds_manager.get_path_manager().get_full_cur_dir(), pcpds_obj.get_cellID())
         print(file, "Saved.")
         
         # TODO: Add progress bar?
         # menu.progress()

generate_persistance_diagrams()