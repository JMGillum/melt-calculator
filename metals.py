"""
   Author: Josh Gillum              .
   Date: 31 July 2025              ":"         __ __
                                  __|___       \ V /
                                .'      '.      | |
                                |  O       \____/  |
^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

    The Metals class is simply an enumeration that facilitates storage of
    metal types. It can easily be expanded to contain more metal types, but
    currently only silver and gold are used in any meaningful capacity.

    An example of the usage would be:

    CoinData(
        name = ...
        years = ...
        metal = Metals.SILVER,
        ...
    )

    Then, to see if the coin is metal, one could simply do:

        if coin.metal == Metals.SILVER

    * See coinData.py for examples of this in use


^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
"""

from enum import Enum


class Metals(Enum):
    """Enumeration class for metal types"""

    OTHER = 0
    SILVER = 1
    GOLD = 2
    PLATINUM = 3
    PALLADIUM = 4
    RHODIUM = 5

    def fromString(string):
        s = string.lower()
        if s == "silver" or s == "ag":
            return Metals.SILVER
        if s == "gold" or s == "au":
            return Metals.GOLD
        if s == "platinum" or s == "pt":
            return Metals.PLATINUM
        if s == "palladium" or s == "pd":
            return Metals.PALLADIUM
        if s == "rhodium" or s == "rh":
            return Metals.RHODIUM
        else:
            return Metals.OTHER
