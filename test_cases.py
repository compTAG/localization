from Classes.PCPDS import PCPDS
from Classes.PCPDS_manager import PCPDS_Manager
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

def rotate_section(pcpds, theta_x, theta_y, theta_z):
    result = rotate_section_x(pcpds, theta_x)
    result = rotate_section_y(result, theta_y)
    result = rotate_section_z(result, theta_z)
    return result
        
def normit(v):
    return v / np.sqrt((v**2).sum())

def rotate_section_x(pcpds, theta):
    S, C = np.sin(theta), np.cos(theta)
    rotation_matrix = np.array( [[1, 0, 0],
                                [0, C, -1*S],
                                [0, S, C]])
    
    new_point_cloud = np.dot(pcpds.get_point_cloud(), rotation_matrix)
    
    pcpds.set_point_cloud(new_point_cloud)
    return pcpds
    
    
def rotate_section_y(pcpds, theta):
    S, C = np.sin(theta), np.cos(theta)
    rotation_matrix = np.array([[C, 0, S],
                                [0, 1, 0],
                                [-1*S, 0, C]])
    
    new_point_cloud = np.dot(pcpds.get_point_cloud(), rotation_matrix)
    
    pcpds.set_point_cloud(new_point_cloud)
    return pcpds
    
def rotate_section_z(pcpds, theta):
    S, C = np.sin(theta), np.cos(theta)
    rotation_matrix = np.array( [[C, -1*S, 0],
                                [S, C, 0],
                                [0, 0, 1]])
    
    new_point_cloud = np.dot(pcpds.get_point_cloud(), rotation_matrix)
    
    pcpds.set_point_cloud(new_point_cloud)
    return pcpds
        
def print_pointcloud(pcpds):
    print(pcpds.get_point_cloud())

def main():
    pcpds_manager = PCPDS_Manager()
    pcpds_manager.set_collection_dir("tiny_10_2019-07-23")
    pcpds = pcpds_manager.get_pcpds("1010601")
    print_pointcloud(pcpds)
    result = rotate_section(pcpds, 20, 52, 93)
    print("RESULT:")
    print_pointcloud(pcpds)
    
main()

