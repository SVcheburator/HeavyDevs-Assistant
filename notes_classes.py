from collections import UserDict
from datetime import datetime


DATE_FORMAT = "%d.%m.%Y"
TIME_FORMAT = "%H:%M"
DATETIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"


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
        if tags:
            for tag in tags:
                self.tags.add(str(tag))
            self.date_modified = datetime.now()

    def remove_tags(self, *tags):
        if tags:
            for tag in tags:
                self.tags.discard(str(tag))
            self.date_modified = datetime.now()

    def remove_all_tags(self):
        if self.tags:
            self.tags.clear()
            self.date_modified = datetime.now()

    def mark_done(self):
        self.flag_done = True

    def unmark_done(self):
        self.flag_done = False

    def __str__(self):
        result = ""
        result += f"Title:\n{self.title}\n"
        result += f"Body:\n{self.body}\n"
        result += f"Tags: {' '.join(self.tags)}\n"
        result += f"Date created: {self.date_created.strftime(DATETIME_FORMAT)}\n"
        result += f"Date modified: {self.date_modified.strftime(DATETIME_FORMAT)}\n"
        result += f"Is done: {self.flag_done}"
        return result


class Tag:
    def __init__(self, tag):
        self.tag = tag.lower()

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

    def remove_note(self, id):
        if self.data.get(id):
            self.data.pop(id)

    def show_notes(self, text=None):
        """
        Returning generator with single pair tuple (id, note) at once
        """
        if not text:
            for id, note in self.data.items():
                yield id, note
        else:
            for id, note in self.data.items():
                if text in note.title or text in note.body:
                    yield id, note

    # Виконує пошук за тегами та показує сортований список нотаток.
    def search_and_sort_by_tags(self, *tags):
        result_search_and_sort_body = []
        result_note = []
        search_tags = []
        for tag in tags:
            search_tags.append(f"#{tag.lower()}")
        for note in self.data.values():
            tags_in_note = []
            note_tags = []
            for tag_note in note.tags:
                note_tags.append(tag_note)
            for tag_search in search_tags:
                if tag_search in note_tags:
                    tags_in_note.append(tag_search)
            if tags_in_note == search_tags:     # Нотатки я сортував по вмісту їхнього body.
                result_search_and_sort_body.append(note.body)
                result_note.append(note)
        result_search_and_sort_body.sort(key=len)
        for index, body in enumerate(result_search_and_sort_body):
            for note in result_note:
                if note.body == body:
                    result_search_and_sort_body[index] = note
        return result_search_and_sort_body
