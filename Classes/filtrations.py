import dionysus as d
import numpy as np

class Filtration:

    def get_rips_diagram(pcpds_obj):
        f = d.fill_rips(pcpds_obj.get_point_cloud().astype('f4'), pcpds_obj.get_skeleton() , pcpds_obj.get_distance())
        m = d.homology_persistence(f)
        diagram = d.init_diagrams(m,f)
        pcpds_obj.set_persistance_diagram(diagram)
        pcpds_obj.set_filtration_used(Filtration.get_rips_diagram, "rips")
        return pcpds_obj

    def get_lower_star(pcpds_obj):
        f = d.fill_freudenthal(pcpds_obj.get_point_cloud().astype('f4'), True)
        m = d.homology_persistence(f)
        diagram = d.init_diagrams(m,f)
        pcpds_obj.set_persistance_diagram(diagram)
        pcpds_obj.set_filtration_used(Filtration.get_lower_star, "lower_star")
        return pcpds_obj

    def get_upper_star(pcpds_obj):
        f = d.fill_freudenthal(pcpds_obj.get_point_cloud().astype('f4'), False)
        m = d.homology_persistence(f)
        diagram = d.init_diagrams(m,f)
        pcpds_obj.set_persistance_diagram(diagram)
        pcpds_obj.set_filtration_used(Filtration.get_upper_star, "upper_star")
        return pcpds_obj
