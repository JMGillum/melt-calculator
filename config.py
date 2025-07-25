"""
   Author: Josh Gillum              .
   Date: 24 July 2025              ":"         __ __
                                  __|___       \ V /
                                .'      '.      | |
                                |  O       \____/  |
^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

    This file contains basic configuration for the program. Below will be a
    summary of each item that can be configured.

    ->  default_retention: This is the value that is shown when --hide_price
        is not set. It appears as the sell value. This is the percentage of the
        melt value that merchants will typically buy the coin at. Default is
        97%.
    ->  tree_fancy_characters: By default, the tree output by the program uses
        codes that are not included in the basic ASCII mapping, and thus may
        not be supported by your system. Change the value to False to disable
        these characters and revert to basic characters.

^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
"""
# Default price retention value for every coin that does not
# have it explicitly set. Default is 97% (0.97)
default_retention = 0.97

# This dictates whether the tree uses less-supported characters in order
# to improve visuals. Default is True if not set.
tree_fancy_characters = True

currency_symbol = "$".strip()

tab = "  "
