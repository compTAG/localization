from laspy.file import File
import numpy as np
import dionysus as d
import Rips
from sys         import argv, exit


class Rips:
    def __init__(self, box_width, skeleton = 1, scalar = 0.2):
        # size of box used in scaling rips distances
        self.box_width = box_width
        # skeleton of rips filtration
        self.skeleton = skeleton
        # scales distances for rips filtration
        self.scalar = 0.2


    def Distances(self, box_width):
        return box_width*self.scalar


    def get_points(self):
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




    def main(self):
        points = self.get_points()
        # not sur

        distances = self.Distances(self.box_width)
        # computes rips filtration with 1 skeleton
        #changing second argument changes skeleton
        f = d.fill_rips(points, 1 , distances)
        m = d.homology_persistence(f)
        diagram = d.init_diagrams(m,f)
        return diagram



if __name__ == '__main__':
    R = Rips(100000000000000000)
    R.main()
