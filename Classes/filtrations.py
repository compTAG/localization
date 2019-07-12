import dionysus as d
import numpy as np

class Filtration:
    def __init__(self):
        pass

    def get_rips_diagram(point_cloud, skeleton = 1, distance = 1):
        f = d.fill_rips(point_cloud, skeleton , distance)
        m = d.homology_persistence(f)
        diagram = d.init_diagrams(m,f)
        return diagram

    def get_lower_star(point_cloud):
        f =d.fill_freudenthal(point_cloud, True)
        m = d.homology_persistence(f)
        diagram = d.init_diagrams(m,f)
        return diagram

    def get_upper_star(point_cloud):
        f = d.fill_freudenthal(point_cloud, False)
        m = d.homology_persistence(f)
        diagram = d.init_diagrams(m,f)
        return diagram
