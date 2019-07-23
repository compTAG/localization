import time
import multiprocessing
from Classes.filtrations import Filtration
from Classes.menu import menu
from Classes.PCPDS_manager import PCPDS_Manager
import Classes.file_manager as file_manager
import os

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
    start_time = time.time()
    
    # TODO: Add filter for '.json' objects as it will have problems on macs otherwise?
    
    # TOOD: FOR MULTITHREADING: Use this iterator only to pass off the processing tasks to each avalible thread!
    for file in os.listdir(pcpds_manager.get_path_manager().get_full_cur_dir_var(collection)):
        # Sets up the process
        process = multiprocessing.Process(target=generate_persistence_diagram, args=(pcpds_manager, file, filter))
        process.start()
        process.join()
        process.terminate()
        
    print("Finished filtrating persistance diagrams for files in: ", str(time.time() - start_time))

def pool_run():
     
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
    start_time = time.time()
    
    # TODO: Add filter for '.json' objects as it will have problems on macs otherwise?
    
    # TODO: set to the number of items we think the cpu should handle at a time based on total cpu count.
    pool_size = 10
    process_pool = []
    pool = multiprocessing.Pool()
    for file in os.listdir(pcpds_manager.get_path_manager().get_full_cur_dir_var(collection)):
        # Build a process pool 
        process_pool.append(file)
        if(len(process_pool) >= pool_size):
            # send the process pool to a cpu
            # TODO: Need a better way of passing in arguements to make using this method justifiable when I can't gaurentee it's time complexity will be beter.
            pool.map(generate_persistence_diagram, process_pool, args(pcpds_manager, file, filter))
            # Empty pool for next set.
            process_pool.clear()
            pool.close()
    
    # finish processing the items left in process pool
        
    print("Finished filtrating persistance diagrams for files in: ", str(time.time() - start_time))


def run():
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
    start_time = time.time()
    
    # TODO: Add filter for '.json' objects as it will have problems on macs otherwise?
    for file in os.listdir(pcpds_manager.get_path_manager().get_full_cur_dir_var(collection)):
        generate_persistence_diagram(pcpds_manager, file, filter)
        
    print("Finished filtrating persistance diagrams for files in: ", str(time.time() - start_time), "s")
    
def generate_persistence_diagram(pcpds_manager, file, filteration):
        
    file_path = os.path.join(pcpds_manager.get_path_manager().get_full_cur_dir(), file)
    pcpds_obj = file_manager.load(file_path)
        
    # TODO: Add capabilitiy to select filtration method using abstract function stuff.
    result = filteration(pcpds_obj)
    file_manager.save(result, pcpds_manager.get_path_manager().get_full_cur_dir(), pcpds_obj.get_cellID())
    print(file, "filtrated & Saved.")
    
run()