import random
import numpy as np
from Classes.process_las import ProcessLas
import Classes.PCPDS as pcpds
from Classes.menu import menu as menu
from Classes.PCPDS_manager import PCPDS_Manager
import Classes.file_manager as file_manager
import Classes.bottleneck_dist as bottleneck_distances

def main():
    number_of_data = 12
    # Create las object and calculate corresponding values
    filename = 'tiny'
    partition = 30
    las_obj = ProcessLas(filename, partition)

    # Makes a string of the folder path, os.path.join makes it compatible
    # between macs, windows, and linux
    dir_name = file_manager.make_folder(filename)

    pfm = PCPDS_Manager()
    dir_name = pfm.generate_collection(filename, partition)
    print('Dir:' + str(dir_name))

    las_obj.input_las(dir_name)
    datafile = open("noise_to_bd2.txt", "a")
    relative_std_dev = 0.001
    while relative_std_dev < 1:
        for _ in range(number_of_data):
            #get random PCPDS
            rand_pcpds = pfm.get_random_pcpds()
            test_idx = rand_pcpds.get_cellID()
            # init a noise added pcpds object
            noise_idx = 'noise'+str(test_idx)
            noise_pcpds = pcpds.PCPDS(noise_idx)
            # make noise pointcloud
            A = rand_pcpds.get_point_cloud()
            sigma = relative_std_dev * (1/partition)
            B = np.random.normal(0, sigma, 3)
            i = 0
            while True:
                noise = np.random.normal(0, sigma, 3)
                B = np.vstack((noise,B))
                i += 1
                if i >= len(A) - 1:
                    break
            C = B + A
            noise_pcpds.set_point_cloud(C)
            temp1 = rand_pcpds.get_point_cloud()
            print(temp1)
            temp = noise_pcpds.get_point_cloud()
            print(temp)
            print('\n\n\n\n')
            noise_pcpds.generate_persistance_diagram()
            #write the test idx and relative std dev to datafile
            datafile.write(str(test_idx))
            datafile.write(":")
            datafile.write(str(relative_std_dev))
            datafile.write(",")
            # Calculate bottleneck distance
            bd = bottleneck_distances.get_distances(noise_pcpds.get_persistance_diagram(),rand_pcpds.get_persistance_diagram())
            datafile.write(str(bd))
            datafile.write("\n")
        relative_std_dev += 0.001

# Do Main
if __name__ == '__main__':
    main()
