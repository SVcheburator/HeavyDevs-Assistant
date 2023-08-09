import pathlib
from .sort_functions import define_data, print_data, rm_empty_dirs, sort_data


def sort_main_func(inp_path):
    path = pathlib.Path(inp_path)

    if not path.is_dir():
        print("The argument is path to file or folder doesn't exist")
        return
    
    defined_files = define_data(path)
    sort_data(path, defined_files)
    rm_empty_dirs(path)
    print_data(defined_files)