from enum import Enum


class Units(Enum):
    """Enumeration class for different units of measure"""

    GRAMS = 0
    OUNCES = 1
    TROY_OUNCES = 2


class Weight:
    """Represents a weight and provides conversion functions. Can store weights as grams, ounces, or troy ounces, and can report them in either of the 3."""
    def __init__(self, weight: float | int, units: Units):
        if isinstance(weight, int):
            weight = float(weight)
        self.weight = weight
        self.units = units

    def get_weight(self, units: Units):
        """Returns the stored weight in the specified units"""
        if units == Units.GRAMS:
            return self.as_grams
        if units == Units.OUNCS:
            return self.as_ounces
        if units == Units.TROY_OUNCES:
            return self.as_troy_ounces

    def as_grams(self):
        """Returns the stored weight in grams. -1 on error"""
        if self.units == Units.GRAMS:
            return self.weight
        elif self.units == Units.OUNCES:
            return self.weight * 28.34952
        elif self.units == Units.TROY_OUNCES:
            return self.weight * 31.10348
        else:
            return -1.0

    def as_ounces(self):
        """Returns the stored wieght in ounces. -1 on error"""
        if self.units == Units.GRAMS:
            return self.weight * 0.03527396
        elif self.units == Units.OUNCES:
            return self.weight
        elif self.units == Units.TROY_OUNCES:
            return self.weight * 1.097143
        else:
            return -1.0

    def as_troy_ounces(self):
        """Returns the stored weight in troy ounces. -1 on error"""
        if self.units == Units.GRAMS:
            return self.weight * 0.03215075
        elif self.units == Units.OUNCES:
            return self.weight * 0.9114583
        elif self.units == Units.TROY_OUNCES:
            return self.weight
        else:
            return -1.0
