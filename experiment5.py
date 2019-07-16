from Classes.process_las import ProcessLas
import Classes.PCPDS
from Classes.bottleneck_dist import BottleneckDistances
from Classes.menu import menu as order_menu
from Classes.PCPDS_manager import PCPDS_Manager
import Classes.file_manager as file_manager

def main():

    number_of_data = 400
    # Create las object and calculate corresponding values
    las_obj = ProcessLas('small', 7, len(str(7)))

    # Makes a string of the folder path, os.path.join makes it compatible
    # between macs, windows, and linux
    dir_name = file_manager.make_folder(filename, partition)

    pfm = PCPDS_Manager()
    dir_name = pfm.generate_collection(filename, partition)
    print('Dir:' + str(dir_name))

    las_obj.input_las(dir_name)
    datafile = open("bdripson7partitions.txt", "a")

    randidx = menu.random_idx_normal

    for _ in range(number_of_data):
        search_idx = randidx(dir_name)
        # search_pcpds = load pcpds with search_idx
        searchfilt = search_pcpds.get_persistance_diagram()
        datafile.write(search_idx)
        datafile.write(":")
        bd_idx = search_distances(10, searchfilt, collection_path):
        for bd, idx in bd_idx:
            datafile.write(idx)
            datafile.write(",")
            datafile.write(bd)
            datafile.write(",")
        datafile.write('\n')


# Do Main
if __name__ == '__main__':
    main()
