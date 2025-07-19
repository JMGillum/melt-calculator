class CountryName:
    """Class for representing a country along with its alternative names."""
    def __init__(self, name: str, other_names: str | list[str] | None = None):
        """Name is primary name, other names is a list of alternative names. Ex: name=France, other_names=[French,Francais]"""
        self.name = name
        if isinstance(other_names, str):
            other_names = [other_names]
        self.other_names = other_names

    def lookup(self, text: str, case_sensitive=False):
        """Determines if the provided string is one of the country's associated names. Returns the country's official/primary name if it is. Returns None if it isn't"""
        if case_sensitive:
            if text == self.name:
                return self.name
            if self.other_names is not None:
                for name in self.other_names:
                    if text == name:
                        return self.name
        else:
            if text.lower() == self.name.lower():
                return self.name
            if self.other_names is not None:
                for name in self.other_names:
                    if text.lower() == name.lower():
                        return self.name
        return None

    def print(self, all_names=False):
        print(self.name)
        if all_names and self.other_names is not None:
            print(" AKA - ")
            for name in self.other_names:
                print(f"{name}, ")

    def __str__(self):
        return self.name()
