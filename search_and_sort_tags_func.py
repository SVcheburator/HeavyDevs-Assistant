"""
Щоб функція працювала треба додати її в клас Notes.

Пошук можна здійснювати незважаючи на те великою чи маленькою літерою було написано, 
усі теги переводяться до маленьких літер та порівнюються між собою.

У висновку повертається генератор по якому треба проходитись.
"""

# Виконує пошук за тегами та показує сортований список нотаток.


def search_and_sort_by_tags(self, *tags):
    result_search_and_sort_body = []
    result_note = []

    search_tags = []
    for tag in tags:
        search_tags.append(tag.lower())

    for note in self.data.values():
        tags_in_note = []
        note_tags = []
        for tag_note in note.tags:
            note_tags.append(tag_note.lower())

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
