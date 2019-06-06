import laspy
import numpy as np

inFile = File('test.las', mode='r')

I = inFile.Classification == 2

outFile = File('output.las', mode='w', header=inFile.header)
outFile.points = inFile.points[I]
outFile.close()
