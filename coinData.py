"""
   Author: Josh Gillum              .
   Date: 24 July 2025              ":"         __ __
                                  __|___       \ V /
                                .'      '.      | |
                                |  O       \____/  |
^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

    This file stores the Purchase and CoinData classes. The purchase class
    represents a purchase or acquisition of a coin (could be multiple of the
    same coin). CoinData stores information about a coin, and offers a way to
    print the information in a custom format.

^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
"""

import weights
from datetime import datetime
import metals

import config


class Purchase:
    """Models a coin purchase with information about the price paid, quantity, date of purchase, mint date, and mint mark"""

    def __init__(
        self,
        price=None,
        quantity=None,
        purchase_date=None,
        mint_date=None,
        mint_mark=None,
    ):
        try:
            self.price = float(price)
        except ValueError:
            self.price = -1.00
        try:
            if quantity is None:
                self.quantity = 1
            else:
                self.quantity = int(quantity)
        except ValueError:
            self.quantity = -1
        self.purchase_date = purchase_date
        self.mint_date = mint_date
        self.mint_mark = mint_mark

    def __str__(self):
        string = ""
        if self.purchase_date is not None:
            if isinstance(self.purchase_date, datetime):
                string += f"({self.purchase_date.strftime('%m/%d/%y')})"
            elif isinstance(self.purchase_date, str) and not (self.purchase_date == ""):
                string += f"({self.purchase_date})"
        if self.mint_date is not None and not (self.mint_date == ""):
            string += f" {self.mint_date}"
            if self.mint_mark is not None and not (self.mint_mark == ""):
                string += f"{self.mint_mark}"
        if self.price is not None:
            string += f" - ${self.price:.2f}"
        if self.quantity is not None:
            if self.quantity > 1:
                string += f" x{self.quantity}"
                if self.price is not None and self.price >= 0:
                    string += f" (${self.price * self.quantity})"
        return string


class CoinData:
    # Templates for printing information about one of the member coins
    coin_string = "[%y] ... %a %m (%w @ %p%)"
    coin_string_name = "%n [%y] ... %a %m (%w @ %p%)"
    coin_string_value = " - [Melt: $%v Sell: $%V]"
    coin_string_value_default_retention = " - [Melt: $%v Sell: $(%V)]"

    def __init__(
        self,
        weight: float | int | weights.Weight = None,
        metal=None,
        fineness=None,
        precious_metal_weight=None,
        years=None,
        country=None,
        face_value=None,
        denomination=None,
        nickname=None,
        value=None,
        retention=None,
        show_value=True,
    ):
        if isinstance(weight, float) or isinstance(weight, int):
            self.weight = weights.Weight(weight, weights.Units.GRAMS)
        else:
            self.weight = weight
        self.show_value = show_value
        self.metal = metal
        self.fineness = fineness
        self.precious_metal_weight = precious_metal_weight
        self.years = years
        self.country = country
        self.face_value = face_value
        self.denomination = denomination
        self.nickname = nickname
        if (
            precious_metal_weight is None
            and weight is not None
            and fineness is not None
        ):
            self.precious_metal_weight = weights.Weight(
                round(self.weight.as_troy_ounces() * self.fineness, 4),
                weights.Units.TROY_OUNCES,
            )
        self.value = value
        if not self.value:
            self.value = 0.00
        if (
            retention is None
        ):  # Percentage of melt value that coin is typically bought at
            self.default_retention = True
            self.retention = config.default_retention # Default retention of 97% of melt value
        else:
            self.default_retention = False
            self.retention = retention

    def togglePrice(self, show_price: bool):
        self.show_value = show_price

    def getCoinString(self):
        """Returns a format string for use with a CoinData object. Depends on settings and information about the coin"""
        string = ""
        if self.nickname is None:
            string = CoinData.coin_string
        else:
            string = CoinData.coin_string_name
        if self.show_value:
            if self.default_retention:
                string += CoinData.coin_string_value_default_retention
            else:
                string += CoinData.coin_string_value
        return string

    def yearsList(self):
        if self.years is not None:
            if isinstance(self.years, int):
                return str(self.years)
            if (
                isinstance(self.years, list)
                and len(self.years) > 0
                and isinstance(self.years[0], int)
            ):
                string = ""
                start_year = None
                previous_year = None
                for i in range(len(self.years)):
                    year = self.years[i]
                    if start_year is None:
                        start_year = year
                    if previous_year is not None and ((year - previous_year) > 1):
                        string += f"{start_year}"
                        if not start_year == previous_year:
                            string += f"-{previous_year}"
                        string += ","
                        start_year = year
                        previous_year = None
                    if i >= (len(self.years) - 1):
                        if previous_year is not None:
                            string += f"{start_year}-{year}"
                            start_year = year
                        else:
                            string += f"{year}"
                    previous_year = year

                return string
        return "Unknown years"

    def metalString(self):
        if self.metal is not None:
            if self.metal == metals.Metals.GOLD:
                return "Gold"
            elif self.metal == metals.Metals.SILVER:
                return "Silver"
            elif self.metal == metals.Metals.PLATINUM:
                return "Platinum"
            elif self.metal == metals.Metals.PALLADIUM:
                return "Palladium"
        return "Unknown metal"

    def asAString(self, format: str):
        """Very simple attempt at a format string for information
        %c - country
        %F - face value
        %d - denomination
        %y - years
        %a - actual precious metal weight
        %m - metal
        %f - fineness
        %p - fineness as a percent (fineness*100)
        %w - weight
        %n - nickname
        %v - value
        %V - Price retention value (value * retention percentage)
        """
        string = format
        string = string.replace(
            "%c", "Unknown country" if self.country is None else self.country.title()
        )
        string = string.replace("%d", str(self.denomination))
        string = string.replace("%F", str(self.face_value))
        string = string.replace(
            "%v",
            "Unknown value" if self.value is None else f"{round(self.value, 2):.2f}",
        )
        string = string.replace(
            "%V",
            "Unknown value"
            if (self.value is None)
            else f"{round(self.value * self.retention, 2):.2f}",
        )
        string = string.replace(
            "%y", "Unknown years" if self.years is None else self.yearsList()
        )
        string = string.replace(
            "%m", "Unknown metal" if self.metal is None else self.metalString()
        )
        string = string.replace("%f", str(self.fineness))
        string = string.replace("%p", str(self.fineness * 100))
        string = string.replace(
            "%a",
            "Unknown weight"
            if not isinstance(self.precious_metal_weight, weights.Weight)
            else f"{self.precious_metal_weight.as_troy_ounces()} toz",
        )
        string = string.replace(
            "%w",
            "Unknown weight"
            if not isinstance(self.weight, weights.Weight)
            else f"{self.weight.as_grams()}g",
        )
        string = string.replace("%n", "" if self.nickname is None else self.nickname)
        return string

    def print(self,format_string):
        return self.asAString(format_string)

    def __str__(self):
        return self.asAString(self.getCoinString())
