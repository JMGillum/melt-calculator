#   Author: Josh Gillum              .
#   Date: 10 February 2026          ":"         __ __
#                                  __|___       \ V /
#                                .'      '.      | |
#                                |  O       \____/  |
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
#
#    This file stores the Purchase and CoinData classes. The purchase class
#    represents a purchase or acquisition of a coin (could be multiple of the
#    same coin). CoinData stores information about a coin, and offers a way to
#    print the information in a custom format.
#
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

import weights
import data
from colors import Colors


class Purchase:
    """ Models a coin purchase with information about the price paid, quantity, date of purchase, mint date, and mint mark

    Attributes: 
        purchase_date: A string representing the date of the purchase. Should be a datetime object, or could be a string that will be directly printed.
        mint_date: The mint date of the coin. Optional.
        mint_mark: The mint mark of the coin. Optional.
        date_format: String for the format to pass to strftime to print the date. Used only if purchase_date is not of str type.
        currency_symbol: The currency symbol to display before any prices.
        show_color: Whether to print colored text or not
        colors_8_bit: If show_color is True, will use 8 bit colors if True, otherwise uses 3 bit colors.
        color_purchase: If show_color is True, will print the purchase in this color.
    """
    

    def __init__(
        self,
        price:int|float=None,
        quantity:int=None,
        purchase_date=None,
        mint_date:str|int=None,
        mint_mark:str=None,

        date_format:str="%m/%d/%y",
        currency_symbol:str="$",
        show_color:bool=True,
        colors_8_bit:bool=True,
        color_purchase:str="teal"
    ):
        """

        Args:
            purchase_date: A datetime object (preferred) or a string representing the date of the purchase. 
            price: The price of the purchase
            quantity: The number of items purchased.
            mint_date: The mint date (year) of the coin. Optional.
            mint_mark: The mint mark on the coin. Optional.
            date_format: If purchase_date is a datetime object, display date in this format
            currency_symbol: The currency symbol to print before any price.
            show_color: Whether to display colors.
            colors_8_bit: True to use 8 bit colors, False to use 3 bit colors. Does nothing if show_color is False.
            color_purchase: The color to display the purchase in. Does nothing if show_color is False.
        """

        # Converts price to float
        try:
            self.price = float(price)
        except ValueError:
            self.price = -1.00

        # Converts quantity to int, default is 1 if none is specified
        try:
            if quantity is None:
                self.quantity = 1
            else:
                self.quantity = int(quantity)
        except ValueError:
            self.quantity = -1

        # Sets class instance variables
        self.purchase_date = purchase_date
        self.mint_date = mint_date
        self.mint_mark = mint_mark

        self.date_format=date_format
        self.currency_symbol=currency_symbol
        self.show_color=show_color
        self.colors_8_bit=colors_8_bit
        self.color_purchase=color_purchase

    def __str__(self):
        """ Called whenever the class is cast to str.

        Returns: A string representation of the class, in the form: "(<date>) <mint_date><mint_mark> <currency_symbol><price> [x<quantity> (only if greater than 1)]"
            
        """

        string = ""

        # Converts the date to str
        if self.purchase_date is not None:

            # Does not format date if it is already a string
            if isinstance(self.purchase_date, str) and not (self.purchase_date == ""):
                string += f"({self.purchase_date})"

            # Assumes the date is a datetime object and attempts to format it.
            else:
                try:
                    string += f"({self.purchase_date.strftime(self.date_format)})"
                except AttributeError:
                    pass

        # Adds the mint date
        if self.mint_date is not None and not (self.mint_date == ""):
            string += f" {self.mint_date}"

            # Adds the mint mark
            if self.mint_mark is not None and not (self.mint_mark == ""):
                string += f"{self.mint_mark}"

        # Adds the currency symbol and price
        if self.price is not None:
            string += f" - {self.currency_symbol}{self.price:.2f}"

        # Adds the quantity if it is greater than 1
        if self.quantity is not None:

            # Prints quantity
            if self.quantity > 1:
                string += f" x{self.quantity}"

                # Calculates price * quantity if quantity is greater than 1
                if self.price is not None and self.price >= 0:
                    string += f" ({self.currency_symbol}{self.price * self.quantity:.2f})"

        # Prints the entire string in the self.color_purchase color.
        return Colors.PrintColored(string,self.show_color,self.colors_8_bit,self.color_purchase)


