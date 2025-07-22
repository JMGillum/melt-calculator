"""
   Author: Josh Gillum              .
   Date: 21 July 2025              ":"         __ __
                                  __|___       \ V /
                                .'      '.      | |
                                |  O       \____/  |
^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

    This script is a useful tool for figuring out the intrinsic or "melt"
    value of various different world coins. It prints them out in a tree
    structure.

    Searching for specific coins or groups of coins is also supported. Searches
    can be as specific as '1898 German 10 Mark', or simply '1866'. The first
    would show the single coin (along with its associated country and 
    denomination). The second search would simply return all coins that were
    minted in 1866.

    Run the script with the '--help' flag to see a list of a supported command
    line arguments. The most useful of which are probably:
        -S <search_string> this allows you to provide a string representing
            your search query
        -s <silver_price> this allows you to supply the silver price to be
            used when calculating value
        -g <gold_price> same as with silver price, but for gold.

    * Checkout the data.py to change the default gold and silver prices that are
    used when you don't manually supply one.
    * Checkout purchases.py to add your own personal collection. This lets
    you quickly see what your purchases of a single coin are, and how they
    compare to its intrinsic value.
    * Checkout coinInfo.py to add other coins to the program if you aren't
    happy with the selection.

    Finally, make sure to read README.md or README.txt for more information
    about the program and how to use it to its fullest potential.

    Thank you.

^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
"""
__version_info__ = ("0", "3", "0")
__version__ = ".".join(__version_info__)
import argparse
import data as d
import search
from coinInfo import Coins
import config

import sys # Used to check if stdin is not from a terminal (piping input)

# Enumeration used for argument tuples for searches
COUNTRY = 0
DENOMINATION = 1
YEAR = 2
FACE_VALUE = 3



# Initializes all of the available command line arguments
def setupParser():
    parser = argparse.ArgumentParser(
        description="Prints information and prices on various coins made of gold and silver. These command line arguments are optional."
    )
    parser.add_argument(
        "-c",
        "--country",
        metavar="COUNTRY",
        help="Name of the country to return results for. Ex: France",
    )
    parser.add_argument(
        "-C",
        "--hide_collection",
        action="store_true",
        help="Use to disable printing of the personal collection of coins. Does nothing when used with --owned flag",
    )
    parser.add_argument(
        "-d",
        "--denomination",
        metavar="DENOMINATION",
        help="Coin denomination to return results for. Ex: Franc",
    )
    parser.add_argument(
        "-f",
        "--face_value",
        metavar="FACE_VALUE",
        help="Face value of coin to return results for. Ex: 10",
    )
    parser.add_argument(
        "-F",
        "--search_file",
        metavar="FILE",
        help="Name of file containing searches. Multiple searches are supported, and must be separated by newlines.",
    )
    parser.add_argument(
        "-g",
        "--gold",
        metavar="PRICE",
        help="Use to supply the gold price for melt value calculations.",
    )
    parser.add_argument(
        "-o",
        "--owned",
        action="store_true",
        help="Show only the coins that are in the personal collection. Takes precedence over --hide_collection. Does nothing when used with the --not_owned flag.",
    )
    parser.add_argument(
        "-O",
        "--not_owned",
        action="store_true",
        help="Show only the coins that are not in the personal collection. Does nothing when used with the --owned flag.",
    )
    parser.add_argument(
        "-p",
        "--hide_price",
        action="store_true",
        help="Use to disable printing of the melt value of the coins.",
    )
    parser.add_argument(
        "-s",
        "--silver",
        metavar="PRICE",
        help="Use to supply the silver price for melt value calculations.",
    )
    parser.add_argument(
        "-S",
        "--search_string",
        metavar="STRING",
        help="String enclosed in quotes, containing a search to be performed. Ex: '1898 German 10 mark'",
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "-V",
        "--verbose",
        action="store_true",
        help="Turns on additional printing. Useful for debugging.",
    )
    parser.add_argument(
        "-y",
        "--year",
        metavar="YEAR",
        help="Year of coin to return results for. Ex: 1898",
    )
    return parser


# Calculates the value of every defined coin.
def price(silver_price=None, gold_price=None):
    silver = d.silver_spot_price
    gold = d.gold_spot_price
    if silver_price is not None and (
        isinstance(silver_price, int) or isinstance(silver_price, float)
    ):
        silver = silver_price
    if gold_price is not None and (
        isinstance(gold_price, int) or isinstance(gold_price, float)
    ):
        gold = gold_price
    Coins.price(silver, gold)


parser = setupParser()
args = vars(parser.parse_args())
if args["verbose"]:
    print(f"arguments: {args}")

# Links all the defined purchases to their respective coins
if not args["hide_collection"]:
    Coins.linkPurchases(
        True
    )  # Links purchases to all of the coinData objects stored in coinInfo.Coins


# Updates data.silver_spot_price and data.gold_spot_price with values provided on command line, if applicable
try:
    if args["silver"] is not None:
        d.silver_spot_price = round(float(args["silver"]), 2)
except ValueError:
    print(
        f"Silver price provided is invalid type. Using value (${d.silver_spot_price:.2f}) defined in data.py instead."
    )
try:
    if args["gold"] is not None:
        d.gold_spot_price = round(float(args["gold"]), 2)
