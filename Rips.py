# very broken and not operational. This is just where I was playing with some code.

from laspy.file import File
import numpy as np
from dionysus import *
import Rips
from    sys         import argv, exit



def PairwiseDistances(points):
    pass


def get_points():
    inFile = File('test.las', mode='r')

    Xvals = inFile.X
    Yvals = inFile.Y
    Zvals = inFile.Z

    # change type from int to float to support rips Filtration
    # float64 Does Not Work!

    Xvals.dtype = "float32"
    Yvals.dtype = "float32"
    Zvals.dtype = "float32"
    points = np.array([Xvals,Yvals,Zvals])
    return points




def main():
    points = get_points()
    # not sure what pairwise distances does yet


    distances = 1
    # computes rips filtration with 1 skeleton
    #changing second argument changes skeleton
    simplicies = fill_rips(points, 1 , distances)




if __name__ == '__main__':

    main()
