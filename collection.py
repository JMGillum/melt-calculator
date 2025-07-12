from coinData import CoinData
from tree import Tree


class Value:
    """Models a value of a denomination, and can have multiple sets of years, with
    different characteristics."""


    # Templates for printing information about one of the member coins
    coin_string = "[%y] ... %a %m (%w @ %F%)"
    coin_string_name = "%n [%y] ... %a %m (%w @ %F%)"
    coin_string_value = " - [Melt: $%v Sell: $%V]"
    coin_string_value_default_retention = " - [Melt: $%v Sell: $(%V)]"


    def __init__(
        self,
        coins: CoinData | list[CoinData] | None = None,
        face_value: int | float | None = None,
        name: str | None = None,
    ):
        self.show_value = True
        self.name = ""
        if name is not None:
            self.name = name
        self.coins = []  # Collection of CoinData objects representing the different iterations of the coin.
        self.face_value = 0
        if face_value is not None:
            self.face_value = face_value
        if name is None and face_value is not None:
            self.name = str(face_value)
        self.tree = Tree(name=self.name, nodes=self.coins)
        if coins is not None:
            self.addCoin(coins)

    def getCoinString(self,coin:CoinData):
        """Returns a format string for use with a CoinData object. Depends on settings and information about the coin"""
        string = ""
        if isinstance(coin,CoinData):
            if coin.nickname is None:
                string = Value.coin_string
            else:
                string = Value.coin_string_name
            if self.show_value:
                if coin.default_retention:
                    string += Value.coin_string_value_default_retention
                else:
                    string += Value.coin_string_value
        return string
    
    def addCoin(self, coin: CoinData | list[CoinData]):
        """Adds a coin/coins to the list of iterations. Ex: 1916-1945 dimes, 1946-1964 dimes, 1965-present dimes"""
        if isinstance(coin, CoinData):
            coin = [coin]
        if isinstance(coin, list):
            coins = sorted(list(self.coins + coin), key=lambda x: x.years[0]) # Sorts member coins by first year available
            nodes = []
            for item in coins:
                if isinstance(item, CoinData):
                    self.coins.append(item)
                    if item.nickname is None:
                        nodes.append(item.asAString(self.getCoinString(item)))
                    else:
                        nodes.append(item.asAString(self.getCoinString(item)))
            self.tree.set_nodes(nodes) # Updates tree for printout


    def price(self,silver_price,gold_price):
        """Determines the price of coins based on precious metal prices"""
        nodes = []
        for item in self.coins:
            if isinstance(item,CoinData):
                item.price(silver_price,gold_price)
                if item.nickname is None:
                    nodes.append(item.asAString(self.getCoinString(item)))
                else:
                    nodes.append(item.asAString(self.getCoinString(item)))
        self.tree.set_nodes(nodes)

    def print(self):
        """Prints out the information about its member coins"""
        if self.name is not None:
            print(self.name)
        if self.coins is not None and isinstance(self.coins, list):
            for item in self.coins:
                print(item)


class Denomination:
    """Models a denomination of the currency. Ex: Francs, Marks, Dollars"""

    def __init__(
        self, values: Value | list[Value] | None = None, name: str | None = None
    ):
        self.name = ""
        if self.name is not None:
            self.name = name
        self.values = []  # Collection of values of the denomination
        self.tree = Tree(name=self.name, nodes=self.values)
        if values is not None:
            self.addValues(values)

    def addValues(self, values: Value | list[Value]):
        """Adds values to the list. Ex: 10 franc, 20 franc, 100 franc."""
        if isinstance(values, Value):
            values = [values]
        if isinstance(values, list):
            nodes = []
            for item in values:
                if isinstance(item, Value):
                    self.values.append(item)
                    nodes.append(item.tree)
            self.tree.set_nodes(nodes)

    def price(self,silver_price,gold_price):
        """Determines the price of coins based on precious metal prices"""
        nodes = []
        for item in self.values:
            if isinstance(item,Value):
                item.price(silver_price,gold_price)
                nodes.append(item.tree)
        self.tree.set_nodes(nodes)

    def print(self):
        if self.name is not None:
            print(self.name)
        if self.values is not None and isinstance(self.values, list):
            for item in self.values:
                item.print()


class Country:
    def __init__(
        self,
        denominations: Denomination | list[Denomination] | None = None,
        name: str | None = None,
    ):
        self.name = ""
        if name is not None:
            self.name = name
        self.denominations = []  # Country has a set of Denomination Objects
        self.tree = Tree(name=self.name, nodes=self.denominations)
        if denominations is not None:
            self.addDenominations(denominations)

    def addDenominations(self, denominations: Denomination | list[Denomination]):
        """Adds denominations to the list. Ex: Francs, Euros"""
        if isinstance(denominations, Denomination):
            denominations = [denominations]
        if isinstance(denominations, list):
            nodes = []
            for item in denominations:
                if isinstance(item, Denomination):
                    self.denominations.append(item)
                    nodes.append(item.tree)
            self.tree.set_nodes(nodes)

    def price(self,silver_price,gold_price):
        """Determines the price of coins based on precious metal prices"""
        nodes = []
        for item in self.denominations:
            if isinstance(item,Denomination):
                item.price(silver_price,gold_price)
                nodes.append(item.tree)
        self.tree.set_nodes(nodes)
        

    def print(self):
        if self.name is not None:
            print(self.name)
        if self.denominations is not None and isinstance(self.denominations, list):
            for item in self.denominations:
                item.print()


class CoinCollection:
    def __init__(
        self, countries: Country | list[Country] | None = None, name: str | None = None
    ):
        self.name = ""
        if name is not None:
            self.name = name
        self.countries = []  # Data collection is a set of Countries with sets of Denominations with sets of Years
        self.tree = Tree(name=self.name, nodes=self.countries)
        if countries is not None:
            self.addCountries(countries)

    def addCountries(self, countries: Country | list[Country]):
        """Adds a country/countries to the collection"""
        if isinstance(countries, Country):
            countries = [countries]
        if isinstance(countries, list):
            nodes = []
            for item in countries:
                if isinstance(item, Country):
                    self.countries.append(item)
                    nodes.append(item.tree)
            self.tree.set_nodes(nodes)
    
    def price(self,silver_price,gold_price):
        """Determines the price of coins based on precious metal prices"""
        nodes = []
        for item in self.countries:
            if isinstance(item,Country):
                item.price(silver_price,gold_price)
                nodes.append(item.tree)
        self.tree.set_nodes(nodes)

    def print(self):
        if self.name is not None:
            print(self.name)
        if self.countries is not None and isinstance(self.countries, list):
            for item in self.countries:
                item.print()
