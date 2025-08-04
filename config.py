#   Author: Josh Gillum              .
#   Date: 4 August 2025             ":"         __ __
#                                  __|___       \ V /
#                                .'      '.      | |
#                                |  O       \____/  |
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
#
#    This file contains basic configuration for the program. Below will be a
#    summary of each item that can be configured.
#
#    ->  default_retention: This is the value that is shown when --hide_price
#        is not set. It appears as the sell value. This is the percentage of the
#        melt value that merchants will typically buy the coin at. Default is
#        97%.
#    ->  tree_fancy_characters: By default, the tree output by the program uses
#        codes that are not included in the basic ASCII mapping, and thus may
#        not be supported by your system. Change the value to False to disable
#        these characters and revert to basic characters.
#    ->  currency_symbol: The symbol that will be displayed to the left of
#        prices. Default value is '$'.
#    ->  current_year: This is the current year. This is used for coins that
#        are still in production. Also used to mark the upper bound for values
#        that can be interpreted as a year. Numbers larger than this are
#        interpreted as face values.
#    ->  minimum_year: This is the smallest number that can be interpreted as
#        a year. This number should be as large as possible while still
#        representing the entire data set. Numbers smaller than this will be
#        interpreted as face values of coins.
#    ->  date_format: The format for displaying dates. Mainly used for 
#        purchases. Must be a string. '%m' is replaced with the month, '%d' the
#        day, and '%y' the year.
#    ->  bullion_hint: This is text that is placed next to all bullion
#        denominations. Set to empty string to not print anything.
#    ->  show_color: This enables or disables color printing in the terminal.
#        Set to False if weird output is occuring. Default value is True
#
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

# Default price retention value for every coin that does not
# have it explicitly set. Default is 97% (0.97)
default_retention = 0.97

# This dictates whether the tree uses less-supported characters in order
# to improve visuals. Default is True if not set.
tree_fancy_characters = True

currency_symbol = "$"

current_year = 2025  # Current year
minimum_year = (
    1800  # Earliest number that will be considered a year and not a face value
)
date_format = "%m/%d/%y"

bullion_hint = " (Bullion)"

show_color = True
colors_8_bit = True
country_color = "blue"
denomination_color = "purple"
bullion_color = "magenta"
value_color = "yellow"
gain_color = "green"
loss_color = "red"
purchase_color = "teal"

# 1. Database Connection Parameters
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": None,
    "database": "coin_data",
}
