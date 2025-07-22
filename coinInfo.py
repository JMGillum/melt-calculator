"""
   Author: Josh Gillum              .
   Date: 18 July 2025              ":"         __ __
                                  __|___       \ V /
                                .'      '.      | |
                                |  O       \____/  |
^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

    This file contains the actual data about all the coins used in the program.
    The typical structure used is:
        <Country> - Ex: Germany
            <Denomination> - Ex: Mark
                <Face value> - Ex: 10
                    <Set of years> - 1871-1915

    This structure allows for changes within the composition of a coin to be
    reflected. In order to add any new coins, each element of the structure
    must exist. First off is to add the actual coin data, with the aptly named
    CoinData class. See coinData.py for more information on the different data
    that can be stored.

    An example of the structure will follow. This is useful if you wish to add
    any new coins or modify existing ones.

    1. An entry must to the coins dictionary within the Coins class must be
    made. Below represents the 5 dollar Canadian Silver Maple Leaf coin,
    minted from 1988 to 2025 (current-year as of writing).


        "canada_dollar_5": Node(
            CoinData(
                nickname="Silver Maple Leaf Bullion",
                years=list(range(1988, 2026)),
                weight=31.11,
                fineness=0.9999,
                precious_metal_weight=weights.Weight(1, weights.Units.TROY_OUNCES),
                metal=Metals.SILVER,
                country="Canada",
                face_value=5,
                denomination="Dollars",
            )
        ),

    * The key needs to be some unique name that describes the coin. This value 
    is never displayed, so do not worry if it is a bit long or drawn out. 
    * The CoinData object must be the data variable of a Node object. See
    tree/node.py for more information on the Node class.
    * The CoinData object stores the actual information about the coin, once
    again, see coinData.py for information on the fields.

    2. An entry to the values dictionary in the Coins class must be added.
    This entry represents all of the coins of this face value, so all 5 
    dollar Canadian coins. If there are multiple coins of this face value, 
    place all of their keys inside the list. Using the above coin, the entry
    would be:

        "canada_dollar_5": NamedList("5", ["canada_dollar_5"]),

    * The NamedList class is simply a list with a name. The name gets returned
    whenever the list is cast to a string.

    3. An entry to the denominations dictionary in the Coins class must then
    be added. This entry represents all Canadian coins of the Dollar
    denomination. The modern Canadian monetary system also uses cents (ex:
    1 cent, 5 cent, 10 cent, etc.), which would have to be its own entry in
    this dictionary. Continuing with the example, the entry would be:

        "canada_dollar": NamedList("Dollars", ["canada_dollar_5"]),

    * Inside the list would be all face values of the Canadian dollar.

    4. Finally, an entry to the countries dictionary in the Coins class must
    be added. This represents all coins of the country (it could also be an
    issuing authority...). Below is the example entry:


        "canada": NamedList("Canada", ["canada_dollar"]),

    * The list stores all denominations for this country, so if coins 
    of the Canadian cent denomination were also defined, the Canadian cent
    denomination would have to be included in the list.

    * The coins_reverse_build dictionary must also be updated. Each entry
    is of the form <coin_id>:(face_value_id, denomination_id, country_id).
    Where each id is the corresponding key in each of the dictionaries. See
    helper.py for information on how to update this.

    ** Note that the NamedList object stores the keys for the objects of the
    lower tier that they represent. So, the "canada_dollar" denomination entry
    stores the keys of all Canadian dollar face_values, as defined in the
    values dictionary.

    ** See purchases.py if you would like to add your personal collection.

^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
"""

from coinData import CoinData
from tree.tree import Tree
from tree.node import Node
from metals import Metals
from purchases import purchases
import weights


class NamedList:
    def __init__(self, name, items):
        self.name = name
        self.items = items

    def __str__(self):
        if self.name:
            return self.name
        else:
            return ""

    def __list__(self):
        if self.items:
            return self.items
        else:
            return ""

    def __getitem__(self, key):
        return self.items[key]

    def __setitem__(self, key, newvalue):
        self.items[key] = newvalue


