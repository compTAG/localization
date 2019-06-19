from ProcessLas import input_las
import PCPDS
import DoRips
import numpy as np
import os

def main():
    dim = int(input("Enter Partition Count (1D): "))
    filename = input("Enter the name of the file you'd wish to import: ")

    leadingZeros = len(str(dim))
    test = format(1, str(leadingZeros))
    idx = int(str(test) + str(test) + str(test))

    exists = os.path.isfile(concatenate('/path/to/', idx, **)) #where ** is file ext
    if exists:
        # Continue (do nothing here)
    else:
        input_las(filename, dim)

        #Load files and compute point clouds
        for x in range(dim):
            y = 0
            for y in range(dim):
                z = 0
                for z in range(dim):
                    #Create PCPDS
                    # Compute persistence for point cloud

    # compare bottlenecks


if __name__ == '__main__':
    main()

#make folder with filename and timestamp and save partitions
