"""
   Author: Josh Gillum              .
   Date: 24 July 2025              ":"         __ __
                                  __|___       \ V /
                                .'      '.      | |
                                |  O       \____/  |
^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

    This script is designed to be used to make adding or updating CoinData
    objects within the Coins class. See CoinInfo.py for information on the
    class. The script will print out the entire coins_reverse_build dictionary,
    as well as the silver_coins and gold_coins lists. They will simply have to
    be copied and pasted into Coins class in coins/coins.py. Make sure to delete
    the old versions of these variables as well.

    In order to work, the CoinData objects must contain the metal type (either
    Metals.SILVER or Metals.GOLD). The entries within Coins.values,
    Coins.denominations, and Coins.countries must also be correct. There needs
    to be a way for the script to go from a country all the way down to the coin
    object.

^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
"""

from coins.coins import Coins
from metals import Metals
from tree.node import Node

tab = "    "


def print_reverse_build():
    coins_reverse_build = [f"{tab}coins_reverse_build =" + " {"]
    values_reverse_build = [f"{tab}values_reverse_build =" + " {"]
    denominations_reverse_build = [f"{tab}denominations_reverse_build =" + " {"]
    for country in Coins.countries:
        for denomination in Coins.countries[country]:
            denominations_reverse_build += [
                f'{tab}{tab}"{denomination}": ("{country}"),'
            ]
            for value in Coins.denominations[denomination]:
                values_reverse_build += [
                    f'{tab}{tab}"{value}": ("{denomination}","{country}"),'
                ]
                for coin in Coins.values[value]:
                    coins_reverse_build += [
                        f'{tab}{tab}"{coin}": ("{value}","{denomination}","{country}"),'
                    ]
    coins_reverse_build += [f"{tab}" + "}"]
    values_reverse_build += [f"{tab}" + "}"]
    denominations_reverse_build += [f"{tab}" + "}"]

    #    for item in [coins_reverse_build,values_reverse_build,denominations_reverse_build]:
    for item in [coins_reverse_build]:
        for line in item:
            print(line)
        print()


def print_metals():
    silver_coins = [f"{tab}silver_coins = ["]
    gold_coins = [f"{tab}gold_coins = ["]
    platinum_coins = [f"{tab}platinum_coins = ["]
    palladium_coins = [f"{tab}palladium_coins = ["]
    for country in Coins.countries:
        for denomination in Coins.countries[country]:
            for value in Coins.denominations[denomination]:
                for coin in Coins.values[value]:
                    test = Coins.coins[coin]
                    if isinstance(test, Node):
                        test = test.data
                    if test.metal == Metals.SILVER:
                        silver_coins.append(f'{tab}{tab}"{coin}",')
                    if test.metal == Metals.GOLD:
                        gold_coins.append(f'{tab}{tab}"{coin}",')
                    if test.metal == Metals.PLATINUM:
                        platinum_coins.append(f'{tab}{tab}"{coin}",')
                    if test.metal == Metals.PALLADIUM:
                        palladium_coins.append(f'{tab}{tab}"{coin}",')
    silver_coins.append(f"{tab}]")
    gold_coins.append(f"{tab}]")
    platinum_coins.append(f"{tab}]")
    palladium_coins.append(f"{tab}]")
    print(f"{tab}# Indicates which coins are made of silver.")
    for line in silver_coins:
        print(line)
    print()
    print(f"{tab}# Indicates which coins are made of gold.")
    for line in gold_coins:
        print(line)
    print()
    print(f"{tab}# Indicates which coins are made of platinum.")
    for line in platinum_coins:
        print(line)
    print()
    print(f"{tab}# Indicates which coins are made of palladium.")
    for line in palladium_coins:
        print(line)
    print()


if __name__ == "__main__":
    print_reverse_build()
    print_metals()
