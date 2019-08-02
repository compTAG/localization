# This file deals with methods that alter/modify pcpds objects in some way, usually for testing

from Classes.PCPDS import PCPDS
from Classes.PCPDS_manager import PCPDS_Manager
import numpy as np
import math

# Noise functions: Add random/specified noise to point clouds for comparison

# point cloud rotation functions:

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
    rotation_matrix = np.array([[C, 0, -1*S],
                                [0, 1, 0],
                                [S, 0, C]])

    new_point_cloud = np.dot(pcpds.get_point_cloud(), rotation_matrix)

    pcpds.set_point_cloud(new_point_cloud)
    return pcpds

def rotate_section_z(pcpds, theta):
    S, C = np.sin(theta), np.cos(theta)
    rotation_matrix = np.array( [[C, S, 0],
                                [-1*S, C, 0],
                                [0, 0, 1]])

    new_point_cloud = np.dot(pcpds.get_point_cloud(), rotation_matrix)

    pcpds.set_point_cloud(new_point_cloud)
    return pcpds

def add_noise(pcpds, sigma):
    X , Y , Z = pcpds.get_dimensions()
    noise_pcpds = np.array([0, 0, 0])
    X_dev = sigma * (1/X)
    Y_dev = sigma * (1/Y)
    Z_dev = sigma * (1/Z)
    i = 0
    while True:
        X_rand = np.random.normal(0, X_dev, 1)
        Y_rand = np.random.normal(0, Y_dev, 1)
        Z_rand = np.random.normal(0, Z_dev, 1)
        B = np.array([X_rand, Y_rand, Z_rand])
        noise_cloud = np.add(noise_pcpds, B.T)
        i += 1
        if i >= len(pcpds.get_point_cloud()) - 1:
            break

    combined_cloud = np.add(pcpds.get_point_cloud(), noise_cloud)
    # print("COMBINED CLOUD:",combined_cloud)
    # print("REGULAR CLouD:", pcpds.get_point_cloud())
    pcpds.set_point_cloud(combined_cloud)
    return pcpds
