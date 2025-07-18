from coinData import CoinData
from tree.tree import Tree
from tree.node import Node
from metals import Metals


coins = {
    "centimes_20": CoinData(
        years=list(range(1848, 1921)),
        weight=1,
        fineness=0.9,
    ),
    "centimes_50_1": CoinData(
        years=list(range(1848, 1867)),
        weight=2.5,
        fineness=0.9,
    ),
    "centimes_50_2": CoinData(
        years=list(range(1866, 1921)),
        weight=2.5,
        fineness=0.835,
    ),
    "franc_1_1": CoinData(years=list(range(1848, 1867)), weight=5, fineness=0.9),
    "franc_1_2": CoinData(years=list(range(1866, 1921)), weight=5, fineness=0.835),
    "franc_2": CoinData(years=list(range(1848, 1921)), weight=10, fineness=0.9),
    "franc_5_1": CoinData(years=list(range(1848, 1921)), weight=25, fineness=0.9),
    "franc_5_2": CoinData(years=list(range(1960, 1970)), weight=12, fineness=0.835),
    "franc_5_3": CoinData(
        years=list(range(1848, 1915)),
        weight=1.6129,
        fineness=0.9,
    ),
    "franc_10_1": CoinData(
        years=[x for x in list(range(1929, 1940)) if x not in [1935, 1936]],
        weight=10,
        fineness=0.68,
    ),
    "franc_10_2": CoinData(
        years=list(range(1848, 1915)),
        weight=3.2258,
        fineness=0.90,
    ),
    "franc_20_1": CoinData(
        years=[x for x in range(1906, 1915)],
        weight=6.4516,
        fineness=0.9,
    ),
    "franc_20_2": CoinData(
        years=list(range(1929, 1940)),
        weight=20,
        fineness=0.68,
    ),
    "franc_50": CoinData(
        years=list(range(1848, 1915)),
        weight=16.129,
fineness=0.9,
    ),
    "franc_100_1": CoinData(
        years=[x for x in range(1982, 2001)],
        weight=15,
        fineness=0.9,
    ),
    "franc_100_2": CoinData(
        years=list(range(1848, 1915)),
        weight=32.2581,
        fineness=0.9,
    ),
    "franc_100_3": CoinData(
        years=list(range(1929, 1937)),
        weight=6.55,
        fineness=0.9,
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
        "centimes_20":["centimes_20"],
        "centimes_50":["centimes_50_1","centimes_50_2"],
        "franc_1":["franc_1_1","franc_1_2"],
        "franc_2":["franc_2"],
        "franc_5":["franc_5_1","franc_5_2","franc_5_3"],
        "franc_10":["franc_10_1","franc_10_2"],
        "franc_20":["franc_20_1","franc_20_2"],
        "franc_50":["franc_50"],
        "franc_100":["franc_100_1","franc_100_2","franc_100_3"],
        }

denominations = {
        "centimes":["centimes_20","centimes_50"],
        "franc":["franc_1","franc_2","franc_5","franc_10","franc_20","franc_50","franc_100"]
}

countries = {
        "france":["centimes","franc"]
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
            current_values.append(Tree(name=value,nodes=current_coins))
        current_denominations.append(Tree(name=denomination,nodes=current_values))
    return Tree(name=country,nodes=current_denominations)



















