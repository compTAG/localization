from Classes.filtrations import Filtration
import numpy as np
import dionysus as d

#points to test on
points = np.array([[0.0,0.0,0.0],[2.0,0.0,0.0],[0.0,2.0,0.0],[2.0,2.0,0.0],[3.0,1.0,0.0],[0.0,0.0,7.0]])

#get rips diagram
rip = Filtration.get_rips_diagram
rfilt = rip(points, 1, 5.0)
print(rfilt)

#get lower star diagram
star = Filtration.get_lower_star
lsfilt = star(points)
print(lsfilt)

#print diagrams
d.plot.plot_diagram(rfilt[0], show = True)

d.plot.plot_diagram(lsfilt[0], show = True)
