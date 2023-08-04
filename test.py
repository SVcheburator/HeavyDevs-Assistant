from notes_classes import Note, Notes

def show_notes(self, text=None):
        result = ""
        if not self.data:
            result = "There is no notes"
        elif not text:
            for id, note in self.data.items():
                result += f"\nNote #{id:08}:\n{str(note)}\n"
        else:
            for id, note in self.data.items():
                if text in note.title or text in note.body:
                    result += f"\nNote #{id:08}:\n{str(note)}\n"
        if not result:
            return "Not found"
        return result

note = Note("Title523555555555555555555555555555555555555555555555522222222222222225", "Body", "fs", "fsfs", "gs", "42342")
print(note)
note.remove_tags("rwerw")
print(note)
note.mark_done()
note.remove_tags("gs")
print(note)
note.remove_all_tags()
print(note)
note.add_tags("rwerw")
print(note)
note.unmark_done()
note.add_tags("rwerw")
note.add_tags("rwerw")
print(note)
notes = Notes()
notes.add_note(note)
notes.edit_note(2)
print(notes)
notes.edit_note(1, "New title", "New body3", ["qwrewrw"], ["qwrewrw"], True)
print(notes)
for i in range(10):
    note = Note("Title2"+str(i), "Body2", "fs", "fsfs", "gs", "42342")
    notes.add_note(note)
print(notes)
for id, note in notes.show_notes():
     print(id, note)

notes.remove_note(5)
notes.remove_note(8)
print(notes.data.keys())
note = Note("Title42342", "Body2", "fs", "fsfs", "gs", "42342")
notes.add_note(note)
print(notes.data.keys())
print("-----------------------------")
for id, note in notes.show_notes("4"):
     print(id, note)