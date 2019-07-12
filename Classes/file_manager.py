# The FileManager object deals with Saving and Loading Objects

import os.path
from os import walk
import json
import jsonpickle

def save(obj, path, name):
    # TODO: verify the folder path is valid
    data = jsonpickle.encode(obj)

    with open(os.path.join(path, str(name)), 'w') as outfile:
        json.dump(data, outfile)

# Returns object stored in json_file from specified path
def load(path):
    # TODO: Add feedback for when the file dosen't exist/handling.
    with open(path) as json_file:

        data = json.load(json_file)
        # print(data)
        obj = jsonpickle.decode(data)

    return obj

def find_files(dir):
    
    files = []
    for (dirpath, dirnames, filenames) in walk(dir):
        files.extend(filenames)
        break

    return files

def find_folders(dir):
    
    folders = []
    for (dirpath, dirnames, filenames) in walk(dir):
        folders.extend(dirnames)
        break

    return folders

def make_folder(dir_name):
    try:
        os.makedirs(dir_name)
        print("Directory " + dir_name + " created.")

    except FileExistsError:
        print("Directory " + dir_name + " already exists.")