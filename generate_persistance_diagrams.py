# import time
import multiprocessing
from Classes.filtrations import Filtration
from Classes.menu import menu
from Classes.PCPDS_manager import PCPDS_Manager
import Classes.file_manager as file_manager
import os
import concurrent.futures

# This file's purpose is to process already generated pcpds object's point clouds into persistance diagrams.

def process_run():
     
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
        
    # Start timer
    # start_time = time.time()
    
    print("Would you like to use multi-processing to attempt to speed things up? [0] No. [1] Yes.")
    print("Please do note that using multiprocessing only speeds up the generation of persistance diagrams with larger point clouds.")
    multiproc = menu.get_int_input()
    
    if(multiproc):
        with concurrent.futures.ProcessPoolExecutor as executor:
            for file in os.listdir(pcpds_manager.get_path_manager().get_full_cur_dir_var(collection)):
                # Sets up the process
                generate_persistence_diagram(pcpds_manager, file, filter)
                # process = multiprocessing.Process(target=generate_persistence_diagram, args=(pcpds_manager, file, filter))
                # process.start()
                # process.join()
                # process.terminate()
            
    else:
        print("NOT MULTIPROCESSING:")
        # Process the point clouds into persistance diagrams without using multiprocessing
        files = os.listdir(pcpds_manager.get_path_manager().get_full_cur_dir_var(collection))
        iter = 0
        for file in files:
            menu.progress(iter, len(files), ("Generating persistance diagram for:"+str(file)))
            generate_persistence_diagram(pcpds_manager, file, filter)
            iter += 1
        menu.progress(1, 1, "Generating persistance diagrams completed.")
        
    # print("Finished filtrating persistance diagrams for files in: ", str(time.time() - start_time))

def generate_persistence_diagram(pcpds_manager, file, filteration):
        
    file_path = os.path.join(pcpds_manager.get_path_manager().get_full_cur_dir(), file)
    pcpds_obj = file_manager.load(file_path)
        
    # TODO: Add capabilitiy to select filtration method using abstract function stuff.
    result = filteration(pcpds_obj)
    file_manager.save(result, pcpds_manager.get_path_manager().get_full_cur_dir(), pcpds_obj.get_cellID())
    # print(file, "filtrated & Saved.")
    
process_run()