import pathlib
from sort_functions import define_data, print_data, rm_empty_dirs, sort_data


def sort_main_fucn(inp_path):
    if len(inp_path) > 1:
        source = inp_path       
    else:
        print("The path to folder should be passed as argument after script name")
        return
    
    path = pathlib.Path(source)

    if not path.is_dir():
        print("The argument is path to file or folder doesn't exist")
        return
    
    defined_files = define_data(path)
    sort_data(path, defined_files)
    rm_empty_dirs(path)
    print_data(defined_files)