class PurchaseStats:
    """ Models the statistics for purchases. This class is to be used as a bucket for multiple purchases. Such as all purchases for coins made out of silver. 

    Attributes: 
        total: Stores the sum of all purchase prices.
        count: Stores the total number of items purchased.
        delta: Stores the first value to compare the purchase prices to. Ex: melt value of each purchase.
        delta2: Stores the second value to compare the purchase prices to. Ex: sell value of each purchase.
    """


    def __init__(self, total:int|float=0.0, count:int=0, delta:int|float=0.0, delta2:int|float=0.0):
        """ Initializes the PurchaseStats object with the values provided.

        Args:
            total: the total/sum of all the items purchased.
            count: the number of items that have been added together to reach the total
            delta: the difference between the purchase price and value one (typically melt price)
            delta2: the difference between the purchase price and value two (typically sell price)
        """

        self.total = total
        self.count = count
        self.delta = delta
        self.delta2 = delta2


    def add(self, total:int|float, count:int, delta:int|float, delta2:int|float=None):
        """ Adds the information needed to make a new PurchaseStats object to this object

        Args:
            total: The total to add to this object
            count: The count to add to this object
            delta: The delta to add to this object
            delta2: The delta2 to add to this object.
        """

        self.total += total
        self.count += count
        self.delta += delta

        # delta2 is optional
        if delta2 is not None:
            self.delta2 = delta2


    def addPurchase(self,purchase:Purchase,unit_value:int|float,unit_value_2:int|float):
        """ Adds a Purchase object to this object. Purchase object should have price and quantity set beforehand.

        Args:
            purchase: The Purchase object to add to this.
            unit_value: The price per item to add to delta. This is multiplied by Purchase.quantity before being added.
            unit_value_2: The price per item to add to delta2. This is multiplied by Purchase.quantity before being added.
        """

        # Purchase stores the price per item and the number of them purchased, 
        # so have to multiply the two to get the total.
        total = purchase.price * purchase.quantity
        count = purchase.quantity

        # Deltas store the difference between the value and the purchase total,
        # So calculate value and subtract total from it.
        delta = (unit_value*count) - total
        delta2 = (unit_value_2*count) - total

        # Performs the actual addition
        self.add(total,count,delta,delta2)


    def __add__(self,o):
        """ Overloads the addition operator to add two PurchaseStats objects together.

        Args:
            o : Another PurchaseStats object to add to this one. 

        Returns: A new PurchaseStats object the stores the sums of each attribute
            
        """

        # Does the addition and does not save in either of the two operands
        total = self.total + o.total
        count = self.count + o.count
        delta = self.delta + o.delta
        delta2 = self.delta2 + o.delta2

        # Stores the results in a new object.
        return PurchaseStats(total,count,delta,delta2)
        

