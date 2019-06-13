from laspy.file import File
import numpy as np
import dionysus as d
import Rips
from sys         import argv, exit


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


    def get_points_file(self):

        #dummy float values for other functionality to continue
        return np.array([[3.0,1.0],[1.0,1.0],[1.0,3.0],[2.0,2.0]])



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
        points = np.array([Xvals[0],Yvals[0],Zvals[0]])
        for i,_ in enumerate(Xvals):
            temp = np.array([Xvals[i],Yvals[i],Zvals[i]])
            points = np.append(points, temp)
        return points

    def get_pointcloud(self):
        #need to build functionality with how we slice up the original dataset
        pass



    def main(self):
        points = self.get_points_file()

        # something is going wrong in here -it may have to do with how we import the numbers
        distances = self.Distances(self.box_width)
        # computes rips filtration with 1 skeleton automatically
        #changing second argument in RipsFilt changes skeleton
        f = d.fill_rips(points, self.skeleton , distances)
        m = d.homology_persistence(f)
        diagram = d.init_diagrams(m,f)
        return diagram



if __name__ == '__main__':
    R = RipsFilt(100000000000000000, 20, 1)
    diagram = R.main()
    print(diagram)
