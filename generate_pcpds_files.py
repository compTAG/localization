from Classes.process_las import ProcessLas
from Classes.menu import menu
from Classes.PCPDS_manager import PCPDS_Manager
import Classes.file_manager as file_manager

# This file's purpose is to generate pcpds files in a directory given the las file as input

def generate_files():

    print("What LAS file would you like to use?")
    filename = menu.get_filename_input()

    print("How manny partitions would you like?")
    partition = menu.get_int_input()

    las_obj = ProcessLas(filename, partition)

    dir_name = file_manager.make_folder(filename)

    pfm = PCPDS_Manager()
    dir_name = pfm.generate_collection(filename, partition)

    # TODO: Add multithreading option to input_las?
    las_obj.input_las(dir_name)
    print("File generation complete.")

generate_files()
