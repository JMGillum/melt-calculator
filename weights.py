#   Author: Josh Gillum              .
#   Date: 19 February 2026          ":"         __ __
#                                  __|___       \ V /
#                                .'      '.      | |
#                                |  O       \____/  |
# ~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
#
#    The Weight class facilitates storage of weights, regardless of units.
#    Weights can be stored in any of the three systems that are meaningful to
#    coins: grams, avoirdupois (typical/standard) ounces, and troy ounces.
#    Regardless of which system the weight was input in, it can be retrieved
#    in any system, using the as_x() functions.
#
#    The Units class is used to identify which system a current weight is.
#
# ~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

from enum import Enum


class Units(Enum):
    """Enumeration class for different units of measure"""

    GRAMS = 0
    OUNCES = 1
    TROY_OUNCES = 2


class Weight:
    """ Represents a weight and provides conversion functions. Can store weights as grams, ounces, or troy ounces, and can report them in either of the 3.

    Attributes: 
        weight: The weight being stored, as a float
        units: What units the weight is in
    """

    def __init__(self, weight: float | int, units: Units):
        if isinstance(weight, Weight):
            return weight

        # Defaults to 0.0 grams
        if weight is None:
            weight = 0.0
            units = Units.GRAMS
        weight = float(weight)
        self.weight = weight
        self.units = units

    def GetWeight(self, units: Units):
        """Returns the stored weight in the specified units"""
        if units == Units.GRAMS:
            return self.AsGrams
        if units == Units.OUNCES:
            return self.AsOunces
        if units == Units.TROY_OUNCES:
            return self.AsTroyOunces

    def AsGrams(self):
        """Returns the stored weight in grams. -1 on error"""
        if self.units == Units.GRAMS:
            return self.weight
        elif self.units == Units.OUNCES:
            return self.weight * 28.34952
        elif self.units == Units.TROY_OUNCES:
            return self.weight * 31.10348
        else:
            return -1.0

    def AsOunces(self):
        """Returns the stored wieght in ounces. -1 on error"""
        if self.units == Units.GRAMS:
            return self.weight * 0.03527396
        elif self.units == Units.OUNCES:
            return self.weight
        elif self.units == Units.TROY_OUNCES:
            return self.weight * 1.097143
        else:
            return -1.0

    def AsTroyOunces(self):
        """Returns the stored weight in troy ounces. -1 on error"""
        if self.units == Units.GRAMS:
            return self.weight * 0.03215075
        elif self.units == Units.OUNCES:
            return self.weight * 0.9114583
        elif self.units == Units.TROY_OUNCES:
            return self.weight
        else:
            return -1.0
