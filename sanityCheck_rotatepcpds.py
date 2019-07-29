# We rotate the point cloud, recompute it's persistence diagram, and compare it's persistance diagram to the origional.
# They should be identical, therefore showing the angle of approach does not matter using this method of TDA.

from Classes.PCPDS_manager import PCPDS_Manager
from Classes.menu import menu
import Classes.modifiers as modifiers
import Classes.bottleneck_dist as bd

def choose_pcpds(pm):
    # Asks the user if they want to specify a pcpds or select a random one.
    print("Enter a specific pcpds number, or enter 'R' for a random one.")
    specification = menu.get_input("PCPDS Num:")
    
    pcpds = None
    valid_pcpds_found = False

    while not valid_pcpds_found:
        try:
            pcpds_num = int(specification)
            # Attempt to load in specified pcpds
            try:
                pcpds = pm.get_pcpds(specification)
                valid_pcpds_found = True
                break
            except:
                # Dosen't exist?
                print("pcpds file for cell_ID:", specification, "dosen't exist.")
        except:
            
            if specification.lower() == "r":
                pcpds = pm.get_random_pcpds()
                valid_pcpds_found = True
                break
                print(specification)
            else:
                print("Invalid pcpds format entered.")
        specification = menu.get_input("PCPDS Num:")
    return pcpds

pcpds_manager = PCPDS_Manager()
    
# List the directories

# Ask for the directory
print("Enter the Collection of pcpds objects you wish to generate persistance diagramsfor.")
collection = menu.get_input("Directory: ")

pcpds_manager.get_path_manager().set_cur_dir(collection)

path = pcpds_manager.get_collection_dir()

while(not path):
    print("Invalid collection name:", pcpds_manager.get_path_manager().get_cur_dir() ,"try again.", path)
    collection = menu.get_input("Directory: ")
    pcpds_manager.get_path_manager().set_cur_dir(collection)
    path = pcpds_manager.get_collection_dir()

# Verify the directory

print("Valid Directory Confirmed:", pcpds_manager.get_path_manager().get_full_cur_dir())

pcpds = None

while True:
    # Load in pcpds object from dir & name
    pcpds = choose_pcpds(pcpds_manager)

    # Verify the pcpds object has a persistence diagram. if not, repeat this process.
    if pcpds.get_persistance_diagram() is not None:
        break
    print("Idx value selected does not have a persistance diagram generated.")

# Get input for rotation values
print("Rotation theta for X axis:")
x = menu.get_float_input()
print("Rotation theta for Y axis:")
y = menu.get_float_input()
print("Rotation theta for Z axis:")
z = menu.get_float_input()

# Make a copy of pcpds object & rotate it's point cloud
rotated_pcpds = modifiers.rotate_section(pcpds, x, y, z)

# Regenerate rotated_pcpds's persistence diagram

rotated_pcpds = rotated_pcpds.get_filtration_used()(rotated_pcpds)

# Compute bottleneck distance & check it is near 0. (within margin of error from rotation)
distance  = bd.get_distances(rotated_pcpds.get_persistance_diagram(), pcpds.get_persistance_diagram())

print("The bottle neck distance between", pcpds.get_cellID(), "and", rotated_pcpds.get_cellID(), "rotated by X", x, "Y", y, "Z", z, "is:", distance)