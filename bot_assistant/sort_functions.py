import re


CATEGORY_EXTS = {
    "archives": ('zip', 'gz', 'tar', '7z', 'rar', 'arj', 'pkg', 'deb', 'rpm', 'z'),
    "audio": ('mp3', 'ogg', 'wav', 'wma', 'amr', 'aif', 'flac', 'cue'),
    "documents": ('doc', 'docx', 'odt', 'wpd', 'rtf', 'txt', 'tex', 'pdf', 'ods', 'xls', 'xlsx', 'xlsm', 'pptx', 'djv', 'djvu'),
    "images": ('jpeg', 'png', 'jpg', 'svg', 'bmp', 'tif', 'tiff', 'ai', 'gif', 'ico', 'ps', 'psd', 'webp'),
    "video": ('avi', 'mp4', 'mov', 'mkv', 'm4v', 'h264', 'h265', 'mp4', 'mpg', 'mpeg', 'rm', 'flv', 'swf', 'vob', 'webm', 'wmv'),
}


def define_data(path):
    defined_files = {}
    category_dirs = []
    for key in CATEGORY_EXTS:
        defined_files[key] = []
        category_dirs.append(path.joinpath(key))

    for i in path.glob("**/*"):
        if i.is_file() and i.parent not in category_dirs:
            for key in defined_files:
                if i.suffix.removeprefix(".").casefold() in CATEGORY_EXTS[key]:
                    defined_files[key].append(i)
                    break

    return defined_files


def print_data(defined_files):
    for key in defined_files:
        if len(defined_files[key]) > 0:
            print(f"Files from '{key}' category:")
            for i in defined_files[key]:
                print(" " * 8 + f"{i.name}")
        else:
            continue
        print("\n")


def rm_empty_dirs(path):
    for i in path.iterdir():
        if i.is_dir():
            rm_empty_dirs(i)
            try:
                i.rmdir()
            except OSError:
                continue


def sort_data(path, defined_files):
    for key in defined_files:
        if len(defined_files[key]) > 0:
            subpath = path.joinpath(key)
            if not subpath.is_dir():
                subpath.mkdir()
            for i in defined_files[key]:
                founded_ids = []
                for file in subpath.iterdir():
                    if file.is_file():
                        if i.name.casefold() == file.name.casefold():
                            founded_ids.append(1)
                        if file.stem.casefold().startswith(i.stem.casefold()):
                            suffix_string = file.stem.casefold().replace(i.stem.casefold(), "")
                            if suffix_string.find(" ") == 0 and suffix_string.count(" ") == 1 and re.fullmatch(" \(\d+\)", suffix_string):
                                founded_ids.append(int(suffix_string[2:-1]))
                if founded_ids:
                    id = 1
                    while True:
                        id += 1
                        if id not in founded_ids:
                            i.replace(subpath.joinpath(i.stem + " " + "(" + str(id) + ")" + i.suffix))
                            break
                else:
                    i.replace(subpath.joinpath(i.name))