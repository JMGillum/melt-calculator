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

from metals import Metals
from tree.node import Node


import coins.canada as canada
import coins.france as france
import coins.germany as germany
import coins.great_britain as great_britain
import coins.italy as italy
import coins.mexico as mexico
import coins.south_africa as south_africa
import coins.united_states as united_states
import coins.switzerland as switzerland

tab = "    "


def print_reverse_build(country,country_name):
    coins_reverse_build = ["coins_reverse_build =" + " {"]
    values_reverse_build = ["values_reverse_build =" + " {"]
    denominations_reverse_build = ["denominations_reverse_build =" + " {"]
    for denomination in country.denominations:
        denominations_reverse_build += [
            f'{tab}"{denomination}": ("{country_name}"),'
        ]
        for value in country.denominations[denomination]:
            values_reverse_build += [
                f'{tab}"{value}": ("{denomination}","{country_name}"),'
            ]
            for coin in country.values[value]:
                coins_reverse_build += [
                    f'{tab}"{coin}": ("{value}","{denomination}","{country_name}"),'
                ]
    coins_reverse_build += ["}"]
    values_reverse_build += ["}"]
    denominations_reverse_build += ["}"]

    #    for item in [coins_reverse_build,values_reverse_build,denominations_reverse_build]:
    for item in [coins_reverse_build]:
        for line in item:
            print(line)
        print()


def print_metals(country):
    silver_coins = ["silver_coins = ["]
    gold_coins = ["gold_coins = ["]
    platinum_coins = ["platinum_coins = ["]
    palladium_coins = ["palladium_coins = ["]
    for denomination in country.denominations:
        for value in country.denominations[denomination]:
            for coin in country.values[value]:
                test = country.coins[coin]
                if isinstance(test, Node):
                    test = test.data
                if test.metal == Metals.SILVER:
                    silver_coins.append(f'{tab}"{coin}",')
                if test.metal == Metals.GOLD:
                    gold_coins.append(f'{tab}"{coin}",')
                if test.metal == Metals.PLATINUM:
                    platinum_coins.append(f'{tab}"{coin}",')
                if test.metal == Metals.PALLADIUM:
                    palladium_coins.append(f'{tab}"{coin}",')
    silver_coins.append("]")
    gold_coins.append("]")
    platinum_coins.append("]")
    palladium_coins.append("]")
    print("# Indicates which coins are made of silver.")
    for line in silver_coins:
        print(line)
    print()
    print("# Indicates which coins are made of gold.")
    for line in gold_coins:
        print(line)
    print()
    print("# Indicates which coins are made of platinum.")
    for line in platinum_coins:
        print(line)
    print()
    print("# Indicates which coins are made of palladium.")
    for line in palladium_coins:
        print(line)
    print()


if __name__ == "__main__":
    print_reverse_build(switzerland,"switzerland")
    print_metals(switzerland)