class CoinData:
    """ Represents a coin and stores information about it.

    Attributes: 
        coin_string: Format string for printing the year, metal weight, metal, gross weight, and fineness
        coin_string_name: Same as coin_string but with the coin_name prepended
        coin_string_value: Format string for printing the melt value and sell value
        coin_string_value_default_retention: Same as coin_string_value but indicates that default retention was used.
        show_value: 
        metal: 
        fineness: 
        precious_metal_weight: 
        years: 
        country: 
        face_value: 
        denomination: 
        nickname: 
        value: 
        currency_symbol: 
        show_color: 
        colors_8_bit: 
        show_metal_colors: 
        metal_colors: 
        use_permille: 
        show_value: 
    """
    # Templates for printing information about one of the member coins
    coin_string = "[%y] ... %a %m (%w @ %p)"
    coin_string_name = f"%n{coin_string}"
    coin_string_value = (
        " - [Melt: %C%v Sell: %C%V]"
    )
    coin_string_value_default_retention = (
        " - [Melt: %C%v Sell: %C(%V)]"
    )


    def FormatYears(self):
        """ Converts the self.years to the desired format (list). If unable to do so, sets to None.

        """
        # Converts a string of x,y,z to a list.
        if isinstance(self.years, str):
            if self.years == self.years[1:]:
                self.years = f"[{self.years}"
            if self.years == "]":
                self.years = self.years[:-1]
            self.years = [int(x) for x in self.years.split(",")]

        # Years is just a single int, so convert it to a list, then return the string.
        elif isinstance(self.years, int):
            self.years = [self.years]
        
        # Worst case, set to None
        elif not isinstance(self.years,list):
            self.years = None


    def ValidateMetal(self):
        """ Validates the current metal saved in self.metals. Sets to other if invalid, and None if other is not defined.

        """
        try:
            data.metals[self.metal]
        except KeyError:
            try:
                data.metals["other"]
                self.metal = "other"
            except KeyError:
                self.metal = None


    def __init__(
        self,
        weight: float | int | weights.Weight = None,
        metal=None,
        fineness=None,
        precious_metal_weight=None,
        years=None,
        country="",
        face_value=None,
        denomination=None,
        nickname="",
        value=0.0,
        retention=None,
        show_value=True,
        config={}

    ):

        # Sets output configuration for instance.
        self.currency_symbol=config["currency_symbol"]
        self.show_color=config["show_color"]
        self.colors_8_bit=config["colors_8_bit"]
        self.show_metal_colors=config["show_metal_colors"]
        self.metal_colors=config["metals_colors"]
        self.use_permille=config["use_permille"]

        self.metal = metal
        self.ValidateMetal()
        self.face_value = face_value
        self.denomination = denomination

        # Sets country name and converts to title if it is a string
        self.country = ""
        if isinstance(country,str):
            self.country = country.title()

        # Converts weights to weights.Weight objects
        self.weight = weights.Weight(weight, weights.Units.GRAMS)
        self.precious_metal_weight = weights.Weight(precious_metal_weight, weights.Units.TROY_OUNCES)
        self.fineness = float(fineness)

        # Precious metal weight was not specified, so calculate it
        if (
            self.precious_metal_weight is None
            and self.weight is not None
            and self.fineness is not None
        ):
            self.precious_metal_weight = weights.Weight(
                self.weight.AsTroyOunces() * self.fineness,
                weights.Units.TROY_OUNCES,
            )

        self.years = years
        self.FormatYears()

        # Sets nickname and converts to title if it is a string
        self.nickname = ""
        if isinstance(nickname, str):
            self.nickname = nickname.title() + " "

        self.value = value

        # Retention was not sepecified, so use default that was passed in config dictionary.
        if retention is None:  
            self.default_retention = True
            self.retention =config["default_retention"]

        # Retention was specified, so use that
        else:
            self.default_retention = False
            self.retention = retention

        # Updated with self.TogglePrice()
        self.show_value = show_value



    def TogglePrice(self, show_price:bool|None=None):
        """ Toggles whether this object will print out values when cast to string.

        Args:
            show_price: Pass nothing to negate the current value or pass a bool to explicitly set it to that.
        """

        # If not explicitly passed, just negate current value.
        if show_price is None:
            self.show_value = not self.show_value

        # Set explicitly
        else:
            self.show_value = bool(show_price)


    def GetCoinString(self):
        """Returns a format string for use with a CoinData object. Depends on settings and information about the coin"""
        string = ""

        # No nickname to show
        if self.nickname is None:
            string = CoinData.coin_string

        # Shows nickname
        else:
            string = CoinData.coin_string_name

        # Shows value
        if self.show_value:

            # Default retention was used, so specify that
            if self.default_retention:
                string += CoinData.coin_string_value_default_retention

            # Retention was specified.
            else:
                string += CoinData.coin_string_value

        return string

    def YearsList(self):
        error_string = "Unknown years"
        if self.years is None or len(self.years) == 0:
            return error_string

        string = "" # The string to be returned

        # Creates sections of years and uses a hyphen to indicate
        # Stretches. Ex: 1931,1932,1933 -> 1931-1933.
        start_year = None # Stores the first year of the section
        previous_year = None # Stores what the previous year was

        # Loops through each year to determine how to display them
        for i in range(len(self.years)):
            year = self.years[i]

            # Sets the start year for the section
            if start_year is None:
                start_year = year

            # Determines if the current year is more than 1 greater than the previous year.
            # If so, end section, and start new one.
            if previous_year is not None and ((year - previous_year) > 1):
                string += f"{start_year}"

                # If multiple years in the section, add x-y
                if not start_year == previous_year:
                    string += f"-{previous_year}"

                string += ","

                # Resets for starting new section
                start_year = year
                previous_year = None

            # Sets previous year to current year to continue loop
            previous_year = year

        # Last section was never closed, so end it
        year = self.years[-1]

        # Section is multiple years, so add x-y
        if previous_year is not None and not start_year == year:
            string += f"{start_year}-{year}"
            start_year = year

        # Otherwise just add year
        else:
            string += f"{year}"

        return string

    def MetalString(self):
        # Options for color display to pass to PrintColored. Default is no color
        color_options = (self.show_color,self.colors_8_bit,"")

        # Attempts to fetch the color of the metal if metals are supposed to be colored
        if self.show_metal_colors:
            try:
                color_options = (self.show_color,self.colors_8_bit,self.metal_colors[self.metal])
            except KeyError:
                pass
        return Colors.PrintColored(data.metals[self.metal][0].title(),*color_options)


    def AsAString(self, format: str):
        """Very simple attempt at a format string for information
        %a - actual precious metal weight
        %c - country
        %C - currency symbol
        %d - denomination
        %f - fineness
        %F - face value
        %m - metal
        %n - nickname
        %p - fineness as a percent (fineness*100)
        %v - value
        %V - Price retention value (value * retention percentage)
        %w - weight
        %y - years
        """
        string = format
        string = string.replace("%c", self.country)
        string = string.replace("%C", self.currency_symbol)
        string = string.replace("%d", str(self.denomination))
        string = string.replace("%F", str(self.face_value))

        # Value
        string = string.replace("%v", f"{round(self.value, 2):.2f}")

        # Value * retention
        string = string.replace("%V",f"{round(self.value * self.retention, 2):.2f}")
        
        # Years
        string = string.replace("%y", self.YearsList())

        # Metal name
        string = string.replace("%m", self.MetalString())
        
        # Fineness
        string = string.replace("%f", f"{self.fineness:.2f}")

        # Either percent or permille, depending on config
        if not self.use_permille:
            string = string.replace("%p", f"{self.fineness * 100:.2f}%")
        else:
            string = string.replace("%p", f"{self.fineness * 1000:.2f}‰")

        # Weights
        string = string.replace("%a",f"{self.precious_metal_weight.AsTroyOunces()} toz")
        string = string.replace("%w",f"{self.weight.AsGrams()}g")

        # Nickname
        string = string.replace("%n",self.nickname)

        return string

    def Print(self, format_string):
        return self.AsAString(format_string)

    def __str__(self):
        return self.AsAString(self.GetCoinString())
