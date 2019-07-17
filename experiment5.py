import random
from Classes.process_las import ProcessLas
import Classes.PCPDS
from Classes.menu import menu as menu
from Classes.PCPDS_manager import PCPDS_Manager
import Classes.file_manager as file_manager
import Classes.bottleneck_dist as bottleneck_distances

def main():

    number_of_data = 400
    # Create las object and calculate corresponding values
    filename = 'small'
    partition = 700
    las_obj = ProcessLas(filename, partition)

    # Makes a string of the folder path, os.path.join makes it compatible
    # between macs, windows, and linux
    dir_name = file_manager.make_folder(filename)

    pfm = PCPDS_Manager()
    dir_name = pfm.generate_collection(filename, partition)
    print('Dir:' + str(dir_name))

    las_obj.input_las(dir_name)
    datafile = open("bdripson70partitions.txt", "a")

    #import functions
    m = menu(partition, las_obj)

    for _ in range(number_of_data):
        #[test_idx, guess_grid] = m.random_idx_normal(dir_name)
        rand_pcpds = pfm.get_random_pcpds()
        test_idx = rand_pcpds.get_cellID()
        
        nearest_results = 12
        
        # TODO: make loading bar for guess_grid
        guess_grid  = bottleneck_distances.search_distances(nearest_results, rand_pcpds.get_persistance_diagram(), dir_name)
        
        datafile.write(str(test_idx))
        datafile.write(":")
        
        pass_string = ''
        # Calculate bottleneck distance, print n_result matches
        for idx in guess_grid:
            datafile.write(str(idx))
            print(idx)
            datafile.write(",")
        datafile.write('\n')

        print("Job done.")

# Do Main
if __name__ == '__main__':
    main()
