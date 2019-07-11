import dionysus as d
import numpy as np

class Filtration:
    def __init__(self, point_cloud):
        self.point_cloud = point_cloud

    def get_rips_diagram(self, skeleton = 1, distance = 1):
        f = d.fill_rips(self.point_cloud, skeleton , distance)
        m = d.homology_persistence(f)
        diagram = d.init_diagrams(m,f)
        self.persistance_diagram = diagram
        return diagram

    # TODO
    def get_lower_star(self):
        pass
