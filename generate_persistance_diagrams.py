import Classes.filtrations as Filtration
from Classes.menu import menu
from Classes.PCPDS_manager import PCPDS_Manager
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
    while(valid is not False):
        print("Invalid collection name:", # PUT FILE NAME HERE ,"try again.")
        collection = menu.get_input("Directory: ")
        pcpds_manager.get_path_manager().set_cur_dir(collection)
        valid = pcpds_manager.get_collection_dir()
    
    # Verify the directory
    
    # TODO: Figure out a good way of iterating through files in a directory to load files
    for entry in os.listdir('/home/geoengel/Documents/Undergraduate Research/localization/cell_collection/small_70_2019-07-18/'):
         print(entry)
         
    # Generates and sets the persistance diagram
    #temp = Filtration.get_rips_diagram(pcpds_obj)

generate_persistance_diagrams()