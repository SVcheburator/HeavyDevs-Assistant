import os
import pathlib
from platformdirs import user_data_dir
from .notes_classes import Tag, Note, Notes, IdError


notes = Notes()


def input_error(func):
    def inner(user_input):

        try:
            result_func = func(user_input)
            return result_func
        except IdError:
            return "\nNote with such id does not exist!\n"

    return inner


def show_commands_note(user_input):
    all_commands = ["add_note", "edit_note", "remove_note", "remove_all_notes", "show_notes", "search_note", "search_by_tags",
                    "add_tags_to_note", "remove_tags_in_note", "remove_all_tags_in_note", "mark_done", "unmark_done", "exit"]
    if user_input.strip().lower() == "show_commands_note":
        return "\n" + "\n".join(all_commands) + "\n"
    else:
        return "\nThis function does not exist. Try again!\n"


def add_note(user_input):
    try:
        user_split_by_title = user_input.split("title:")
        user_split_by_body = user_split_by_title[1].split("body:")
        user_split_by_tags = user_split_by_body[1].split("tags:")
    except IndexError:
        return "\nTo add a note you need to write 'title: ... body: ... tags: ...' Tags as desired.\n"

    note_title = user_split_by_body[0].strip()
    note_body = user_split_by_tags[0].strip()
    note_tags_list = []

    if len(user_split_by_tags) > 1:
        note_tags = user_split_by_tags[1].strip()
        note_tags_list = note_tags.split(", ")

    if note_title and note_body:
        note = Note(note_title, note_body)
    else:
        return "\nYou need to write something in 'title: ... body: ...'\n"

    if note_tags_list:
        for note_tag in note_tags_list:
            note_tag = Tag(note_tag)
            note.add_tags(note_tag)

    notes.add_note(note)

    result_note = "-"*20 + "\n" + "This note was succesfully added!\n" + \
        "-"*20 + "\n" + str(note) + "\n"

    return result_note


@input_error
def edit_note(user_input):
    try:
        user_split_by_id = user_input.split("id:")
        user_split_by_title = user_split_by_id[1].split("title:")
        user_split_by_body = user_split_by_title[1].split("body:")
    except IndexError:
        return "\nTo edit a note you need to write 'id: ... title: ... body: ...'\n"

    note_id = user_split_by_title[0].strip()
    note_title = user_split_by_body[0].strip()
    note_body = user_split_by_body[1].strip()

    if note_id and note_title and note_body:
        try:
            note_id = int(note_id)
        except ValueError:
            return "\nid must be a number\n"

        notes.edit_note(note_id, note_title, note_body)
        return f"\nNote with id: {note_id} was succesfully changed!\n"
    else:
        return "\nYou need to write something in 'id: ... title: ... body: ...'\n"


@input_error
def remove_note(user_input):
    try:
        list_user_input = user_input.split("id:")
        note_id = list_user_input[1].strip()
    except IndexError:
        return "\nTo remove a note you need to write 'id: ...'\n"

    try:
        note_id = int(note_id)
    except ValueError:
        return "\nid must be a number\n"

    notes.remove_note(note_id)

    return f"\nNote with id: {note_id} was succesfully removed!\n"


def remove_all_notes(user_input):
    if user_input.lower() != "remove_all_notes":
        return "\nThis function does not exist. Try again!\n"

    for note_id in notes.data.keys():
        notes.remove_note(int(note_id))
        if remove_all_notes(user_input) == None:
            return "\nAll notes have been deleted!\n"
        return remove_all_notes(user_input)


def show_notes(user_input):
    user_input_list = user_input.split()
    if len(user_input_list) == 1:
        result_note = []
        for note in notes.show_notes():
            result_note.append(note)
        if result_note:
            return "\n" + "\n--------------------\n".join(result_note)
        else:
            return "\nYour notes list is empty!\n"
    else:
        return "\nThis function does not exist. Try again!\n"


def search_note(user_input):
    user_input = user_input.removeprefix("search_note")
    user_input = user_input.strip()

    if not user_input:
        return "\nYou have to write some content to find a note!\n"

    result_note = []
    for note in notes.show_notes(user_input):
        result_note.append(note)

    if result_note:
        return "\n" + "\n--------------------\n".join(result_note) + "\n"
    else:
        return "\nYou don't have any notes with this content!\n"


