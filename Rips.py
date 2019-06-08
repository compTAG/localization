from laspy.file import File
import numpy as np
from dionysus import *
from    sys         import argv, exit



def get_points():
    inFile = File('test.las', mode='r')

    Xvals = inFile.X
    Yvals = inFile.Y
    Zvals = inFile.Z

    #could clean this up with enumerate
    i = 0
    points = ["Zero"]
    for x in Xvals:
        point = (Xvals[i],Yvals[i],Zvals[i])
        points.append(point)
        i += 1

    return points


# code from https://www.mrzv.org/software/dionysus/examples/rips.html
# not sure what argv is doing, but PairwiseDistances needs touples in the way done here
def main(skeleton, max):
    points = get_points()
    distances = PairwiseDistances(points)
    rips = Rips(distances)
    print(time.asctime(), "Rips Initialized")

    simplicies = Filtration()
    rips.generate(skeleton, max, simplicies.append)



if __name__ == '__main__':
    if len(argv) < 4:
        print("Usage: %s POINTS SKELETON MAX" % argv[0])
        exit()

    filename = argv[1]
    skeleton = int(argv[2])
    max = float(argv[3])

    main(skeleton, max)

#print(Xvals)
#print(type(Xvals))
#print(type(Xvals[1]))