class Coins:
    coins = {
        # Canada
        "canada_dollar_5": Node(
            CoinData(
                nickname="Silver Maple Leaf Bullion",
                years=list(range(1988, 2026)),
                weight=31.11,
                fineness=0.9999,
                precious_metal_weight=weights.Weight(1, weights.Units.TROY_OUNCES),
                metal=Metals.SILVER,
                country="Canada",
                face_value=5,
                denomination="Dollars",
            )
        ),
        # France
        "centimes_20": Node(
            data=CoinData(
                years=list(range(1848, 1921)),
                weight=1,
                fineness=0.9,
                metal=Metals.SILVER,
                country="France",
                face_value=20,
                denomination="Centimes",
            )
        ),
        "centimes_50_1": Node(
            data=CoinData(
                years=list(range(1848, 1867)),
                weight=2.5,
                fineness=0.9,
                metal=Metals.SILVER,
                country="France",
                face_value=50,
                denomination="Centimes",
            )
        ),
        "centimes_50_2": Node(
            data=CoinData(
                years=list(range(1866, 1921)),
                weight=2.5,
                fineness=0.835,
                metal=Metals.SILVER,
                country="France",
                face_value=50,
                denomination="Centimes",
            )
        ),
        "franc_1_1": Node(
            CoinData(
                years=list(range(1848, 1867)),
                weight=5,
                fineness=0.9,
                metal=Metals.SILVER,
                country="France",
                face_value=1,
                denomination="Franc",
            )
        ),
        "franc_1_2": Node(
            CoinData(
                years=list(range(1866, 1921)),
                weight=5,
                fineness=0.835,
                metal=Metals.SILVER,
                country="France",
                face_value=1,
                denomination="Franc",
            )
        ),
        "franc_2": Node(
            CoinData(
                years=list(range(1848, 1921)),
                weight=10,
                fineness=0.9,
                metal=Metals.SILVER,
                country="France",
                face_value=2,
                denomination="Franc",
            )
        ),
        "franc_5_1": Node(
            CoinData(
                years=list(range(1848, 1921)),
                weight=25,
                fineness=0.9,
                metal=Metals.SILVER,
                country="France",
                face_value=5,
                denomination="Franc",
            )
        ),
        "franc_5_2": Node(
            CoinData(
                years=list(range(1960, 1970)),
                weight=12,
                fineness=0.835,
                metal=Metals.SILVER,
                country="France",
                face_value=5,
                denomination="Franc",
            )
        ),
        "franc_5_3": Node(
            CoinData(
                years=list(range(1848, 1915)),
                weight=1.6129,
                fineness=0.9,
                metal=Metals.GOLD,
                country="France",
                face_value=5,
                denomination="Franc",
            )
        ),
        "franc_10_1": Node(
            CoinData(
                years=[x for x in list(range(1929, 1940)) if x not in [1935, 1936]],
                weight=10,
                fineness=0.68,
                metal=Metals.SILVER,
                country="France",
                face_value=10,
                denomination="Franc",
            )
        ),
        "franc_10_2": Node(
            CoinData(
                years=list(range(1848, 1915)),
                weight=3.2258,
                fineness=0.90,
                metal=Metals.GOLD,
                country="France",
                face_value=10,
                denomination="Franc",
            )
        ),
        "franc_20_1": Node(
            data=CoinData(
                years=[x for x in range(1906, 1915)],
                weight=6.4516,
                fineness=0.9,
                metal=Metals.GOLD,
                country="France",
                face_value=20,
                denomination="Franc",
            ),
            nodes=[],
        ),
        "franc_20_2": Node(
            CoinData(
                years=list(range(1929, 1940)),
                weight=20,
                fineness=0.68,
                metal=Metals.SILVER,
                country="France",
                face_value=20,
                denomination="Franc",
            )
        ),
        "franc_50": Node(
            CoinData(
                years=list(range(1848, 1915)),
                weight=16.129,
                fineness=0.9,
                metal=Metals.GOLD,
                country="France",
                face_value=20,
                denomination="Franc",
            )
        ),
        "franc_100_1": Node(
            CoinData(
                years=[x for x in range(1982, 2001)],
                weight=15,
                fineness=0.9,
                metal=Metals.SILVER,
                country="France",
                face_value=100,
                denomination="Franc",
                retention=0.70,
            )
        ),
        "franc_100_2": Node(
            CoinData(
                years=list(range(1848, 1915)),
                weight=32.2581,
                fineness=0.9,
                metal=Metals.GOLD,
                country="France",
                face_value=100,
                denomination="Franc",
            )
        ),
        "franc_100_3": Node(
            CoinData(
                years=list(range(1929, 1937)),
                weight=6.55,
                fineness=0.9,
                metal=Metals.GOLD,
                country="France",
                face_value=100,
                denomination="Franc",
            )
        ),
        # Germany
        "mark_10": Node(
            CoinData(
                years=list(range(1871, 1916)),
                weight=3.9825,
                fineness=0.900,
                retention=0.97,
                metal=Metals.GOLD,
                country="Germany",
                face_value=10,
                denomination="Mark",
            )
        ),
        # Italy
        "centesimi_20": Node(
            CoinData(
                years=list(range(1863, 1918)),
                weight=1,
                fineness=0.835,
                metal=Metals.SILVER,
                country="Italy",
                face_value=20,
                denomination="Centesimi",
            )
        ),
        # Mexico
        "peso_1": Node(
            CoinData(
                years=[
                    x
                    for x in list(range(1920, 1946))
                    if x not in list(range(1928, 1932)) + [1936, 1937, 1939, 1941, 1942]
                ],
                weight=16.66,
                fineness=0.72,
                metal=Metals.SILVER,
                country="Mexico",
                face_value=1,
                denomination="Peso",
            )
        ),
        # United States
        "barber_dime": Node(
            CoinData(
                nickname="Barber Dime",
                years=[x for x in list(range(1892, 1917))],
                weight=2.5,
                fineness=0.900,
                metal=Metals.SILVER,
                country="United States",
                face_value=10,
                denomination="Cents",
            )
        ),
        "mercury_dime": Node(
            CoinData(
                nickname="Mercury Dime",
                years=[
                    x for x in list(range(1916, 1946)) if x not in [1922, 1932, 1933]
                ],
                weight=2.5,
                fineness=0.900,
                metal=Metals.SILVER,
                country="United States",
                face_value=10,
                denomination="Cents",
            )
        ),
        "roosevelt_dime": Node(
            CoinData(
                nickname="Roosevelt Dime",
                years=[x for x in list(range(1946, 1965))],
                weight=2.5,
                fineness=0.900,
                metal=Metals.SILVER,
                country="United States",
                face_value=10,
                denomination="Cents",
            )
        ),
        "barber_quarter": Node(
            CoinData(
                nickname="Barber Quarter",
                years=list(range(1892, 1917)),
                weight=6.25,
                fineness=0.900,
                metal=Metals.SILVER,
                country="United States",
                face_value=25,
                denomination="Cents",
            )
        ),
        "standing_liberty_quarter": Node(
            CoinData(
                nickname="Standing Liberty Quarter",
                years=[x for x in list(range(1916, 1931)) if x not in [1922]],
                weight=6.25,
                fineness=0.900,
                metal=Metals.SILVER,
                country="United States",
                face_value=25,
                denomination="Cents",
            )
        ),
        "washington_quarter": Node(
            CoinData(
                nickname="Washington Quarter",
                years=[x for x in list(range(1932, 1965)) if x not in [1933]],
                weight=6.25,
                fineness=0.900,
                metal=Metals.SILVER,
                country="United States",
                face_value=25,
                denomination="Cents",
            )
        ),
        "walking_liberty_half": Node(
            CoinData(
                nickname="Walking Liberty Half",
                years=[
                    x
                    for x in list(range(1916, 1948))
                    if x
                    not in ([1922] + list(range(1924, 1927)) + list(range(1930, 1933)))
                ],
                weight=12.5,
                fineness=0.900,
                metal=Metals.SILVER,
                country="United States",
                face_value=50,
                denomination="Cents",
            )
        ),
        "benjamin_half": Node(
            CoinData(
                nickname="Benjamin Half",
                years=[x for x in list(range(1948, 1964))],
                weight=12.5,
                fineness=0.900,
                metal=Metals.SILVER,
                country="United States",
                face_value=50,
                denomination="Cents",
            )
        ),
        "kennedy_half_1": Node(
            CoinData(
                nickname="90% Kennedy Half",
                years=[1964],
                weight=12.5,
                fineness=0.900,
                metal=Metals.SILVER,
                country="United States",
                face_value=50,
                denomination="Cents",
            )
        ),
        "kennedy_half_2": Node(
            CoinData(
                nickname="40% Kennedy Half",
                years=[x for x in list(range(1965, 1971))],
                weight=11.5,
                fineness=0.400,
                metal=Metals.SILVER,
                country="United States",
                face_value=50,
                denomination="Cents",
            )
        ),
        "morgan_dollar": Node(
            CoinData(
                nickname="Morgan Dollar",
                years=[x for x in (list(range(1878, 1905)) + [1921])],
                weight=26.73,
                fineness=0.900,
                metal=Metals.SILVER,
                country="United States",
                face_value=1,
                denomination="Dollar",
            )
        ),
        "peace_dollar": Node(
            CoinData(
                nickname="Peace Dollar",
                years=[x for x in (list(range(1921, 1929)) + [1934, 1935])],
                weight=26.73,
                fineness=0.900,
                metal=Metals.SILVER,
                country="United States",
                face_value=1,
                denomination="Dollar",
            )
        ),
    }

    # Used to build the tree from just a coin object
    coins_reverse_build = {
        "canada_dollar_5": ("canada_dollar_5", "canada_dollar", "canada"),
        "centimes_20": ("centimes_20", "centimes", "france"),
        "centimes_50_1": ("centimes_50", "centimes", "france"),
        "centimes_50_2": ("centimes_50", "centimes", "france"),
        "franc_1_1": ("franc_1", "franc", "france"),
        "franc_1_2": ("franc_1", "franc", "france"),
        "franc_2": ("franc_2", "franc", "france"),
        "franc_5_1": ("franc_5", "franc", "france"),
        "franc_5_2": ("franc_5", "franc", "france"),
        "franc_5_3": ("franc_5", "franc", "france"),
        "franc_10_1": ("franc_10", "franc", "france"),
        "franc_10_2": ("franc_10", "franc", "france"),
        "franc_20_1": ("franc_20", "franc", "france"),
        "franc_20_2": ("franc_20", "franc", "france"),
        "franc_50": ("franc_50", "franc", "france"),
        "franc_100_1": ("franc_100", "franc", "france"),
        "franc_100_2": ("franc_100", "franc", "france"),
        "franc_100_3": ("franc_100", "franc", "france"),
        "mark_10": ("mark_10", "mark", "germany"),
        "centesimi_20": ("centesimi_20", "centesimi", "italy"),
        "peso_1": ("peso_1", "peso", "mexico"),
        "barber_dime": ("dime", "cents", "united_states"),
        "mercury_dime": ("dime", "cents", "united_states"),
        "roosevelt_dime": ("dime", "cents", "united_states"),
        "barber_quarter": ("quarter", "cents", "united_states"),
        "standing_liberty_quarter": ("quarter", "cents", "united_states"),
        "washington_quarter": ("quarter", "cents", "united_states"),
        "walking_liberty_half": ("half", "cents", "united_states"),
        "benjamin_half": ("half", "cents", "united_states"),
        "kennedy_half_1": ("half", "cents", "united_states"),
        "kennedy_half_2": ("half", "cents", "united_states"),
        "morgan_dollar": ("dollar", "dollar", "united_states"),
        "peace_dollar": ("dollar", "dollar", "united_states"),
    }

    # Indicates which coins are made of silver
    silver_coins = [
        # Canada
        "canada_dollar_5",
        # France
        "centimes_20",
        "centimes_50_1",
        "centimes_50_2",
        "franc_1_1",
        "franc_1_2",
        "franc_2",
        "franc_5_1",
        "franc_5_2",
        "franc_10_1",
        "franc_20_2",
        "franc_100_1",
        # Italy
        "centesimi_20",
        # Mexico
        "peso_1",
        # United States
        "barber_dime",
        "mercury_dime",
        "roosevelt_dime",
        "barber_quarter",
        "standing_liberty_quarter",
        "washington_quarter",
        "walking_liberty_half",
        "benjamin_half",
        "kennedy_half_1",
        "kennedy_half_2",
        "morgan_dollar",
        "peace_dollar",
    ]

    # Indicates which coins are made of gold
    gold_coins = [
        # France
        "franc_5_3",
        "franc_10_2",
        "franc_20_1",
        "franc_50",
        "franc_100_2",
        "franc_100_3",
        # Germany
        "mark_10",
    ]

    values = {
        # Canada
        "canada_dollar_5": NamedList("5", ["canada_dollar_5"]),
        # France
        "centimes_20": NamedList("20", ["centimes_20"]),
        "centimes_50": NamedList("50", ["centimes_50_1", "centimes_50_2"]),
        "franc_1": NamedList("1", ["franc_1_1", "franc_1_2"]),
        "franc_2": NamedList("2", ["franc_2"]),
        "franc_5": NamedList("5", ["franc_5_1", "franc_5_2", "franc_5_3"]),
        "franc_10": NamedList("10", ["franc_10_1", "franc_10_2"]),
        "franc_20": NamedList("20", ["franc_20_1", "franc_20_2"]),
        "franc_50": NamedList("50", ["franc_50"]),
        "franc_100": NamedList("100", ["franc_100_1", "franc_100_2", "franc_100_3"]),
        # Germany
        "mark_10": NamedList("10", ["mark_10"]),
        # Italy
        "centesimi_20": NamedList("20", ["centesimi_20"]),
        # Mexico
        "peso_1": NamedList("1", ["peso_1"]),
        # United States
        "dime": NamedList("Dimes", ["barber_dime", "mercury_dime", "roosevelt_dime"]),
        "quarter": NamedList(
            "Quarters",
            ["barber_quarter", "standing_liberty_quarter", "washington_quarter"],
        ),
        "half": NamedList(
            "Halves",
            [
                "walking_liberty_half",
                "benjamin_half",
                "kennedy_half_1",
                "kennedy_half_2",
            ],
        ),
        "dollar": NamedList("Dollars", ["morgan_dollar", "peace_dollar"]),
    }

    denominations = {
        # Canada
        "canada_dollar": NamedList("Dollars", ["canada_dollar_5"]),
        # France
        "centimes": NamedList("Centimes", ["centimes_20", "centimes_50"]),
        "franc": NamedList(
            "Franc",
            [
                "franc_1",
                "franc_2",
                "franc_5",
                "franc_10",
                "franc_20",
                "franc_50",
                "franc_100",
            ],
        ),
        # Germany
        "mark": NamedList("Mark", ["mark_10"]),
        # Italy
        "centesimi": NamedList("Centesimi", ["centesimi_20"]),
        # Mexico
        "peso": NamedList("Peso", ["peso_1"]),
        # United States
        "cents": NamedList("Cents", ["dime", "quarter", "half"]),
        "dollar": NamedList("Dollars", ["dollar"]),
    }

    countries = {
        "canada": NamedList("Canada", ["canada_dollar"]),
        "france": NamedList("France", ["centimes", "franc"]),
        "germany": NamedList("Germany", ["mark"]),
        "italy": NamedList("Italy", ["centesimi"]),
        "mexico": NamedList("Mexico", ["peso"]),
        "united_states": NamedList("United States", ["cents", "dollar"]),
    }

    # Enables or disables printing of the coins value
    def togglePrice(show_price=True):
        for coin_id in list(Coins.coins.keys()):
            coin = Coins.coins[coin_id]
            if isinstance(coin, Node):
                coin = coin.data
            coin.togglePrice(show_price)

    # Calculates the value of all defined coin objects, using the provided precious metal values
    def price(silver_price, gold_price):
        for coin_id in list(Coins.coins.keys()):
            coin = Coins.coins[coin_id]
            if isinstance(coin, Node):
                coin = coin.data
            if coin.metal == Metals.SILVER:
                coin.value = coin.precious_metal_weight.as_troy_ounces() * silver_price
            if coin.metal == Metals.GOLD:
                coin.value = coin.precious_metal_weight.as_troy_ounces() * gold_price

    # Removes associated purchases from all defined coins
    def removePurchases():
        for coin_id in list(Coins.coins.keys()):
            coin = Coins.coins[coin_id]
            if isinstance(coin, Node):
                coin.nodes = []

    # Links all purchases in purchases.py to their associated coins
    def linkPurchases(keep_old_purchases=False):
        if not keep_old_purchases:
            Coins.removePurchases()
        for purchase in purchases:
            try:
                coin = Coins.coins[purchase]
                if isinstance(coin, Node):
                    coin.nodes += purchases[purchase]
            except KeyError:
                print(f"{purchase} is not a valid key")


    # Creates a tree from any number/combination of key values.
    def buildTree(coin_ids, debug=False):
        results = Tree(name="Results", nodes=[])
        needed_countries = {}
        needed_denominations = {}
        needed_values = {}
        for coin_id in coin_ids:
            try:
                information = Coins.coins_reverse_build[coin_id]
                try:
                    value_found = needed_values[information[0]]
                    needed_values[information[0]] = value_found + [coin_id]
                except (
                    KeyError
                ):  # coin_id's value is not a valid key in needed_values yet
                    needed_values[information[0]] = [coin_id]

                try:
                    denominations_found = needed_denominations[information[1]]
                    if not [x for x in denominations_found if x == information[0]]:
                        needed_denominations[information[1]] = denominations_found + [
                            information[0]
                        ]
                except (
                    KeyError
                ):  # coin_id's value is not a valid key in needed_values yet
                    needed_denominations[information[1]] = [information[0]]
                try:
                    countries_found = needed_countries[information[2]]
                    if not [x for x in countries_found if x == information[1]]:
                        needed_countries[information[2]] = countries_found + [
                            information[1]
                        ]
                except KeyError:
                    needed_countries[information[2]] = [information[1]]
            except KeyError:  # coin_id is not a valid key in coins_reverse_build
                try:
                    information = Coins.values[coin_id]
                    coin_ids += list(information)
                except KeyError:
                    try:
                        information = Coins.denominations[coin_id]
                        coin_ids += list(information)
                    except KeyError:
                        try:
                            information = Coins.countries[coin_id]
                            coin_ids += list(information)
                        except KeyError:
                            pass

            if debug:
                print(f"---{coin_id}---")
                print(f"Values: {needed_values}")
                print(f"Denominations: {needed_denominations}")
                print(f"Countries: {needed_countries}")
                print()

        current_countries = []
        for country in needed_countries:
            current_denominations = []
            for denomination in Coins.countries[country]:
                if denomination in needed_denominations:
                    current_values = []
                    for value in Coins.denominations[denomination]:
                        if value in needed_values:
                            current_coins = []
                            for coin in Coins.values[value]:
                                if coin in coin_ids:
                                    temp = Coins.coins[coin]
                                    if isinstance(temp, Node):
                                        current_coins.append(temp)
                                    else:
                                        current_coins.append(Node(data=temp))
                            # Sorts the coins by first year available
                            current_coins = sorted(
                                current_coins, key=lambda x: x.data.years[0]
                            )
                            if isinstance(Coins.values[value], NamedList):
                                current_values.append(
                                    Tree(
                                        name=str(Coins.values[value]),
                                        nodes=current_coins,
                                    )
                                )
                            else:
                                current_values.append(
                                    Tree(name=value, nodes=current_coins)
                                )
                    if isinstance(Coins.denominations[denomination], NamedList):
                        current_denominations.append(
                            Tree(
                                name=str(Coins.denominations[denomination]),
                                nodes=current_values,
                            )
                        )
                    else:
                        current_denominations.append(
                            Tree(name=denomination, nodes=current_values)
                        )

            if isinstance(Coins.countries[country], NamedList):
                current_countries.append(
                    Tree(
                        name=str(Coins.countries[country]), nodes=current_denominations
                    )
                )
            else:
                current_countries.append(
                    Tree(name=country, nodes=current_denominations)
                )
        results = Tree(name="Results", nodes=current_countries)
        return results

    def search(
        country=None, denomination=None, face_value=None, year=None, debug=False
    ):
        found_denominations = list(Coins.denominations.keys())
        if country:
            try:
                found_denominations = Coins.countries[country.lower()]
            except KeyError:
                return None

        if debug:
            print("Denominations found:")
            for item in found_denominations:
                print(f"  {item}")

        found_values = []
        if denomination:
            matches = [
                x
                for x in found_denominations
                if Coins.denominations[x].name.lower() == denomination.lower()
            ]
            if matches:
                try:
                    for match in matches:
                        found_values += Coins.denominations[match]
                except KeyError:
                    return None
            else:
                return None
        else:
            for denom in found_denominations:
                found_values += Coins.denominations[denom]

        if debug:
            print("Values found:")
            for item in found_values:
                print(f"  {item}")

        found_coins = []
        if face_value:
            matches = [
                x
                for x in found_values
                if (
                    Coins.values[x].name == face_value
                    or str(Coins.values[x].name).lower() == str(face_value).lower()
                )
            ]
            if matches:
                try:
                    for match in matches:
                        found_coins = Coins.values[match]
                except KeyError:
                    return None
            else:
                return None
        else:
            for value in found_values:
                found_coins += Coins.values[value]

        if debug:
            print("Coins found:")
            for item in found_coins:
                print(f"  {item}")

        results = []
        if year:
            matches = [
                x
                for x in found_coins
                if year
                in (
                    Coins.coins[x].years
                    if isinstance(Coins.coins[x], CoinData)
                    else Coins.coins[x].data.years
                )
            ]
            if matches:
                try:
                    for match in matches:
                        results += [match]
                except KeyError:
                    return None
            else:
                return None
        else:
            results = found_coins

        if debug:
            print("Results:")
            for item in results:
                print(f"  {item}")

        return Coins.buildTree(results, debug)