def search_by_tags(user_input):
    user_input = user_input.removeprefix("search_by_tags")
    user_input = user_input.strip()
    if not user_input:
        return "\nWrite some tags to find a note!\n"
    user_input = user_input.split(", ")
    result_note = []

    for note in notes.search_and_sort_by_tags(user_input):
        result_note.append(str(note))

    if result_note:
        return "\n" + "\n--------------------\n".join(result_note) + "\n"
    else:
        return "\nNo notes were found by your tags!\n"


@input_error
def add_tags_to_note(user_input):
    try:
        user_split_by_id = user_input.split("id:")
        user_split_by_tags = user_split_by_id[1].split("tags:")
        note_tags = user_split_by_tags[1].strip()
        note_tags = note_tags.split(", ")
    except IndexError:
        return "\nTo add tags you need to write 'id: ... tags: ...'\n"

    try:
        note_id = int(user_split_by_tags[0].strip())
    except ValueError:
        return "\nid must be a number!\n"

    note = notes.data.get(note_id)

    if not note:
        raise IdError

    if note_tags != [""]:
        for tag in note_tags:
            note.add_tags(Tag(tag))
    else:
        return "\nTo add tags you need to write 'id: ... tags: ...'\n"

    return "\nTags were succesfully added!\n"


@input_error
def remove_tags_in_note(user_input):

    try:
        user_split_by_id = user_input.split("id:")
        user_split_by_tags = user_split_by_id[1].split("tags:")

        try:
            note_id = int(user_split_by_tags[0].strip())
        except ValueError:
            return "\nid must be a number!\n"

        note = notes.data.get(note_id)

        if not note:
            raise IdError

        if user_split_by_id[0].strip() == "remove_all_tags_in_note":
            try:
                int(user_split_by_id[1])
                note.remove_all_tags()
                return "\nTags were succesfully removed!\n"
            except ValueError:
                return "\nThis function does not exist. Try again!\n"

        note_tags = user_split_by_tags[1].strip()
        note_tags = note_tags.split(", ")

    except IndexError:
        return "\nTo remove tags you need to write 'id: ... tags: ...'.\nTo remove all tags you need to write 'id: ...'\n"

    for tag in note_tags:
        note.remove_tags(Tag(tag))

    return "\nTags were succesfully removed!\n"


def mark_done(user_input):
    try:
        list_user_input = user_input.split("id:")
        note_id = list_user_input[1].strip()
    except IndexError:
        return "\nTo mark done a note you need to write 'id: ...'\n"

    try:
        note_id = int(note_id)
    except ValueError:
        return "\nid must be a number\n"

    try:
        if list_user_input[0].strip() == "mark_done":
            notes.data.get(note_id).mark_done()
            return "\nNote was marked done!\n"
        else:
            notes.data.get(note_id).unmark_done()
            return "\nNote was unmarked done!\n"
    except AttributeError:
        return "\nThere is no such note!\n"

operations_notes = {
    "show_commands_note": show_commands_note,
    "add_note": add_note,
    "edit_note": edit_note,
    "remove_note": remove_note,
    "remove_all_notes": remove_all_notes,
    "show_notes": show_notes,
    "search_note": search_note,
    "search_by_tags": search_by_tags,
    "add_tags_to_note": add_tags_to_note,
    "remove_tags_in_note": remove_tags_in_note,
    "remove_all_tags_in_note": remove_tags_in_note,
    "mark_done": mark_done,
    "unmark_done": mark_done
}


def get_handler(handler):
    try:
        return operations_notes[handler]
    except:
        return "\nThis function does not exist. Try again!\n"


def get_file_path(file_name):
    path = pathlib.Path(user_data_dir("Personal assistant"))
    if os.name == "nt":
        path = path.parent
    if not path.is_dir():
        path.mkdir()
    file_path = path.joinpath(file_name)
    return file_path


def notes_main_func():
    global notes
    file_path = get_file_path("notes.bin")
    notes.load_from_file(file_path)

    while True:

        notes.save_to_file(file_path)
        user_input = input(">>> ")

        if user_input.lower() in ['close', 'exit']:
            print("\nGood Bye!\n")
            break

        if user_input:
            list_user_input = user_input.split()
            list_user_input[0] = list_user_input[0].lower()

            result_handler = get_handler(list_user_input[0])

            if type(result_handler) == str:
                print(result_handler)
            else:
                print(result_handler(user_input))