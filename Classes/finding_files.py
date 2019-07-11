from Classes.process_las import ProcessLas
import Classes.PCPDS
from datetime import datetime
import os.path

class FindingFiles:

    def __init__(self):

        pass

    def partitions(self):

        partition = 0.1
        while (partition%1) != 0:
            partition = float(input("Enter Partition Count (1D): "))
            if (partition%1) != 0:
                print('Please enter a whole number.')
        filename = input("Enter the name of the file you'd wish to import: ")
        return [int(partition), filename]

    def return_points(self, las_obj, idx, json_ext, las_ext, dir_name):
        if not (las_obj.check_file(idx, json_ext, dir_name)): #Where ** is the ext of PDs
            #Check if the file exists

            if las_obj.check_file(None, las_ext, None):

                # Saves the persistence diagrams of each grid
                # and returns the dict of PCPDS

                # TODO: save the PCPDS objects in the dict under their file.
                # TODO: move the saving of PCPDS objects to happen as they are generated/updated
                try:
                    os.makedirs(dir_name)
                    print("Directory " + dir_name + " created.")

                except FileExistsError:
                    print("Directory " + dir_name + " already exists.")

                # Save persistence diagrams in the aforementioned folder
                return las_obj.input_las()

            else:
                print('Error. No matching file found. Exiting.')
                exit()
        else:
            pass
            # Import persistence diagrams/ points array
            # using PCPDS .json files
