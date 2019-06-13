from laspy.file import File
import numpy as np
import dionysus as d
import Rips
from sys         import argv, exit
import PCPDS


class RipsFilt:
    def __init__(self, box_width, skeleton = 1, scalar = 0.2):
        # size of box used in scaling rips distances
        self.box_width = box_width
        # skeleton of rips filtration
        self.skeleton = skeleton
        # scales distances for rips filtration
        self.scalar = 0.2


    def Distances(self, box_width):
        return box_width*self.scalar

    def get_points_fake(self):

        Xvals = np.array([1,2,3,4,5,6,7,8,9,0])
        Yvals = np.array([2,3,4,5,6,7,8,9,0,1])
        Zvals = np.array([3,4,5,6,7,8,9,10,1,2])

        # change type from int to float to support rips Filtration
        # float64 Does Not Work!

        Xvals.dtype = "float32"
        Yvals.dtype = "float32"
        Zvals.dtype = "float32"

        # not functional! Gets stuck in finfinite loop
        temp = np.array([Xvals,Yvals,Zvals])
        points  = temp.T
        return points

    def get_points_file(self):

        # File was too large to work quickly. Took more than 6 min to compute
        inFile = File('test.las', mode='r')
        Xvals = inFile.X
        Yvals = inFile.Y
        Zvals = inFile.Z


        # change type from int to float to support rips Filtration
        # float64 Does Not Work!

        Xvals.dtype = "float32"
        Yvals.dtype = "float32"
        Zvals.dtype = "float32"

        # not functional! Gets stuck in finfinite loop
        temp = np.array([Xvals,Yvals,Zvals])
        points  = temp.T
        return points

    def get_points_pcpds(self, dataobject):
        return dataobject.point_cloud

    def main(self):
        #gets points from file
        points = self.get_points_fake()
        distances = self.Distances(self.box_width)
        # computes rips filtration with 1 skeleton automatically
        #changing second argument in RipsFilt changes skeleton
        f = d.fill_rips(points, self.skeleton , distances)
        m = d.homology_persistence(f)
        diagram = d.init_diagrams(m,f)
        return diagram



if __name__ == '__main__':
    R = RipsFilt(1)
    diagram = R.main()
    print(diagram)
