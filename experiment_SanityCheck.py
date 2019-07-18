import random
from Classes.process_las import ProcessLas
import Classes.PCPDS
from Classes.menu import menu as menu
from Classes.PCPDS_manager import PCPDS_Manager
import Classes.file_manager as file_manager
import Classes.bottleneck_dist as bottleneck_distances
import os.path

def main():

    number_of_data = 400
    # Create las object and calculate corresponding values
    filename = 'tiny'
    partition = 70
    las_obj = ProcessLas(filename, partition)

    pfm = PCPDS_Manager()
    dir_name = pfm.generate_collection(filename, partition)
    print('Dir:' + str(dir_name))

    las_obj.input_las(dir_name)
    datafile = open("bdripson70partitions.txt", "a")

    #import functions
    n_results = 4 # menu.get_n_result_input()

    for n in range(number_of_data):

        # Generates random idx value for pcpds object
        random_idx = str(las_obj.random_grid())
        
        random_pcpds  = None
        first = True
        # TODO: Validate the idx from random_grid is valid, else run random_grid again.
        # Generate & validate a random_pcpds to use.
        while(not pfm.get_path_manager().validate_file(os.path.join(dir_name, random_idx+".json")) or first):
            random_idx = str(las_obj.random_grid())
            print("Attempting RANDOM ID:", random_idx)
            first = False
               
        # Grabs the pcpds object that was generated
        random_pcpds = pfm.get_pcpds(random_idx) 
        # Calculate bottleneck distance, print n_result matches
        closest_matches  = bottleneck_distances.search_distances(n_results, random_pcpds.get_persistance_diagram(), dir_name)

        datafile.write(str(random_idx))
        datafile.write(":")

        # Calculate bottleneck distance, print n_result matches
        for idx in closest_matches:
            datafile.write(str(idx))
            print(idx)
            datafile.write(",")
        datafile.write('\n')

        menu.progress(n, number_of_data, ("Processing random grid: "+str(random_idx)+"..."))

    print("Job done.")

# Do Main
if __name__ == '__main__':
    main()
