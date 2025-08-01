"""
   Author: Josh Gillum              .
   Date: 1 August 2025             ":"         __ __
                                  __|___       \ V /
                                .'      '.      | |
                                |  O       \____/  |
^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

    This script prints out a report of the personal collection of coins. It 
    utilizes Coins.owned in coins/coins.py. See purchases.py for information on
    how to add and update purchases. This script is still a work in progress.
    
    Use the script by calling it as main from the command line

-------------------------------------------------------------------------------
                            DEFUNCT - NON OPERATIONAL
-------------------------------------------------------------------------------

^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
"""

"""
from coins.coins import Coins
import data
from coinData import Purchase, PurchaseStats as Stats
from metals import Metals
import config

tab = "    "
currency_symbol="$"
"""



if __name__ == "__main__":
    print("""
-------------------------------------------------------------------------------
                            DEFUNCT - NON OPERATIONAL
-------------------------------------------------------------------------------
terminating...
""")
    exit(1)
    """
    # Prints out the tree of all owned coins
    Coins.price(data.silver_spot_price,data.gold_spot_price,data.platinum_spot_price,data.palladium_spot_price)
    Coins.linkPurchases()
    results = Coins.buildTree(Coins.countries.keys(),show_only_owned=True)
    results.cascading_set_fancy(config.tree_fancy_characters)
    for line in results.print():
        print(line)

    # Calculates statistics
    total = Stats()
    silver = Stats()
    gold = Stats()
    platinum = Stats()
    palladium = Stats()
    other = Stats()
    collection = Coins.owned
    for coin in collection:
        coin = Coins.coins[coin]

        if coin is not None:
            value = coin.data.value*coin.data.retention
            for node in coin.nodes:
                if isinstance(node,Purchase):
                    sum_delta = (node.price * node.quantity)
                    count_delta = node.quantity
                    delta_delta = ((value - node.price)*node.quantity)

                    total.add(sum_delta,count_delta,delta_delta)
                    metal = None
                    match coin.data.metal:
                        case Metals.SILVER:
                            metal = silver
                        case Metals.GOLD:
                            metal = gold
                        case Metals.PLATINUM:
                            metal = platinum
                        case Metals.PALLADIUM:
                            metal = palladium
                        case _:
                            metal = other
                    if metal is not None:
                        metal.add(sum_delta,count_delta,delta_delta)

    if total.count > 0:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("|                                   Totals:                                    |")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Silver:\n  ",end="")
        print(Coins.print_statistics(stats=silver))
        print("Gold:\n  ",end="")
        print(Coins.print_statistics(stats=gold))
        print("Platinum:\n  ",end="")
        print(Coins.print_statistics(stats=platinum))
        print("Palladium:\n  ",end="")
        print(Coins.print_statistics(stats=palladium))
        print("Total:\n  ",end="")
        print(Coins.print_statistics(stats=total))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    """ 
