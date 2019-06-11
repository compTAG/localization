from laspy.file import File
import numpy as np

inFile = File('test.las', mode='r')

# Grabs all the points from the file:
points = inFile.points

for p in points:
    print(p)
    
inFile.visualize()