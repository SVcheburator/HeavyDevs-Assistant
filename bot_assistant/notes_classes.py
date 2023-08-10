from collections import UserDict
from datetime import datetime
import pickle


DATE_FORMAT = "%d.%m.%Y"
TIME_FORMAT = "%H:%M"
DATETIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"


TEXT_COLOR = {
    "red": "\033[31m",
    "green": "\033[32m",
    "reset": "\033[0m"
}


class IdError(Exception):
    pass


class Note():
    def __init__(self, title, body, *tags):
        self.date_created = datetime.now()
        self.date_modified = self.date_created
        self.title = title[:50]
        self.body = body
        self.tags = set()
        self.add_tags(*tags)
        self.flag_done = False

    def edit_title(self, title):
        self.title = title[:50]
        self.date_modified = datetime.now()

    def edit_body(self, body):
        self.body = body
        self.date_modified = datetime.now()

    def add_tags(self, *tags):
        tag_note_list = []
        for tag_note in self.tags:
            tag_note_list.append(tag_note.tag)
            
        if tags:
            for tag in tags:
                if not tag.tag in tag_note_list:
                    self.tags.add(tag)
                    self.date_modified = datetime.now()
                    return True
                return False

    def remove_tags(self, tag):
        for my_tag in self.tags:
            if tag == my_tag.tag:
                self.tags.discard(my_tag)
                self.date_modified = datetime.now()
                break

    def remove_all_tags(self):
        if self.tags:
            self.tags.clear()
            self.date_modified = datetime.now()

    def mark_done(self):
        self.flag_done = True
        self.date_modified = datetime.now()

    def unmark_done(self):
        self.flag_done = False
        self.date_modified = datetime.now()

    def get_date_modified(self):
        return self.date_modified

    def __str__(self):
        result = ""
        result += f"Title:\n{self.title}\n"
        result += f"Body:\n{self.body}\n"
        if self.tags:
            result += f"Tags: {' '.join(map(str, self.tags))}\n"
        result += f"Date created: {self.date_created.strftime(DATETIME_FORMAT)}\n"
        result += f"Date modified: {self.date_modified.strftime(DATETIME_FORMAT)}\n"
        result += f"Is done: {self.flag_done}"
        return result


class Tag:
    def __init__(self, tag):
        self.tag = tag.strip().lower()

    def __str__(self):
        return f"#{self.tag}"


class Notes(UserDict):
    def add_note(self, note: Note):
        id = 0
        while True:
            id += 1
            if not self.data.get(id):
                self.data[id] = note
                break

    def edit_note(self, id, title=None, body=None, adding_tags=None, removing_tags=None, flag_clear_tags=False):
        note = self.data.get(id)
        if note:
            if title:
                note.edit_title(title)
            if body:
                note.edit_body(body)
            if adding_tags:
                note.add_tags(*adding_tags)
            if removing_tags:
                note.remove_tags(*removing_tags)
            if flag_clear_tags:
                note.remove_all_tags()
            self.data[id] = note
        else:
            raise IdError("There is no such note")

    def remove_note(self, id):
        if self.data.get(id):
            self.data.pop(id)
        else:
            raise IdError("There is no such note")

    def show_notes(self, text=None):
        """
        Returning generator with single pair tuple (id, note) at once
        """
        if not text:
            for id, note in self.data.items():
                yield f"ID: {id:08}\n{note}\n"
        else:
            for id, note in self.data.items():
                if text.casefold() in note.title.casefold() or text.casefold() in note.body.casefold():
                    yield f"ID: {id:08}\n{note}\n"

    # Виконує пошук за тегами та показує сортований список нотаток.
    def search_and_sort_by_tags(self, tags):
        result_search_and_sort_body = []
        search_tags = []
        for tag in tags:
            search_tags.append(f"#{tag.strip().lower()}")
        for note in self.data.values():
            note_tags = list(map(str, note.tags))
            for tag_search in search_tags:
                if tag_search in note_tags:
                    result_search_and_sort_body.append(note)
                    break
        result_search_and_sort_body.sort(key=Note.get_date_modified, reverse=True)
        return result_search_and_sort_body

    def load_from_file(self, file):
        try:
            with open(file, "rb") as fh:
                self.data = pickle.load(fh)
        except:
            return TEXT_COLOR["red"] + "The file with saved notes not found, corrupted or empty." + TEXT_COLOR["reset"]

    def save_to_file(self, file):
        with open(file, "wb") as fh:
            pickle.dump(self.data, fh)
