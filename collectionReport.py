#   Author: Josh Gillum              .
#   Date: 4 August 2025             ":"         __ __
#                                  __|___       \ V /
#                                .'      '.      | |
#                                |  O       \____/  |
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
#
#    This script prints out a report of the personal collection of coins. It
#    utilizes Coins.owned in coins/coins.py. See purchases.py for information on
#    how to add and update purchases. This script is still a work in progress.
#
#    Use the script by calling it as main from the command line
#
#
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

from db_interface import DB_Interface
from queries import Queries
from coins import Coins
import config
from coinData import Purchase,CoinData, PurchaseStats as Stats
from data import metals


if __name__ == "__main__":
    silver = Stats()
    gold = Stats()
    platinum = Stats()
    palladium = Stats()
    rhodium = Stats()
    other = Stats()
    metals = [("ag",silver),("au",gold),("pt",platinum),("pd",palladium),("rh",rhodium),("other",other)]
    entries = []
    coins = []
    purchases = {}
    prices = {}
    prices_entries = {}
    try:
        db = DB_Interface()
        db.connect(config.db_config)

        coins = db.fetchCoins({"show_only_owned":True})
        entries = db.fetchPurchases()
        prices_entries = db.fetchMetals()
        
    finally:
        db.closeConnection()
        
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

    for entry in prices_entries:
        key,name,price,date = entry
        if key == "other":
            price = 0
        if price < 0:
            print(f"WARNING: PRICE FOR [{key}]({name.title()}) HAS NOT BEEN SET. PLEASE UPDATE DATABASE BEFORE CONTINUING...")
            exit(1)
        prices[key] = (name,float(price),date)
    for key in purchases.keys():
        entry = purchases[key]
        Coins.price(entry[0],**prices)
        runner = other
        for key,metal in metals:
            if entry[0].metal == key:
                runner = metal

        temp = Stats()
        print(f"+-{entry[0]}")
        for purchase in entry[1]:
            print(f"|~ {purchase}")
            temp.addPurchase(purchase,entry[0].value,entry[0].value*entry[0].retention)
            runner.addPurchase(purchase,entry[0].value,entry[0].value*entry[0].retention)
        print(f"+-{Coins.print_statistics(stats=temp)}")
        print()

    total = other
    for _,metal in metals:
        total += metal
    
    if total.count > 0:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("|                                   Totals:                                    |")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for key,metal in metals:
            print(f"{prices[key][0].title()}:\n  ",end="")
            print(Coins.print_statistics(stats=metal))
        print("Total:\n  ",end="")
        print(Coins.print_statistics(stats=total))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

