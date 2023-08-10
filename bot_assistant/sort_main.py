import pathlib
from .sort_functions import define_data, print_data, rm_empty_dirs, sort_data


TEXT_COLOR = {
    "red": "\033[31m",
    "green": "\033[32m",
    "reset": "\033[0m"
}


def sort_main_func(inp_path):
    path = pathlib.Path(inp_path)

    if not path.is_dir():
        print(TEXT_COLOR["red"] + "The argument is path to file or folder doesn't exist" + TEXT_COLOR["reset"])
        return
    
    defined_files = define_data(path)
    sort_data(path, defined_files)
    rm_empty_dirs(path)
    print_data(defined_files)