import Classes.PCPDS as pcpds_util
from Classes.PCPDS import PCPDS
import numpy as np
import math

# The purpose of this class is to hold the test cases for use of demonstrating tests

# Chooses a random section from the las grid, rotates it, and sees if it can find it in the grid again using rips filtration methodology.
class rotated_section_test:
    
    def __init__(self, pcpds):
        
        # Begin by rotating the pcpds's point cloud
        
        # Process the pcpds's point cloud into a persistance diagram
        
        # Use Bottle neck distance to try and find the closest match
        pass
        
### Rotates a passed in pcpds's point cloud and regenerates it's persistance diagram.

# Returns the rotation matrix given theta
def rotation_matrix(theta):
    return [[math.cos(theta), -math.sin(theta), 0][math.sin(theta), math.cos(theta), 0][0,0,1]]

def rotate_section(pcpds):
    point_cloud = pcpds.get_point_cloud()
    
    for point in point_cloud:
        x = point[0]
        y = point[1]
        z = point[2]
        
        n1, n2, ncalc = [normit()]
        
def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def normit(v):
    return v / np.sqrt((v**2).sum())

def rotate_section_x(pcpds, theta):
    point_cloud = pcpds.get_point_cloud()
    
    
def rotate_section_y(pcpds, theta):
    point_cloud = pcpds.get_point_cloud()
    
def rotate_section_z(pcpds, theta):
    point_cloud = pcpds.get_point_cloud()