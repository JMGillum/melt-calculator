class NamedList:
    def __init__(self, name, items, sorting_name=None):
        self.name = name
        self.items = items
        self.sorting_name = sorting_name

    def name_sorting(self):
        if self.sorting_name:
            return self.sorting_name
        elif self.name:
            return self.name
        else:
            return ""

    def __str__(self):
        if self.name:
            return self.name
        else:
            return ""

    def __list__(self):
        if self.items:
            return self.items
        else:
            return ""

    def __getitem__(self, key):
        return self.items[key]

    def __setitem__(self, key, newvalue):
        self.items[key] = newvalue
