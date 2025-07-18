from datetime import datetime
import collection
from coinData import CoinData,Purchase
from metals import Metals
import weights
from country import CountryName
from tree.node import Node
from tree.tree import Tree
import coinInfo


silver_spot_price = 36.00
gold_spot_price = 3350.00


def applyBasicInformation(country_tree,country_name,silver_coins,gold_coins):
    for denomination in country_tree.nodes:
        for value in denomination.nodes:
            for coin in value.nodes:
                coin.face_value = value.name
                coin.denomination = denomination.name
                coin.country = country_name
                if coin in silver_coins:
                    coin.metal = Metals.SILVER
                    silver_coins.remove(coin)
                if coin in gold_coins:
                    coin.metal = Metals.GOLD
                    gold_coins.remove(coin)


def coinsFrance(show_personal_collection=True):
    """Builds a CoinCollection object about the precious metal content of French coins"""

    return coinInfo.buildCountry("france")

    purchase_0 = Purchase(price=8.00,mint_date=1931,purchase_date = datetime(2025,7,4))
    centimes_20 = Node(data=CoinData(
        years=list(range(1848, 1921)),
        weight=1,
        fineness=0.9,
    ),nodes=[])

    centimes_50_1 = CoinData(
        years=list(range(1848, 1867)),
        weight=2.5,
        fineness=0.9,
    )
    centimes_50_2 = CoinData(
        years=list(range(1866, 1921)),
        weight=2.5,
        fineness=0.835,
    )
    

    centimes_20_tree = Tree(name=20,nodes=[centimes_20])
    centimes_50 = [centimes_50_1, centimes_50_2]
    centimes_50_tree = Tree(name=50,nodes=centimes_50)

    franc_1_1 = CoinData(
        years=list(range(1848, 1867)), weight=5, fineness=0.9
    )
    franc_1_2 = CoinData(
        years=list(range(1866, 1921)), weight=5, fineness=0.835
    )
    franc_1 = [franc_1_1, franc_1_2]
    franc_1_tree = Tree(name=1,nodes=franc_1)

    franc_2 = CoinData(
        years=list(range(1848, 1921)), weight=10, fineness=0.9
    )

    franc_2_tree = Tree(name=2,nodes=[franc_2])
    franc_5_1 = CoinData(
        years=list(range(1848, 1921)), weight=25, fineness=0.9
    )
    franc_5_2 = CoinData(
        years=list(range(1960, 1970)), weight=12, fineness=0.835
    )
    franc_5_3 = CoinData(
        years=list(range(1848, 1915)),
        weight=1.6129,
        fineness=0.9,
    )
    franc_5_silver = [franc_5_1, franc_5_2]
    franc_5_gold = [franc_5_3]

    franc_5_tree = Tree(name=5,nodes=(franc_5_silver + franc_5_gold))

    franc_10_1 = CoinData(
        years=[x for x in list(range(1929, 1940)) if x not in [1935, 1936]],
        weight=10,
        fineness=0.68,
    )
    franc_10_2 = CoinData(
        years=list(range(1848, 1915)),
        weight=3.2258,
        fineness=0.90,
    )
    franc_10_silver = [franc_10_1]
    franc_10_gold = [franc_10_2]

    franc_10_tree = Tree(name=10,nodes=(franc_10_silver+franc_10_gold))

    franc_20_1 = CoinData(
        years=[x for x in range(1906, 1915)],
        weight=6.4516,
        fineness=0.9,
    )
    franc_20_2 = CoinData(
        years=list(range(1929, 1940)),
        weight=20,
        fineness=0.68,
    )
    franc_20_silver = [franc_20_2]
    franc_20_gold = [franc_20_1]

    franc_20_tree = Tree(name=20,nodes=(franc_20_silver+franc_20_gold))

    franc_50 = CoinData(
        years=list(range(1848, 1915)),
        weight=16.129,
        fineness=0.9,
    )

    franc_50_tree = Tree(name=50,nodes=[franc_50])

    franc_100_1 = CoinData(
        years=[x for x in range(1982, 2001)],
        weight=15,
        fineness=0.9,
    )
    franc_100_2 = CoinData(
        years=list(range(1848, 1915)),
        weight=32.2581,
        fineness=0.9,
    )
    franc_100_3 = CoinData(
        years=list(range(1929, 1937)),
        weight=6.55,
        fineness=0.9,
    )
    franc_100_silver = [franc_100_1]
    franc_100_gold = [franc_100_2, franc_100_3]

    franc_100_tree = Tree(name=100,nodes=(franc_100_silver+franc_100_gold))

    # Assign metal type and country to all coins
    silver_coins = (
        [centimes_20, franc_2]
        + centimes_50
        + franc_1
        + franc_5_silver
        + franc_10_silver
        + franc_20_silver
        + franc_100_silver
    )
    gold_coins = (
        [franc_50] + franc_5_gold + franc_10_gold + franc_20_gold + franc_100_gold
    )
    """
    for coin in silver_coins:
        coin.metal = Metals.SILVER
        coin.country = "France"
    for coin in gold_coins:
        coin.metal = Metals.GOLD
        coin.country = "France"
    # french_coins = silver_coins + gold_coins
    """

    """

    # Centimes
    france_20_centimes = collection.Value(coins=centimes_20, face_value=20)
    france_50_centimes = collection.Value(coins=centimes_50, face_value=50)

    centime = collection.Denomination(
        values=[france_20_centimes, france_50_centimes], name="Centime"
    )

    # Francs
    france_1_franc = collection.Value(coins=franc_1, face_value=1)
    france_2_franc = collection.Value(coins=franc_2, face_value=2)
    france_5_franc = collection.Value(coins=franc_5_silver + franc_5_gold, face_value=5)
    france_10_franc = collection.Value(
        coins=franc_10_silver + franc_10_gold, face_value=10
    )
    france_20_franc = collection.Value(
        coins=franc_20_silver + franc_20_gold, face_value=20
    )
    france_50_franc = collection.Value(coins=franc_50, face_value=50)
    france_100_franc = collection.Value(
        coins=franc_100_silver + franc_100_gold, face_value=100
    )

    franc = collection.Denomination(
        values=[
            france_1_franc,
            france_2_franc,
            france_5_franc,
            france_10_franc,
            france_20_franc,
            france_50_franc,
            france_100_franc,
        ],
        name="Franc",
    )
    """

    france_centime = [centimes_20_tree,centimes_50_tree]
    france_centime_tree = Tree(name="Centime",nodes=france_centime)
    france_franc = [franc_1_tree,franc_2_tree,franc_5_tree,franc_10_tree,franc_20_tree,franc_50_tree,franc_100_tree]
    france_franc_tree = Tree(name="Franc",nodes=france_franc)
    france = Tree(name="France",nodes=[france_centime_tree,france_franc_tree])

    applyBasicInformation(france,"France",silver_coins,gold_coins)
    return france


    """
    france = collection.Country(denominations=[centime, franc], name="France")

    for denomination in france.denominations:
        for value in denomination.values:
            for coin in value.coins:
                coin.face_value = value.face_value
                coin.denomination = denomination.name
                coin.country = "France"
                if coin in silver_coins:
                    coin.metal = Metals.SILVER
                    silver_coins.remove(coin)
                if coin in gold_coins:
                    coin.metal = Metals.GOLD
                    gold_coins.remove(coin)

    """
    if show_personal_collection:
        # Personal collection below
        franc_10_1.addCollection(Purchase(price=8.00,mint_date=1931,purchase_date = datetime(2025,7,4)))
        franc_100_1.addCollection(Purchase(price=11.95,purchase_date=datetime(2025,7,3),mint_date=1982))
        # Personal collection above

    return france






countries = [
        (CountryName("France", ["French"]),coinsFrance),
        ]
