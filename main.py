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

    #TODO: Continue with files
    # compare bottlenecks


if __name__ == '__main__':
    main()
