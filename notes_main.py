import re
from notes_classes import Note, Notes, Tag
import os
import pathlib
from platformdirs import user_data_dir
from notes_classes import Tag, Note, Notes


notes = Notes()


def show_commands_note():
    all_commands = ["add_note", "edit_note", "remove_note", "show_notes", "search_note", "search_by_tags",
                    "add_tags_to_note", "remove_tags_in_note", "remove_all_tags_in_note"]
    return "\n" + "\n".join(all_commands) + "\n"


def add_note(user_input):
    user_split_by_title = user_input.split("title:")
    user_split_by_body = user_split_by_title[1].split("body:")
    user_split_by_tags = user_split_by_body[1].split("tags:")

    note_title = user_split_by_body[0].strip()
    note_body = user_split_by_tags[0].strip()
    note_tags_list = []

    if len(user_split_by_tags) > 1:
        note_tags = user_split_by_tags[1].strip()
        note_tags_list = note_tags.split(", ")

    note = Note(note_title, note_body)

    if note_tags_list:
        for note_tag in note_tags_list:
            note_tag = Tag(note_tag)
            note.add_tags(note_tag)

    notes.add_note(note)

    result_note = "\n" + "This note was succesfully added!\n" + \
        "-"*20 + "\n" + str(note) + "\n"

    return result_note


def edit_note(user_input):
    user_split_by_id = user_input.split("id:")
    user_split_by_title = user_split_by_id[1].split("title:")
    user_split_by_body = user_split_by_title[1].split("body:")

    note_id = int(user_split_by_title[0].strip())
    note_title = user_split_by_body[0].strip()
    note_body = user_split_by_body[1].strip()

    notes.edit_note(note_id, note_title, note_body)

    return f"\nNote with id: {note_id} was succesfully changed!\n"


def remove_note(user_input):
    list_user_input = user_input.split()
    notes.remove_note(list_user_input[1])

    return f"\nNote with id: {list_user_input[1]} was succesfully removed!\n"


def show_notes(user_input):
    result_note = []
    for note in notes.show_notes():
        result_note.append(note)

    return "\n" + "\n--------------------\n".join(result_note) + "\n"


def search_note(user_input):
    user_input = user_input.removeprefix("search_note")
    user_input = user_input.strip()
    result_note = []
    for note in notes.show_notes(user_input):
        result_note.append(note)

    return "\n" + "\n--------------------\n".join(result_note) + "\n"


def search_by_tags(user_input):
    user_input = user_input.removeprefix("search_by_tags")
    user_input = user_input.strip()
    user_input = user_input.split(", ")
    result_note = []

    for note in notes.search_and_sort_by_tags(user_input):
        result_note.append(str(note))

    return "\n" + "\n--------------------\n".join(result_note) + "\n"


def add_tags_to_note(user_input):
    user_split_by_id = user_input.split("id:")
    user_split_by_tags = user_split_by_id[1].split("tags:")

    note_id = int(user_split_by_tags[0].strip())
    note_tags = user_split_by_tags[1].strip()
    note_tags = note_tags.split(", ")

    note = notes.data.get(note_id)

    for tag in note_tags:
        note.add_tags(Tag(tag))

    return "\nTags was succesfully added!\n"


def remove_tags_in_note(user_input):
    user_split_by_id = user_input.split("id:")
    user_split_by_tags = user_split_by_id[1].split("tags:")

    note_id = int(user_split_by_tags[0].strip())
    note = notes.data.get(note_id)

    if user_split_by_id[0].strip() == "remove_all_tags_in_note":
        note.remove_all_tags()
        return "\nTags was succesfully removed!\n"

    note_tags = user_split_by_tags[1].strip()
    note_tags = note_tags.split(", ")

    for tag in note_tags:
        note.remove_tags(Tag(tag))

    return "\nTags was succesfully removed!\n"


operations_notes = {
    "show_commands_note": show_commands_note,
    "add_note": add_note,
    "edit_note": edit_note,
    "remove_note": remove_note,
    "show_notes": show_notes,
    "search_note": search_note,
    "search_by_tags": search_by_tags,
    "add_tags_to_note": add_tags_to_note,
    "remove_tags_in_note": remove_tags_in_note,
    "remove_all_tags_in_note": remove_tags_in_note
}


def get_handler(handler):
    return operations_notes[handler]


def notes_main_func():
    while True:

        user_input = input(">>> ")
        list_user_input = user_input.split()
        list_user_input[0] = list_user_input[0].lower()

        result_handler = get_handler(list_user_input[0])(user_input)

        print(result_handler)


def get_file_path(file_name):
    path = pathlib.Path(user_data_dir("Personal assistant"))
    if os.name == "nt":
        path = path.parent
    if not path.is_dir():
        path.mkdir()
    file_path = path.joinpath(file_name)
    return file_path


def notes_func():
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
    test_note1 = Note("Test Note 1", "reirweitweiruwehrweurhweurhwje", Tag(
        "tag1"), Tag("tag2"), Tag("tag2"), Tag("tag3"))
    test_note2 = Note("Test Note 2", "573463463425325235", Tag(
        "tag4"), Tag("tag4"), Tag("tag4"), Tag("tag5"))
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
    notes_func()
    notes_main_func()
