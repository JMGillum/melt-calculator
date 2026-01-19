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

from setup import initialSetup,setupMetals


if __name__ == "__main__":

    args = initialSetup()
    # Stores sum and count statistics for each metal type

    coins = [] # Stores all coins with purchases
    metal_stats = {}
    purchases = {}
    purchase_entries = []
    metal_prices = {}
    try:
        db = DB_Interface()
        db.connect(config.db_config)
        purchase_entries, metal_prices = setupMetals(db,args) # Gets a list of all purchases and the metal prices.
        for key,_ in metal_prices.items():
            metal_stats[key] = Stats()
        metal_stats |= {"other": Stats()} # Catch all for any undefined metals
        coins = db.fetchCoins({"show_only_owned":True}) # Gets a list of all coins with associated purchases
        
    finally:
        db.closeConnection()
        
    for entry in purchase_entries:
        key = entry[0]
        purchase = Purchase(*(entry[1:4]+entry[5:]))
        try:
            purchases[key][1].append(purchase)
        except KeyError:
            purchases[key] = (None,[purchase])

    for entry in coins:
        # Create CoinData objects for each coin with purchases
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

    for key,entry in metal_prices.items():
        name,price,date = entry
        if key == "other":
            price = 0
        if price < 0:
            print(f"WARNING: PRICE FOR [{key}]({name.title()}) HAS NOT BEEN SET. PLEASE UPDATE DATABASE BEFORE CONTINUING...")
            exit(1)
        metal_prices[key] = (name,float(price),date)
    for key in purchases.keys():
        entry = purchases[key]
        Coins.price(entry[0],**metal_prices)
        runner = metal_stats["other"]
        try: # Sets which metal the stats will be updated for
            runner = metal_stats[entry[0].metal]
        except KeyError: # The metal composition of the coin is not a defined type.
            pass

        temp = Stats()
        print(f"+-{entry[0]}")
        for purchase in entry[1]: # Prints each purchase associated with the coin
            print(f"|~ {purchase}")
            temp.addPurchase(purchase,entry[0].value,entry[0].value*entry[0].retention)
            runner.addPurchase(purchase,entry[0].value,entry[0].value*entry[0].retention)
        print(f"+-{Coins.print_statistics(stats=temp)}")
        print()

    total = metal_stats["other"]
    for _,metal in metal_stats.items():
        total += metal
    
    if total.count > 0:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("|                                   Totals:                                    |")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for key,metal in metal_stats.items():
            # Determines the name of the metal for total statistics display
            name = "Undefined"
            if key.lower() == "other":
                name = "Other"
            else:
                try:
                    name = metal_prices[key][0].title()
                except KeyError:
                    pass

            # Prints the name of the metal and the associated statistics
            print(f"{name}:\n  ",end="")
            print(Coins.print_statistics(stats=metal))
        print("Total:\n  ",end="")
        print(Coins.print_statistics(stats=total))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

