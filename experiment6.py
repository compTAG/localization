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
    m = menu(partition, las_obj)

    for n in range(number_of_data):

        [test_pcpds, test_idx] = random_test_grid(collection_path)

        (X, Y, Z) = test_pcpds.get_xyz(test_idx)
        (dimX, dimY) = test_pcpds.get_dimensions()
        

        results = []

        pcpds_manager = PCPDS_Manager()

        #Change this to loop over X+-1 and Y+-1, check exists
        slide_pcpds = pcpds_manager.get_pcpds(las_obj.find_idx(X+1, Y))

        #Add for loop over 0.1 to 1 and to bottleneck distance to average in results
        for overlay in range(10):
            begin_X = (float(overlay)/10.0 * dimX) + (dimX * X)
            end_X = (float(overlay)/10.0 * dimX) + (dimX * X) + dimX

            for pc in test_pcpds.point_cloud:
                #if point is within bounds of beginX and endX regardless of Y coord, add to temp_pcpds
                pass

            for pc in slide_pcpds.point_cloud:
                #if point is within bounds of beginX and endX regardless of Y coord, add to temp_pcpds
                pass

            temp_pd = temp_pcpds.get_persistence_diagram()
            test_pd = test_pcpds.get_persistence_diagram()
            results[overlay] = bottleneck_distances.get_distances(temp_pd, test_pd)#bottleneck temp_pcpds against test_pcpds

        #Repeat above for X-1, Y+-1

        # Calculate bottleneck distance, print n_result matches

        datafile.write(str(test_idx))
        datafile.write(":")

        pass_string = ''
        # Calculate bottleneck distance, print n_result matches
        for idx in guess_grid:
            datafile.write(str(idx))
            print(idx)
            datafile.write(",")
        datafile.write('\n')

        m.progress(n, number_of_data, ("Processing random grid: "+str(test_idx)+"..."))

    print("Job done.")

# Do Main
if __name__ == '__main__':
    main()
