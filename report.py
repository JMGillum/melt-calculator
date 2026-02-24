#   Author: Josh Gillum              .
#   Date: 23 February 2026          ":"         __ __
#                                  __|___       \ V /
#                                .'      '.      | |
#                                |  O       \____/  |
# ~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
#
#    This script provides a function for displaying all the owned coins (those
#    with associated purchases), and providing summary statistics about them.
#
# ~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

# Provides functions for searching for coins and building the results tree
from coins import Coins  

# Classes for storing purchases for statistical purposes.
from coinData import Purchase, PurchaseStats as Stats


def CollectionReport(args:dict, db, purchases:dict, prices:dict, config:dict):
    """ Same output as searching for owned coins. Then has profit statistics broken down by metal type.

    Args:
        db (DB_Interface): Object for interacting with the database 
        args: Passed to Coins.Build().
        purchases: Stores purchases in lists indexed by their associated coin_ids
        prices: Stores metal prices indexed by their keys in the database
        config: Stores config. Passed to Coins.Build()
    """

    metal_stats = {}  # Stores totals for each metal type, key is atomic symbol, and value is Stats() object
    for key, _ in prices.items():
        metal_stats[key] = Stats()
    metal_stats |= {"other": Stats()}  # Catch-all for any undefined metals
    prices |= {"other": ("other", 0.0, None)}  # Appends other metal price

    # Only filter applied is to show only owned.
    search_arguments = {
        "debug": args["verbose"],
        "show_only_owned": True,
    }

    # Fetches results
    results, mapping = db.FetchCoins(search_arguments)

    # Builds results into a tree
    results = Coins.Build(
        results,
        mapping,
        prices=prices,
        purchases=purchases,
        debug=args["verbose"],
        show_only_bullion=args["only_bullion"],
        show_only_not_bullion=args["hide_bullion"],
        show_coin_ids=args["show_coin_ids"],
        hide_coins=args["no_coins"],
        hide_values=args["no_values"],
        hide_denominations=args["no_denominations"],
        config=config,
    )

    # Adds every purchase to the respective metal total
    for _,country in results:
        for _,denomination in country:
            for _,value in denomination:

                # Every coin in results
                for _,coin in value:
                    runner = metal_stats["other"]
                    try:
                        runner = metal_stats[coin.data.metal]
                    except KeyError:
                        pass

                    # Every purchase for the coin
                    for _,purchase in coin:
                        if isinstance(purchase,Purchase):
                            runner.addPurchase(purchase,coin.data.value, coin.data.value * coin.data.retention)

    # Adds up all of the metals to the total
    total = metal_stats["other"]
    for _, metal in metal_stats.items():
        total += metal

    # Prints tree
    results.set_fancy(config["tree_fancy_characters"], cascade=True)
    if not args["no_tree"]:
        for line in results.print():
            print(line)

    # Prints Total statistics
    if total.count > 0:
        print(
            "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        )
        print(
            "|                                   Totals:                                    |"
        )
        print(
            "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        )
        for key, metal in metal_stats.items():
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
            print(f"{name}:\n  ", end="")
            print(Coins.PrintStatistics(config=config, stats=metal))
        print("Total:\n  ", end="")
        print(Coins.PrintStatistics(config=config, stats=total))
        print(
            "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        )


if __name__ == "__main__":
    print(
        "This script is not meant to be called on its own. Please use the main script."
    )
