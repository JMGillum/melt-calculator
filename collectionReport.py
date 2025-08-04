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


^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
"""

from db_interface import DB_Interface
from queries import Queries
from coins import Coins
import config
from metals import Metals
from coinData import Purchase,CoinData, PurchaseStats as Stats
from data import silver_spot_price,gold_spot_price,platinum_spot_price,palladium_spot_price


if __name__ == "__main__":
    silver = Stats()
    gold = Stats()
    platinum = Stats()
    palladium = Stats()
    other = Stats()
    try:
        db = DB_Interface()
        db.connect(config.db_config)

        purchases = {}
        coins = db.fetchCoins({"show_only_owned":True})
        entries = db.fetchPurchases()
        
        for entry in entries:
            key = entry[0]
            purchase = Purchase(*entry[1:])
            try:
                purchases[key][1].append(purchase)
            except KeyError:
                purchases[key] = (None,[purchase])

        for entry in coins:
            item = CoinData(
                        weight=entry[1],
                        fineness=entry[2],
                        precious_metal_weight=entry[3],
                        years=entry[4],
                        metal=entry[5],
                        nickname=entry[6],
                    )
            try:
                purchases[entry[0]] = (item,purchases[entry[0]][1])
            except KeyError:
                continue
        for key in purchases.keys():
            entry = purchases[key]
            Coins.price(silver_spot_price,gold_spot_price,platinum_spot_price,palladium_spot_price,entry[0])
            runner = other
            match entry[0].metal:
                case Metals.SILVER:
                    runner = silver
                case Metals.GOLD:
                    runner = gold
                case Metals.PLATINUM:
                    runner = platinum
                case Metals.PALLADIUM:
                    runner = palladium

            temp = Stats()
            print(f"+-{entry[0]}")
            for purchase in entry[1]:
                print(f"|~ {purchase}")
                temp.addPurchase(purchase,entry[0].value,entry[0].value*entry[0].retention)
                runner.addPurchase(purchase,entry[0].value,entry[0].value*entry[0].retention)
            print(f"+-{Coins.print_statistics(stats=temp)}")
            print()

        total = silver + gold + platinum + palladium
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
    finally:
        db.closeConnection()


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
