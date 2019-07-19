import dionysus as d
import numpy as np

class Filtration:

    def get_rips_diagram(pcpds_obj):
        f = d.fill_rips(pcpds_obj.get_point_cloud(), pcpds_obj.get_skeleton() , pcpds_obj.get_distance())
        m = d.homology_persistence(f)
        diagram = d.init_diagrams(m,f)
        pcpds_obj.set_persistance_diagram(diagram)
        return pcpds_obj

    def get_lower_star(pcpds_obj):
        f = d.fill_freudenthal(pcpds_obj.get_point_cloud(), True)
        m = d.homology_persistence(f)
        diagram = d.init_diagrams(m,f)
        pcpds_obj.set_persistance_diagram(diagram)
        return pcpds_obj

    def get_upper_star(pcpds_obj):
        f = d.fill_freudenthal(pcpds_obj.get_point_cloud(), False)
        m = d.homology_persistence(f)
        diagram = d.init_diagrams(m,f)
        pcpds_obj.set_persistance_diagram(diagram)
        return pcpds_obj
