# The FileManager object deals with Saving and Loading Objects

import os.path
from os import walk
import json
import jsonpickle
import random

def input_partitions_file():

    partition = 0.1
    while (partition%1) != 0:
        partition = float(input("Enter Partition Count (1D): "))
        if (partition%1) != 0:
            print('Please enter a whole number.')

    fn = False
    filename = ''
    while fn == False:
        filename = input("Enter the name of the file you'd wish to import: ")
        temp = filename + '.las'
        fn = os.path.isfile(temp)
        if fn == False:
            print('File not found.')

    return [int(partition), filename]


def save(obj, path, name):
    # TODO: verify the folder path is valid
    data = jsonpickle.encode(obj)

    with open(os.path.join(path, (str(name)+".json")), 'w') as outfile:
        json.dump(data, outfile)


# Returns object stored in json_file from specified path
def load(path):
    # TODO: Add feedback for when the file dosen't exist/handling.
    with open(path) as json_file:

        data = json.load(json_file)
        # print(data)
        obj = jsonpickle.decode(data)

    return obj

def find_files(dir, ext):

    ext_len = -1*len(ext)
    for (dirpath, dirnames, filenames) in walk(dir):
        return filenames

def find_folders(dir):

    folders = []
    for (dirpath, dirnames, filenames) in walk(dir):
        folders.extend(dirnames)
        break

    return folders

# Takes in a directory, & returns a random file in that directory (Sub directories not included)
def get_random_file(dir, file_type):
      files = []
      for file in os.listdir(dir):
            if file.endswith(file_type):
                files.append(file)

      file_count = len(files)

      if len(files) < 1:
            print("No valid files of type:",file_type,", in directory:",dir)
      else:
            return random.choice(files)

def make_folder(dir_name):

    try:
        os.makedirs(dir_name)
        print("Directory " + dir_name + " created.")

    except FileExistsError:
        print("Directory " + dir_name + " already exists.")
        
def make_folder_at_dir(path, dir_name):
    
    try:
        dir_path = os.path.join(path, dir_name)
        os.makedirs(dir_path)
        print("Directory " + dir_path + " created.")

    except FileExistsError:
        print("Directory " + dir_name + " already exists @", path)