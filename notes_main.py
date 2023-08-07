import os
import pathlib
from platformdirs import user_data_dir
from notes_classes import Tag, Note, Notes


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

    # Temporary testing code for notes:
    # Begin
    print("\n" * 10)
    print("Loaded notes:")
    print("-" * 100)
    for note in notes.show_notes():
        print(note)
    print("-" * 100)
    test_note1 = Note("Test Note 1", "reirweitweiruwehrweurhweurhwje", Tag("tag1"), Tag("tag2"), Tag("tag2"), Tag("tag3"))
    test_note2 = Note("Test Note 2", "573463463425325235", Tag("tag4"), Tag("tag4"), Tag("tag4"), Tag("tag5"))
    notes.add_note(test_note1)
    notes.add_note(test_note2)

    # Dumping to file
    notes.save_to_file(file_path)

    print("\n" * 10)
    print("Saved notes:")
    print("-" * 100)
    for note in notes.show_notes():
        print(note)
    print("-" * 100)
    # End


if __name__ == "__main__":
    notes_main_func()