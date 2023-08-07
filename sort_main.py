import pathlib
import sys
from sort_functions import define_data, print_data, rm_empty_dirs, sort_data


def main():
    sysargv = sys.argv
    if len(sysargv) > 1:
        source = sysargv[1]        
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

if __name__ == "__main__":
    main()