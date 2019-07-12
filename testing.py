from Classes.PCPDS_manager import PCPDS_Manager as PCPDS_manager

pc = PCPDS_manager()
pc.get_path_manager().set_cols_dir("Classes")
print(pc.get_path_manager().get_cols_dir())