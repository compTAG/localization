from Classes.PCPDS_manager import PCPDS_Manager
from Classes.menu import menu
import Classes.file_manager as file_manager
import Classes.modifiers as modifiers
import os.path
import Classes.bottleneck_dist as bd
from xlwt import Workbook

pcpds_manager = PCPDS_Manager()
print("Collections:")
collections_string = ""
collections =  os.listdir(pcpds_manager.get_path_manager().get_collections_path())
collections.sort()
for directory in collections:
    collections_string += directory + " \t"
print(collections_string)
print("Please enter a collection that has already been filtrated:")

# Loop here for valid directory
collection = menu.get_input("Directory: ")
    
pcpds_manager.get_path_manager().set_cur_dir(collection)
    
cap = 10
valid = pcpds_manager.get_collection_dir()
while(True):
    
    # If not a valid directory, ask again saying it is invalid
    while(not valid):
        if not pcpds_manager.get_collection_dir():
            print("Invalid collection name:", pcpds_manager.get_path_manager().get_cur_dir() ,"try again.")
        collection = menu.get_input("Directory: ")
        pcpds_manager.get_path_manager().set_cur_dir(collection)
        valid = pcpds_manager.get_collection_dir()
    
    # Checks the first pcpds object in this directory for if it has a persistance diagram
    pcpds_temp = None
    for file in os.listdir(pcpds_manager.get_path_manager().get_full_cur_dir_var(collection)):
        file_path = os.path.join(pcpds_manager.get_path_manager().get_full_cur_dir(), file)
        pcpds_temp = file_manager.load(file_path)
        break
    if pcpds_temp is not None:
        if pcpds_temp.get_persistance_diagram() is not None:
            print("Valid Directory Chosen:", valid)
            break
        else:
            valid = False
            print("\nNo persistance diagram present for files @ collection:", pcpds_manager.get_path_manager().get_full_cur_dir() + ".\n")
            print("Please Either enter a directory that has been filtrated for persistance diagrams or run 'generate_persistance_diagrams.py' on the collection.")
    else:
        print("Problem loading pcpds file, it loaded as None.")
    
pcpds = None

# Set up workbook
wb = Workbook()
excel_sheet = wb.add_sheet('Noise compared to Normal')

excel_sheet.write(0, 0, "Sigma:")

idx_counter = 1
for file in file_manager.find_files(pcpds_manager.get_collection_dir(), '.json'):
    pcpds = file_manager.load(os.path.join(pcpds_manager.get_collection_dir(), file))

    excel_sheet.write(0, idx_counter, pcpds.get_cellID())
    idx_counter = idx_counter + 1
    if idx_counter > cap:
            break
        
print("Computing...")
for n in range(1, 11):
    # Loop through different sigma values for every file in the dir.
    idx_counter = 1
    sigma = n * 0.01
    excel_sheet.write(n, 0, sigma)
    for file in file_manager.find_files(pcpds_manager.get_collection_dir(), '.json'):
        # Sets the PCPDS
        og_pcpds = file_manager.load(os.path.join(pcpds_manager.get_collection_dir(), file))
        pcpds = file_manager.load(os.path.join(pcpds_manager.get_collection_dir(), file))
        
        # Adds the noise to the pcpds object
        pcpds = modifiers.add_noise(pcpds, sigma)# .set_point_cloud(modifiers.add_noise(og_pcpds, sigma))
        
        # Reapply the filtration
        filt = pcpds.get_filtration_used()
        pcpds = filt(pcpds)

        # print("REG POINT CLOuD:", og_pcpds.get_point_cloud())
        # print("NOISE POINT CLOuD:", pcpds.get_point_cloud())

        # Calculate bottleneck distance
        distance = bd.get_distances(og_pcpds.get_persistance_diagram(), pcpds.get_persistance_diagram())
        excel_sheet.write(n, idx_counter, distance)
        print(distance)
        
        idx_counter = idx_counter + 1
        if idx_counter > cap:
            break
        
        
    # "Noise Applied. Sigma: "+str(sigma))
wb.save(os.path.join("results", ":"+pcpds_manager.get_path_manager().get_cur_dir())+":Noise ALL:" + pcpds.get_filtration_used_name() + '.xls')
print("Done.")

