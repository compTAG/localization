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

def rotate_section(pcpds, theta):
    point_cloud = pcpds.get_point_cloud()
    
    S, C = np.sin(theta), np.cos(theta)
    rotation_matrix = np.array([[C, -1*S, 0],
                       [S, C, 0],
                       [0, 0, 1]])
    
    for point in point_cloud:
        x = point[0]
        y = point[1]
        z = point[2]
        
        transform.homography
        
def normit(v):
    return v / np.sqrt((v**2).sum())

def rotate_section_x(pcpds, theta):
    point_cloud = pcpds.get_point_cloud()
    S, C = np.sin(theta), np.cos(theta)
    rotation_matrix = np.array([[1, 0, 0],
                       [0, C, -1*S],
                       [0, S, C]])
    for point in point_cloud:
        x = point[0]
        y = point[1]
        z = point[2]
    
    
def rotate_section_y(pcpds, theta):
    point_cloud = pcpds.get_point_cloud()
    S, C = np.sin(theta), np.cos(theta)
    rotation_matrix = np.array([[C, 0, S],
                       [0, 1, 0],
                       [-1*S, 0, C]])
    for point in point_cloud:
        x = point[0]
        y = point[1]
        z = point[2]
    
def rotate_section_z(pcpds, theta):
    # TODO: Build a np array with every 3 entries in the point_cloud 
    point_cloud = pcpds.get_point_cloud()
    
    S, C = np.sin(theta), np.cos(theta)
    rotation_matrix = np.array([[C, -1*S, 0],
                       [S, C, 0],
                       [0, 0, 1]])
    new_point_cloud = []
    for point in point_cloud:
        
        xyz = np.array(point)
        #print("XYZ: "+ str(point_cloud[0])+ ", ", point_cloud[1], ",", point_cloud[2])
        
        rotated_xyz = np.dot(xyz, rotation_matrix)
        print("Rotated XYZ: "+ str(rotated_xyz))
        #if rotated_xyz.isempty
        
        #np.vstack((new_point_cloud, rotated_xyz))
    #print("\nNEW POINT_CLOUD:\n", new_point_cloud)
        
def main():
    rotate_section_z(pcpds_util.load_section("cell_collections/test_2_2019-07-08","1011"), 90)