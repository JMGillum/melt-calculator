"""
   Author: Josh Gillum              .
   Date: 24 July 2025              ":"         __ __
                                  __|___       \ V /
                                .'      '.      | |
                                |  O       \____/  |
^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

    Adds tagging to a NamedList, which can make identifying coins a lot easier.

^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
"""

from coins.namedList import NamedList

class TaggedList(NamedList):
    def __init__(self,name,items,sorting_name=None,tags=None):
        super().__init__(name,items,sorting_name)
        if not isinstance(tags,list):
            tags = [tags]
        self.tags = tags


