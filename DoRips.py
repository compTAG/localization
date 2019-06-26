from laspy.file import File
import numpy as np
import dionysus as d
from sys         import argv, exit
import PCPDS


class RipsFilt:
    def __init__(self, box_width, pcpds_cloud = np.array([1,1]), skeleton = 1, scalar = 0.2):
        # size of box used in scaling rips distances
        self.box_width = box_width
        # skeleton of rips filtration
        self.skeleton = skeleton
        # scales distances for rips filtration
        self.scalar = 0.2
        # sets a point_cloud for use in get_points_pcpds()
        self.pcpds_cloud = pcpds_cloud


    def Distances(self, box_width):
        # temporary - we should play with this to determine best distance
        return box_width*self.scalar

    def get_points_fake(self):
        # random points - same format as those that come from .las file
        Xvals = np.array([1,2,3,4,5,6,7,8,9,0])
        Yvals = np.array([2,3,4,5,6,7,8,9,0,1])
        Zvals = np.array([3,4,5,6,7,8,9,10,1,2])

        # change type from int to float to support rips Filtration
        # float64 Does Not Work!

        Xvals.dtype = "float32"
        Yvals.dtype = "float32"
        Zvals.dtype = "float32"

        # converts cordinate arrays into an array of points
        temp = np.array([Xvals,Yvals,Zvals])
        points  = temp.T
        return points

    def get_points_file(self):

        # File was too large to work quickly. Took more than 6 min to compute
        inFile = File(concatenate(filename, '.las'), mode='r')
        Xvals = inFile.X
        Yvals = inFile.Y
        Zvals = inFile.Z


        # change type from int to float to support rips Filtration
        # float64 Does Not Work!

        Xvals.dtype = "float32"
        Yvals.dtype = "float32"
        Zvals.dtype = "float32"

        # not functional with large datasets
        # can take a very long time to compute filtration on > 1000 points
        temp = np.array([Xvals,Yvals,Zvals])
        points  = temp.T
        return points

    def get_points_pcpds(self):
        try:
            self.pcpds_cloud
        except:
            print("ERROR, NO POINT CLOUD")
        else:
            return self.pcpds_cloud

    def do_persistance(self, p_sc = 'fa'):
        #returns a persistance diagram

        #p_sc is point source selection
        if p_sc == 'fa':
            # uses fake points for filtration
            points = self.get_points_fake()
        elif p_sc == 'pcpds':
            # uses pcpds points for filtration
            points = self.get_points_pcpds()
        elif p_sc == 'fi':
            # uses file points for filtration
            points = self.get_points_file()



        # computes rips filtration with 1 skeleton automatically
        #changing second argument in fill_rips changes skeleton
        f = d.fill_rips(points, self.skeleton , self.Distances(self.box_width))
        m = d.homology_persistence(f)
        diagram = d.init_diagrams(m,f)
        return diagram


class BottleneckDistances:

    def __init__(self, parallelograms, testGrid):
        self.parallelograms = parallelograms
        self.testGrid = testGrid

    def naive_search_distances(self):
        found_idx = 'Error'
        # improve this later
        best_dist = 10000000000

        # generates persistance diagram to search for
        pd1 = self.testGrid.get_persistance_diagram()

        #loops through all IDX in parallelograms dictionary and compares their bottleneck distance to pd1
        for i in parallelograms:
            # gets persistance diagram for i which should be an idx
            pd2 = parallelograms[i].get_persistance_diagram()
            #checks bottleneck distance against current lowest, if it is lower, saves new distance and that idx value
            result = .bottleneck_distance(pd1[0],pd2[0])
            if result < best_dist:
                best_dist = result
                found_idx = i
        # returns idx of lowest bottleneck distance to search_idx
        return found_idx



if __name__ == '__main__':
    R = RipsFilt(1)
    diagram = R.main()
    print(diagram)
