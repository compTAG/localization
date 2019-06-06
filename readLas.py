from laspy.file import File
import numpy as np

inFile = File('test.las', mode='r')

#print("Examining Point Format: ")
#pointformat = inFile.point_format
#for spec in inFile.point_format:
#    print(spec.name)

print("X dim: ", inFile.X)
print("Y dim: ", inFile.Y)
print("Z dim: ", inFile.Z)

#print("Examining Header Format:")
#headerformat = inFile.header.header_format
#for spec in headerformat:
#    print(spec.name)

#Puts x,y,z coordinates into a 3d array
#Coordinates = np.vstack((inFile.x, inFile.y, inFile.z)).transpose()

I = inFile.Classification == 2

outFile = File('output.las', mode='w', header=inFile.header)
outFile.points = inFile.points[I]
outFile.close()
