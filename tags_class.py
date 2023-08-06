
"""
Так як Володимир казав, що теги у нас мають зберігатись в окремому класі, то роблю окремий клас з тегами. 

При додаванні у клас note додається список, тому треба буде по ньому пройтись, 
щоб дістатись до кожного з тегів.
"""


class Tag:
    def __init__(self, *tags):
        self.tags = []
        self.add_tags(*tags)

    def add_tags(self, *tags):  # Додавання тегів
        if tags:
            for tag in tags:
                self.tags.append(tag)

    def remove_tags(self, *tags):  # Видалення тегів
        if tags:
            for tag in tags:
                self.tags.remove(tag)

    def show_tag(self, *tags):  # Цю функцію можна використовувати для додавання в клас note
        result_tags = []
        if tags:
            for tag in self.tags:
                for tag2 in tags:
                    if tag2.lower() in tag.lower():
                        result_tags.append(tag)
        return result_tags

    def show_all_tags(self):  # Покаже усі теги, що записані
        return self.tags
