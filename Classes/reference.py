class reference:
    
    # This class serves as a means of statically referencing variables so they 
    # don't have to be passed around everywhere, but only set once here instead.
    
    cur_dir_name = None
    
    @staticmethod
    def set_cur_dir_name(dir_name):
        reference.cur_dir_name = dir_name
        
    @staticmethod
    def get_cur_dir_name():
        return reference.cur_dir_name