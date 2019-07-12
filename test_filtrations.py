from Classes.filtrations import Filtration
import numpy as np

points = np.array([[0.0,0.0,0.0],[2.0,0.0,0.0],[0.0,2.0,0.0],[2.0,2.0,0.0],[3.0,1.0,0.0]])

rip = Filtration.get_rips_diagram
print(rip(points, 1, 5.0))
