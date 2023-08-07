import os
import pathlib
from platformdirs import user_data_dir
from notes_classes import Notes


def get_file_path(file_name):
    path = pathlib.Path(user_data_dir("Personal assistant"))
    if os.name == "nt":
        path = path.parent
    if not path.is_dir():
        path.mkdir()
    file_path = path.joinpath(file_name)
    return file_path


def notes_main_func():
    notes = Notes()
    file_path = get_file_path("notes.bin")
    notes.load_from_file(file_path)