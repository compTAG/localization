import ProcessLas
import PCPDS
import DoRips
import numpy as np
import os

def main():

    dim = 0
    while (dim%1) != 0:
        dim = int(input("Enter Partition Count (1D): "))
        if (dim%1) != 0:
            print('Please enter a whole number.')
    filename = input("Enter the name of the file you'd wish to import: ")

    # Create las object and calculate corresponding values
    lasObj = ProcessLas(filename, dim, len(str(dim)))
    #test = format(1, str(leadingZeros))
    idx = int(str(test) + str(test) + str(test))

    # Check if the final persistence diagram for the las object doesn't exist
    if !ProcessLas.checkFile(lasObj, idx, '**'): #Where ** is the extention of persistence diagrams
        #Check if the file exists
        if ProcessLas.checkFile(lasObj, null, '.las'):
            # Saves the persistence diagrams of each grid
            ProcessLas.inputLas(lasObj)

        else:
            # Print error
            print('Error, no matching file found.')
            exit()



    # compare bottlenecks


if __name__ == '__main__':
    main()

#make folder with filename and timestamp and save partitions