except ValueError:
    print(
        f"Gold price provided is invalid type. Using value (${d.gold_spot_price:.2f}) defined in data.py instead."
    )


# Prints out the precious metal prices and calculates the coins' worth
if not args["hide_price"]:
    price()
    print(f"Silver Spot: ${d.silver_spot_price:.2f}")
    print(f"Gold Spot: ${d.gold_spot_price:.2f}")
else:
    Coins.togglePrice(False) # Disables printing of the value of coins


# Determines if the user provided any search criteria, either by
# Exact command line flags, a search string, or a search file
if args["country"] or args["denomination"] or args["year"] or args["face_value"]:
    arguments_list = [
        (args["country"], args["denomination"], args["year"], args["face_value"])
    ]
else:
    arguments_list = []
input_strings = []
# If multiple searches are to be performed
if not sys.stdin.isatty(): # Input is a piped in file
    input_strings = sys.stdin
elif args["search_file"]: # Search file was provided
    with open(args["search_file"], "r") as f:
        input_strings = f.readlines()
if args["search_string"]:
    input_strings.append(args["search_string"])

# Parses all of the search strings and gets 4 element tuples of arguments
for item in input_strings:
    arguments_list.append(search.parseSearchString(item, debug=args["verbose"]))

# Goes through each set of arguments and searches
if arguments_list:
    for arguments in arguments_list:  # Loops through each search
        # At least one argument is defined
        if (
            arguments[COUNTRY]
            or arguments[DENOMINATION]
            or arguments[YEAR]
            or arguments[FACE_VALUE]
        ):
            fail = False
            year = None
            face_value = None
            # Attempts to convert year and face_value to numeric data type (int or float(only for face_value))
            try:  # Converts the year from a string to an int
                if arguments[YEAR]:
                    year = int(arguments[YEAR])
                    arguments = (
                        arguments[COUNTRY],
                        arguments[DENOMINATION],
                        year,
                        arguments[FACE_VALUE],
                    )
                    if args["verbose"]:
                        print(f"Year was successfully converted to {year}")
                else:
                    if args["verbose"]:
                        print("Year was not provided. Ignoring...")
            except ValueError:
                print(
                    f"The specified year ({arguments[YEAR]}) is not valid. It must be an integer"
                )
                fail = True
            try:  # Converts the face_value from a string to either an int or float
                if arguments[FACE_VALUE] and isinstance(arguments[FACE_VALUE], str):
                    index = arguments[FACE_VALUE].find(".")
                    if index > 0:
                        is_float = False
                        for i in range(index + 1, len(arguments[FACE_VALUE])):
                            if not (arguments[FACE_VALUE][i] == "0"):
                                face_value = float(arguments[FACE_VALUE])
                                is_float = True
                                break
                        if not is_float:
                            face_value = int(arguments[FACE_VALUE][:index])
                    else:
                        face_value = int(arguments[FACE_VALUE])
                    arguments = (
                        arguments[COUNTRY],
                        arguments[DENOMINATION],
                        arguments[YEAR],
                        face_value,
                    )
                    if args["verbose"]:
                        print(f"face value was successfully converted to {face_value}")
                else:
                    if args["verbose"]:
                        print("face_value was not provided. Ignoring...")
            except ValueError:
                print(
                    f"The specified face_value ({arguments[FACE_VALUE]}) is not valid. It must be a number"
                )
                fail = True

            if not fail:  # The year and face_value could be converted to numeric types if applicable
                if args["verbose"]:
                    print(
                        "The year and/or face_value arguments were successfully converted."
                    )
                results = Coins.search(
                    country=arguments[COUNTRY],
                    denomination=arguments[DENOMINATION],
                    year=arguments[YEAR],
                    face_value=arguments[FACE_VALUE],
                    debug=args["verbose"],
                    show_only_owned = args["owned"], 
                    show_only_not_owned = args["not_owned"]
                )
                if results is None:
                    print(
                        f"No results found for {arguments[COUNTRY]} {arguments[YEAR]} {arguments[DENOMINATION]} {arguments[FACE_VALUE]}"
                    )
                else:  # Search found some results
                    # Sorts results into their types and stores them in their respective lists
                    text_year = f"{arguments[YEAR]} " if arguments[YEAR] else ""
                    text_country = (
                        f"{arguments[COUNTRY]} " if arguments[COUNTRY] else ""
                    )
                    text_face_value = (
                        f"{arguments[FACE_VALUE]} " if arguments[FACE_VALUE] else ""
                    )
                    text_denomination = (
                        f"{arguments[DENOMINATION]}" if arguments[DENOMINATION] else ""
                    )
                    results.set_name(
                        f"Results for '{text_year}{text_country}{text_face_value}{text_denomination}'".strip()
                    )
                    results.cascading_set_fancy(config.tree_fancy_characters)
                    for line in results.print():
                        print(line)

# Done when no search specifiers were provided.
else:  # Simply prints out all of the coins.
    # Builds Country objects for each country defined in data.countries
    countries = list(Coins.countries.keys())
    data = Coins.buildTree(countries, debug=args["verbose"], show_only_owned = args["owned"], show_only_not_owned = args["not_owned"])

    data.set_name("Precious Metals")
    data.cascading_set_fancy(config.tree_fancy_characters)
    for line in data.print():
        print(line)


