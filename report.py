#   Author: Josh Gillum              .
#   Date: 7 February 2026           ":"         __ __
#                                  __|___       \ V /
#                                .'      '.      | |
#                                |  O       \____/  |
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
#
#    This script provides a function for displaying all the owned coins (those 
#    with associated purchases), and providing summary statistics about them.
#
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

import config

from coins import Coins # Provides functions for searching for coins and building the results tree
from coinData import Purchase, PurchaseStats as Stats # Classes for storing purchases for statistical purposes.

def CollectionReport(args,db,purchases,prices):
    """Prints out a tree of owned coins as well as some profit statistics broken down by metal type."""

    metal_stats = {} # Stores totals for each metal type, key is atomic symbol, and value is Stats() object
    for key,_ in prices.items():
        metal_stats[key] = Stats()
    metal_stats |= {"other":Stats()} # Catch-all for any undefined metals
    prices |= {"other":("other",0.0,None)} # Appends other metal price

    # Only filter applied is to show only owned.
    search_arguments = {
        "debug":args["verbose"],
        "show_only_owned":True,
    }
    # Builds the associations between coins
    results = db.FetchCoins(search_arguments)
    results = Coins.Build(
        results,
        prices=prices,
        purchases=purchases,
        debug=args["verbose"],
        show_only_bullion=args["only_bullion"],
        show_only_not_bullion=args["hide_bullion"],
        only_coin_ids=args["only_coin_ids"],
        hide_coins=args["no_coins"],
        hide_values=args["no_values"],
        hide_denominations=args["no_denominations"],
        do_not_build_tree=True
    )
    # Results returned a tuple of (countries,denominations,values,coins)
    # coins is a dict of {coin_id: (coin_id,CoinData)}
    for entry in purchases:
        key = entry[0] # coin_id purchase is associated with
        purchase = Purchase(*(entry[1:4]+entry[5:])) # purchase price, quantity, date, mint date, mint mark
        coin = None
        try:
            coin = results[3][key][1] # CoinData object
        except KeyError:
            continue # Not found when building tree. Just skip and don't calculate statistics on it
        runner = metal_stats["other"] # Defaults to other metal
        try:
            runner = metal_stats[coin.metal] # Updates metal to apply statistics to
        except KeyError:
            pass
        runner.addPurchase(purchase,coin.value,coin.value*coin.retention)

    # Adds up all of the metals to the total
    total = metal_stats["other"]
    for _,metal in metal_stats.items():
        total += metal

    # Finishes building tree using saved tuple from Coins.build()
    results = Coins.BuildTree(*results,purchases=purchases,debug=args["verbose"],only_coin_ids=args["only_coin_ids"])
    results.cascading_set_fancy(config.tree_fancy_characters)

    # Prints tree
    if not args["no_tree"]:
        for line in results.print():
            print(line)

    # Prints Total statistics
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
                    name = prices[key][0].title()
                except KeyError:
                    pass

            # Prints the name of the metal and the associated statistics
            print(f"{name}:\n  ",end="")
            print(Coins.PrintStatistics(stats=metal))
        print("Total:\n  ",end="")
        print(Coins.PrintStatistics(stats=total))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

if __name__ == "__main__":
    print("This script is not meant to be called on its own. Please use the main script.")
