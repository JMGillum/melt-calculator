import re
import collection
from country import CountryName
import data
import copy


class Search:
    minimum_year = 1800 # Minimum number to be interpreted as a year instead of a denomination
    current_year = 2025 # Current year (used for determining if a number is a year or denomination)

    def __init__(self,country_name=None,year=None,denomination=None,face_value=None,nickname=None,debug=False,data=None,text=None):
        self.country_name = country_name
        self.year = year
        self.denomination = denomination
        self.face_value = face_value
        self.nickname = nickname
        self.debug = debug  # Flag for whether to print out information or not
        self.data = data
        self.text = text

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

        country_names = data.countries

        # Sets the country name and denomination
        if len(words) >= 2:
            for word in words:
                temp = Search.validCountry(word) # checks if word is a valid country name
                if temp is not None:
                    country = temp
                    words.remove(word)
                    break
        elif len(words) > 0:
            temp = Search.validCountry(words[0])
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

    def search(self,country_name=None,year=None,denomination=None,face_value=None,nickname=None,data=None,as_a_collection=False):
        """Searches the data based on the set parameters. as_a_collection will return a CoinCollection object of a deepcopy of the results."""
        # Sets member variables to the values of any provided parameters
        if country_name is not None:
            self.country_name = country_name
        if year is not None:
            self.year = year
        if denomination is not None:
            self.denomination = denomination
        if face_value is not None:
            self.face_value = face_value
        if nickname is not None:
            self.nickname = nickname
        if data is not None:
            self.data = data

        # Converts empty strings to None type
        if self.country_name == "":
            self.country_name = None
        if self.year == "":
            self.year = None
        if self.denomination == "":
            self.denomination = None
        if self.face_value == "":
            self.face_value = None
        if self.nickname == "":
            self.nickname = None

        if self.debug:
            print("Search parameters are as follows:")
            print(f"  Country:      {self.country_name}")
            print(f"  Year:         {self.year}")
            print(f"  Denomination: {self.denomination}")
            print(f"  Face Value:   {self.face_value}")
            print(f"  Nickname:     {self.nickname}")
            print(f"  Returning:    {'Collection' if as_a_collection else 'Any'}")
        if as_a_collection:
            return self.__searchReturnCollection()
        else:
            return self.__searchReturnAny()


    def __searchReturnAny(self):
        """Returns a list of any matching objects. Can by Country(s),Denomination(s), or CoinData"""
        coins = []
        countries = []
        denominations = []
        values = []
        # Narrows down the countries if possible
        if self.country_name is not None:
            countries = Search.lookupCountry(data, self.country_name)
            if ( # if country is provided, return entire Country object.
                self.year is None
                and self.denomination is None
                and self.face_value is None
                and self.nickname is None
            ):
                return countries
        if (
            countries is None or len(countries) <= 0
        ):  # Country doesn't exist in data or name wasn't provided
            countries = data.countries

        if self.debug:
            print("Search filtered down to the following countries: ")
            for item in countries:
                print(f"  {item.name}")

        # Narrows down the denomination if possible
        if self.denomination is not None:
            for item in countries:
                denominations += Search.lookupDenomination(item, self.denomination)
            if self.year is None and self.face_value is None and self.nickname is None: # If only denomination (and optionally country) is provided, return denomination objects
                return denominations
        if (
            denominations is None or len(denominations) <= 0
        ):  # Denomination doesn't exist or wasn't provided
            denominations = []
            for item in countries:
                denominations += item.denominations

        if self.debug:
            print("Search filtered down to the following denominations: ")
            for item in denominations:
                print(f"  {item.name}")

        # One of the more specific parameters is provided, so narrow down results more
        if self.face_value is not None:
            for item in denominations:
                values += Search.lookupValue(item, self.face_value)
        if values is None or len(values) <= 0:
            values = []
            for item in denominations:
                values += item.values

        if self.debug:
            print("Search filtered down to the following values: ")
            for item in values:
                print(f"  {item.name}")

        # Narrows down years
        if self.year is not None and not (self.year == ""):
            coins = []
            for item in values:
                coins += Search.lookupYear(item, self.year)
            if self.debug:
                print("Search found the following coins: ")
                for item in coins:
                    print(f"  {item}")
            return coins

        if self.debug:
            print("Search could not narrow down by year.")

        # Narrows down by nickname
        if self.nickname is not None and not (self.nickname == ""):
            coins = []
            for item in values:
                coins += Search.lookupCoinByNickname(item, self.nickname)
            if self.debug:
                print("Search found the following coins: ")
                for item in coins:
                    print(f"  {item}")
            return coins

        if self.debug:
            print("Search could not narrow down by face value.")

        for item in values:
            coins += item.coins

        if self.debug:
            print("Search found the following coins: ")
            for item in coins:
                print(f"  {item}")

        return coins

    def __searchReturnCollection(self):
        """Returns a deepcopy of the results of the search. This object should be able to be printed or used as normal CoinCollection data."""
        self.data = copy.deepcopy(self.data)

        countries = []
        denominations = []
        values = []
        coins = []

        if self.country_name is not None:
            countries = Search.lookupCountry(self.data,self.country_name) 
            if countries is not None and len(countries) > 0:
                self.data.countries = countries
            else:
                self.data.countries = []
                return self.data

        if self.denomination is not None:
            for country in self.data.countries:
                temp = Search.lookupDenomination(country,self.denomination)
                if denominations is not None and len(temp) > 0:
                    country.denominations = denominations
                    denominations += temp
                else:
                    self.data.countries.remove(country)

        if self.face_value is not None:
            for denomination in denominations:
                temp = Search.lookupValue(denomination,self.face_value)
                if temp is not None and len(temp) > 0:
                    denomination.values = temp
                    values += temp
                else:
                    del(denomination)

        if self.nickname is not None or self.year is not None:
            for value in values:
                temp = []
                temp2 = []
                if self.nickname is not None:
                    temp = Search.lookupCoinByNickname(value,self.nickname)
                if self.year is not None:
                    temp2 = Search.lookupYear(value,self.year)
                temp = list((set(temp)|set(temp2)))
                if temp is not None and len(temp) > 0:
                    value.coins = temp
                    coins += temp
                else:
                    del(value)

        return self.data



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

    def lookupCoinByNickname(data: collection.Value, nickname: str):
        """Looks up CoinData objects from a Value based on nicknames"""
        return [x for x in data.coins if x.nickname.lower() == nickname.lower()]

    def lookupYear(data: collection.Value, year: int):
        """Looks up CoinData objects from a Value based on year"""
        try:
            year = int(year)
        except ValueError:
            return []
        return [x for x in data.coins if year in x.years]

    def countryInfo(name,return_name=True,return_build=True,countries=None):
        """Returns information about a country, if it exists.  
        Name is the name of the country  
        return_name is boolean for whether the proper/main name of the country will be returned
        return_build is boolean for whether the build function of the country will be returned
        countries is a list of (countryName,buildFunction) tuples to search through. If not provided,
        the ones specified in data.countries will be used."""
        if return_name or return_build:
            if countries is None:
                countries = data.countries
                if not isinstance(countries,list):
                    countries = [countries]
                for item in countries:
                    item_name = item
                    if isinstance(item,tuple):
                        item_name = item[0]
                    else:
                        item = (item,None)
                    answer = item_name.lookup(name)
                    if answer is not None: # Determines what to return
                        if return_name and return_build:
                            return item
                        if return_name and not return_build:
                            return item_name
                        if not return_name and return_build:
                            return item[1]
                        else:
                            return None
        return None

    def validCountry(text,countries=None):
        """Determines if the string is a valid country name. Returns country's
        proper/main name on success, and None on failure. Wrapper for Search.countryInfo()"""
        return Search.countryInfo(text,return_build=False,countries=countries)

    def lookupCountryBuild(name,countries=None):
        """Finds the coin build function of a country, if the country is valid.
        Returns a tuple of (countryName,buildFunction) on success, None on fail."""
        return Search.countryInfo(name,return_name=False,countries=countries)


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
