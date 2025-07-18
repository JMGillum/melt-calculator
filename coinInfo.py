from coinData import CoinData
from tree.tree import Tree
from tree.node import Node
from metals import Metals

class NamedList:
    def __init__(self,name,items):
        self.name = name
        self.items = items

    def __str__(self):
        if self.name:
            return self.name
        else:
            return ""

    def __getitem__(self,key):
        return self.items[key]

    def __setitem__(self,key,newvalue):
        self.items[key] = newvalue

coins = {
    "centimes_20": CoinData(
        years=list(range(1848, 1921)),
        weight=1,
        fineness=0.9,
        metal=Metals.SILVER,
        country="France"
    ),
    "centimes_50_1": CoinData(
        years=list(range(1848, 1867)),
        weight=2.5,
        fineness=0.9,
        metal=Metals.SILVER,
        country="France"
    ),
    "centimes_50_2": CoinData(
        years=list(range(1866, 1921)),
        weight=2.5,
        fineness=0.835,
        metal=Metals.SILVER,
        country="France"
    ),
    "franc_1_1": CoinData(
        years=list(range(1848, 1867)),
          weight=5,
          fineness=0.9,
        metal=Metals.SILVER,
        country="France"
        ),
    "franc_1_2": CoinData(
        years=list(range(1866, 1921)), 
        weight=5, 
        fineness=0.835,
        metal=Metals.SILVER,
        country="France"
        ),
    "franc_2": CoinData(
        years=list(range(1848, 1921)), 
        weight=10, 
        fineness=0.9,
        metal=Metals.SILVER,
        country="France"
        ),
    "franc_5_1": CoinData(
        years=list(range(1848, 1921)), 
        weight=25, 
        fineness=0.9,
        metal=Metals.SILVER,
        country="France"
        ),
    "franc_5_2": CoinData(
            years=list(range(1960, 1970)), 
            weight=12, 
            fineness=0.835,
        metal=Metals.SILVER,
        country="France"
            ),
    "franc_5_3": CoinData(
        years=list(range(1848, 1915)),
        weight=1.6129,
        fineness=0.9,
        metal=Metals.GOLD,
        country="France"
    ),
    "franc_10_1": CoinData(
        years=[x for x in list(range(1929, 1940)) if x not in [1935, 1936]],
        weight=10,
        fineness=0.68,
        metal=Metals.SILVER,
        country="France"
    ),
    "franc_10_2": CoinData(
        years=list(range(1848, 1915)),
        weight=3.2258,
        fineness=0.90,
        metal=Metals.GOLD,
        country="France"
    ),
    "franc_20_1": CoinData(
        years=[x for x in range(1906, 1915)],
        weight=6.4516,
        fineness=0.9,
        metal=Metals.GOLD,
        country="France"
    ),
    "franc_20_2": CoinData(
        years=list(range(1929, 1940)),
        weight=20,
        fineness=0.68,
        metal=Metals.SILVER,
        country="France"
    ),
    "franc_50": CoinData(
        years=list(range(1848, 1915)),
        weight=16.129,
fineness=0.9,
metal=Metals.GOLD,
        country="France"
    ),
    "franc_100_1": CoinData(
        years=[x for x in range(1982, 2001)],
        weight=15,
        fineness=0.9,
        metal=Metals.SILVER,
        country="France"
    ),
    "franc_100_2": CoinData(
        years=list(range(1848, 1915)),
        weight=32.2581,
        fineness=0.9,
        metal=Metals.GOLD,
        country="France"
    ),
    "franc_100_3": CoinData(
        years=list(range(1929, 1937)),
        weight=6.55,
        fineness=0.9,
        metal=Metals.GOLD,
        country="France"
    ),
}



silver_coins = [
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
        ]

gold_coins = [
        "franc_5_3",
        "franc_10_2",
        "franc_20_1",
        "franc_50",
        "franc_100_2",
        "franc_100_3",
        ]

values = {
        "centimes_20":NamedList("20",["centimes_20"]),
        "centimes_50":NamedList("50",["centimes_50_1","centimes_50_2"]),
        "franc_1":NamedList("1",["franc_1_1","franc_1_2"]),
        "franc_2":NamedList("2",["franc_2"]),
        "franc_5":NamedList("5",["franc_5_1","franc_5_2","franc_5_3"]),
        "franc_10":NamedList("10",["franc_10_1","franc_10_2"]),
        "franc_20":NamedList("20",["franc_20_1","franc_20_2"]),
        "franc_50":NamedList("50",["franc_50"]),
        "franc_100":NamedList("100",["franc_100_1","franc_100_2","franc_100_3"]),
        }

denominations = {
        "centimes":NamedList("Centimes",["centimes_20","centimes_50"]),
        "franc":NamedList("Franc",["franc_1","franc_2","franc_5","franc_10","franc_20","franc_50","franc_100"]),
}

countries = {
        "france":NamedList("France",["centimes","franc"]),
        }

def applyMetals(country):
    for denomination in countries[country]:
        for value in denominations[denomination]:
            for coin in values[value]:
                if coin in silver_coins:
                    coins[coin].metal = Metals.SILVER
                elif coin in gold_coins:
                    coins[coin].metal = Metals.GOLD

def applyCountry(country):
    for denomination in countries[country]:
        for value in denominations[denomination]:
            for coin in values[value]:
                coins[coin].country = country.title()

def buildCountry(country,first_time=True):
    """country is name, first_time will apply metals and country"""
    current_denominations = []
    for denomination in countries[country]:
        current_values = []
        for value in denominations[denomination]:
            current_coins = []
            for coin in values[value]:
                current_coins.append(Node(data=coins[coin]))
            # Sorts the coins by first year available
            current_coins = sorted(current_coins, key = lambda x : x.data.years[0])
            if isinstance(values[value],NamedList):
                current_values.append(Tree(name=str(values[value]),nodes=current_coins))
            else:
                current_values.append(Tree(name=value,nodes=current_coins))
        if isinstance(denominations[denomination],NamedList):
            current_denominations.append(Tree(name=str(denominations[denomination]),nodes=current_values))
        else:
            current_denominations.append(Tree(name=denomination,nodes=current_values))
    return Tree(name=str(countries[country]),nodes=current_denominations)



















