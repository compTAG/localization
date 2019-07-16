import random
from Classes.process_las import ProcessLas
import Classes.PCPDS
from Classes.menu import menu as menu
from Classes.PCPDS_manager import PCPDS_Manager
import Classes.file_manager as file_manager

def main():

    number_of_data = 400
    # Create las object and calculate corresponding values
    filename = 'tiny'
    partition = 70
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
    m = menu(partition, las_obj, dir_name)

    print("COLLECTION VAR:", pfm.get_path_manager().get_cur_dir(), "Collection path:", pfm.get_collection_dir())

    for _ in range(number_of_data):
        #search_idx = randidx(dir_name)
        #search_pcpds = file_manager.load(pfm.get_file_path(search_idx)) # load pcpds with search_idx
        #searchfilt = search_pcpds.get_persistance_diagram()
        [test_idx, guess_grid] = m.random_idx_normal(dir_name)
        datafile.write(test_idx)
        datafile.write(":")
        for bd, idx in bd_idx:
            datafile.write(str(guess_grid[idx]))
            datafile.write(",")
            datafile.write(bd)
            datafile.write(",")
        datafile.write('\n')


# Do Main
if __name__ == '__main__':
    main()
