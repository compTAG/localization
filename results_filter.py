from Classes.PCPDS_manager import PCPDS_Manager
from Classes.menu import menu
import Classes.file_manager as fm
import os.path
import xlrd
from xlwt import Workbook

pm = PCPDS_Manager()
pm.get_path_manager().set_cols_dir("results")

print("Enter the result file directory name:")
collection = menu.get_input("Directory: ")

pm.get_path_manager().set_cur_dir(collection)

valid = pm.get_collection_dir()

while(not valid):
    print("Invalid results dir name:", pm.get_path_manager().get_cur_dir() ,"try again.")
    collection = menu.get_input("Directory: ")
    pm.get_path_manager().set_cur_dir(collection)
    valid = pm.get_collection_dir()
    
# Load in all files from directory
file_names = fm.find_files(pm.get_collection_dir(), ".xls")
print("DIR:", pm.get_collection_dir(), "\n")

print("Ready to process, how manny n_nearest results would you like?")
# Takes in the n_nearest you want to include from those files
n_nearest = menu.get_int_input() + 1
    
print("Mixing into a single result file:", file_names, "\n")

# Generate new results file
wb = Workbook()
excel_sheet = wb.add_sheet('Compiled results')

iter = 0
for file_name in file_names:
    if ".~lock" in file_name or 'compiled_results' in file_name:
        print("\nSkipping irrelevant file:", file_name)
    else:
        try:
            # To open Workbook
            rb = xlrd.open_workbook(os.path.join(pm.get_collection_dir(), file_name))
            sheet = rb.sheet_by_index(0) 
            
            # Store results in other workbook
            for n in range(1, n_nearest):
                val = sheet.cell_value(n, 1)
                excel_sheet.write(n-1, iter, val)
            
            # Check if the idx of the closest Bottleneck distance is the same as the one it was compared against:
            closest_idx = int(sheet.cell_value(1, 0))
            searched_idx = int(sheet.cell_value(1, 2))
            
            if closest_idx == searched_idx:
                excel_sheet.write(n_nearest-1, iter, "yes")
            else:
                excel_sheet.write(n_nearest-1, iter, "no")
                
            iter = iter + 1
            
            # Limit it to 255 since that is the max for excel files.
            if iter > 199:
                print("\nLimiting results folder to excel file capacity of 255 columns for results.")
                break
        except:
            print("\nERROR Invalid file:", file_name)
    menu.progress(iter, len(file_names), "Processed: "+file_name)

wb.save(os.path.join(pm.get_collection_dir(), 'compiled_results.xls'))
menu.progress(1, 1, "Finished compiling result data.\n")
    
# smaller_25 lower star results