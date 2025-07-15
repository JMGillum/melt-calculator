import re
import collection
from country import CountryName
import data


class Search:
    minimum_year = 1800 # Minimum number to be interpreted as a year instead of a denomination
    current_year = 2025 # Current year (used for determining if a number is a year or denomination)

    def __init__(self):
        self.country = None
        self.year = None
        self.denomination = None
        self.face_value = None
        self.nickname = None
        self.debug = False  # Flag for whether to print out information or not
        self.data = None

    def parseSearchString(self, text: str):
        """Parses a string to extract the country's name, year, denomination, and face value"""
        numbers = re.findall("\d+", text) # Regex finds all strings of digits
        words = re.findall("[a-zA-Z]+", text) # Same for words

        year = ""
        denomination = ""
        country = ""
        face_value = ""
        # If more than two numbers, picks year and denomination
        if len(numbers) >= 2:
            if len(numbers[0]) != 4 and len(numbers[1]) == 4:
                year = numbers[1]
                face_value = numbers[0]
            else:
                year = numbers[0]
                face_value = numbers[1]
        elif len(numbers) == 1: # Only one number found
            if len(numbers[0]) == 4: # Checks if number is 4 digits (a year), then checks if within provided range
                temp = int(numbers[0])
                if temp >= Search.minimum_year and temp <= Search.current_year:
                    year = numbers[0]
                else: # If not, uses number as face value
                    face_value = numbers[0]
            else:
                face_value = numbers[0]

        country_names = Search.countryNames()

        # Sets the country name and denomination
        if len(words) >= 2:
            for word in words:
                temp = Search.validCountry(country_names, word) # checks if word is a valid country name
                if temp is not None:
                    country = temp
                    words.remove(word)
                    break
        elif len(words) > 0:
            temp = Search.validCountry(country_names, words[0])
            if temp:
                country = temp
            else:
                denomination = words[0]

        if self.debug:
            print(
                f"COUNTRY:{country},DENOMINATION:{denomination},YEAR:{year},FACE VALUE:{face_value}"
            )

        # Sets values to None if they weren't found
        if country == "":
            self.country = None
        else:
            self.country = country
        if year == "":
            self.year = None
        else:
            self.year = year
        if face_value == "":
            self.face_value = None
        else:
            self.face_value = face_value
        if denomination == "":
            self.denomination = None
        else:
            self.denomination = denomination

    def search(self):
        """Searches the data based on the set parameters"""
        country_name = self.country
        year = self.year
        denomination = self.denomination
        face_value = self.face_value
        nickname = self.nickname
        data = self.data
        if country_name == "":
            country_name = None
        if year == "":
            year = None
        if denomination == "":
            denomination = None
        if face_value == "":
            face_value = None
        if nickname == "":
            nickname = None
        coins = []
        countries = []
        denominations = []
        values = []

        # Narrows down the countries if possible
        if country_name is not None:
            countries = Search.lookupCountry(data, country_name)
            if ( # if country is provided, return entire Country object.
                year is None
                and denomination is None
                and face_value is None
                and nickname is None
            ):
                return countries
        if (
            countries is None or len(countries) <= 0
        ):  # Country doesn't exist in data or name wasn't provided
            countries = data.countries

        # Narrows down the denomination if possible
        if denomination is not None:
            for item in countries:
                denominations += Search.lookupDenomination(item, denomination)
            if year is None and face_value is None and nickname is None: # If only denomination (and optionally country) is provided, return denomination objects
                return denominations
        if (
            denominations is None or len(denominations) <= 0
        ):  # Denomination doesn't exist or wasn't provided
            denominations = []
            for item in countries:
                denominations += item.denominations

        # One of the more specific parameters is provided, so narrow down results more
        if face_value is not None:
            for item in denominations:
                values += Search.lookupValue(item, face_value)
        if values is None or len(values) <= 0:
            values = []
            for item in denominations:
                values += item.values

        # Narrows down years
        if year is not None and not (year == ""):
            coins = []
            for item in values:
                coins += Search.lookupYear(item, year)
            return coins

        # Narrows down by nickname
        if nickname is not None and not (nickname == ""):
            coins = []
            for item in values:
                coins += Search.lookupValueByNickname(item, nickname)
            return coins

        for item in values:
            coins += item.coins

        return coins

    def performSearch(self, data: collection.CoinCollection, search_string: str):
        """Function to be called from outside of class. Performs search of provided string on provided data"""
        self.data = data
        self.parseSearchString(search_string)
        # return self.search(data,country_name=arguments[0],year=arguments[1],denomination=arguments[3],face_value=arguments[2])
        return self.search()

    def lookupCountry(data: collection.CoinCollection, name: str | list[str]):
        """Looks up the country object in the collection"""
        if isinstance(name, str):
            return [x for x in data.countries if x.name.lower() == name.lower()]
        elif isinstance(name, list):
            countries = []
            for item in name:
                countries += [
                    x for x in data.countries if x.name.lower() == item.lower()
                ]
            return countries

    def lookupDenomination(data: collection.Country, name: str):
        """Looks up the denomination within the country object"""
        return [x for x in data.denominations if x.name.lower() == name.lower()]

    def lookupValue(data: collection.Denomination, face_value: int):
        """Looks up a face value within a denomination"""
        try:
            face_value = int(face_value)
        except ValueError:
            return []
        return [x for x in data.values if x.face_value == face_value]

    def lookupValueByNickname(data: collection.Value, nickname: str):
        """Looks up CoinData objects from a Value based on nicknames"""
        return [x for x in data.coins if x.nickname.lower() == nickname.lower()]

    def lookupYear(data: collection.Value, year: int):
        """Looks up CoinData objects from a Value based on year"""
        try:
            year = int(year)
        except ValueError:
            return []
        return [x for x in data.coins if year in x.years]

    def validCountry(countries, text):
        """Determines if the string is a valid country name"""
        for name in countries:
            answer = name.lookup(text)
            if answer is not None:
                return answer
        return None

    def lookupCountryBuild(name,countries=None):
        """Finds the coin build function of a country, if the country is valid.
        Returns a tuple of (countryName,buildFunction) on success, None on fail."""
        if countries is None:
            countries = Search.countryNames(with_functions=True)
        for item in countries:
            if isinstance(item,tuple):
                answer = item[0].lookup(name)
                if answer is not None:
                    return item
        return None


    def countryNames(with_functions=False):
        """Initialization function for country names. Optional with_functions parameter
        will return a list of tuples of the form (CountryName,country coin build function)"""
        france = CountryName("France", ["French"])
        mexico = CountryName("Mexico", ["Mexican"])
        united_states = CountryName(
            "United States",
            ["US", "USA", "United States of America", "America", "American"],
        )
        germany = CountryName("Germany", ["Deutschland", "German"])
        italy = CountryName("Italy",["Italian","Italia"])
        canada = CountryName("Canada",["Canadian"])

        if with_functions:
            france = (france,data.coinsFrance)
            mexico = (mexico,data.coinsMexico)
            united_states = (united_states,data.coinsUnitedStates)
            germany = (germany,data.coinsGermany)
            italy = (italy,data.coinsItaly)
            canada = (canada,data.coinsCanada)

        return [france, mexico, united_states, germany,italy,canada]
