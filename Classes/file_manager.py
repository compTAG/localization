# The FileManager object deals with Saving and Loading Objects

import os.path
from os import walk
import json
import jsonpickle
from datetime import datetime

def __init__(self):
    print("FileManager Loaded.")

# TODO: Move folder creation here.

def save(self, obj, path, name):
    # TODO: verify the folder path is valid
    data = jsonpickle.encode(obj)

    with open(os.path.join(path, str(name)), 'w') as outfile:
        json.dump(data, outfile)

# Returns object stored in json_file from specified path
def load(self, path):
    # TODO: Add feedback for when the file dosen't exist/handling.
    with open(path) as json_file:

        data = json.load(json_file)
        print(data)
        obj = jsonpickle.decode(data)

    return obj

def find_files(self, dir):
    
    files = []
    for (dirpath, dirnames, filenames) in walk(dir):
        files.extend(filenames)
        break

    return files

def find_folders(self, dir):
    
    folders = []
    for (dirpath, dirnames, filenames) in walk(dir):
        folders.extend(dirnames)
        break

    return folders

def directory(self, filename, partition):

    dir_name = str(filename + '_' + str(partition) + '_' + datetime.today().strftime('%Y-%m-%d'))

    return str(os.path.join('cell_collections', dir_name))
