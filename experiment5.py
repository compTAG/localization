from Classes.process_las import ProcessLas
import Classes.PCPDS
from Classes.bottleneck_dist import BottleneckDistances
from Classes.menu import menu as menu
from Classes.PCPDS_manager import PCPDS_Manager
import Classes.file_manager as file_manager

def main():

    number_of_data = 400
    # Create las object and calculate corresponding values
    filename = 'small'
    partition = 7
    las_obj = ProcessLas(filename, partition)

    # Makes a string of the folder path, os.path.join makes it compatible
    # between macs, windows, and linux
    dir_name = file_manager.make_folder(filename)

    pfm = PCPDS_Manager()
    dir_name = pfm.generate_collection(filename, partition)
    print('Dir:' + str(dir_name))

    las_obj.input_las(dir_name)
    datafile = open("bdripson7partitions.txt", "a")

    #import functions
    randidx = menu.__random_test_grid
    search_distances = BottleneckDistances.search_distances

    for _ in range(number_of_data):
        search_idx = randidx(dir_name)
        search_pcpds = file_manager.load(pfm.get_file_path(search_idx)) # load pcpds with search_idx
        searchfilt = search_pcpds.get_persistance_diagram()
        datafile.write(search_idx)
        datafile.write(":")
        bd_idx = search_distances(10, searchfilt, collection_path)
        for bd, idx in bd_idx:
            datafile.write(idx)
            datafile.write(",")
            datafile.write(bd)
            datafile.write(",")
        datafile.write('\n')


# Do Main
if __name__ == '__main__':
    main()
