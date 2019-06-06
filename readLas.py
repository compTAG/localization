from laspy.file import File
import numpy as np

inFile = File('test.las', mode='r')

print("X dim: ", inFile.X)
print("Y dim: ", inFile.Y)
print("Z dim: ", inFile.Z) 

I = inFile.Classification == 2

outFile = File('output.las', mode='w', header=inFile.header)
outFile.points = inFile.points[I]
outFile.close()
