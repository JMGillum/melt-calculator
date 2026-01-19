#   Author: Josh Gillum              .
#   Date: 18 January 2026           ":"         __ __
#                                  __|___       \ V /
#                                .'      '.      | |
#                                |  O       \____/  |
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
#
#    This script is a useful tool for figuring out the intrinsic or "melt"
#    value of various different world coins. It prints them out in a tree
#    structure.
#
#    Searching for specific coins or groups of coins is also supported. Searches
#    can be as specific as '1898 German 10 Mark', or simply '1866'. The first
#    would show the single coin (along with its associated country and
#    denomination). The second search would simply return all coins that were
#    minted in 1866.
#
#    Run the script with the '--help' flag to see a list of a supported command
#    line arguments. The most useful of which are probably:
#        -S <search_string> this allows you to provide a string representing
#            your search query
#        -s <silver_price> this allows you to supply the silver price to be
#            used when calculating value
#        -g <gold_price> same as with silver price, but for gold.
#        -p <platinum_price> same as above, but for platinum.
#        -P <palladium_price> same as above, but for palladium.
#
#    * Checkout data.py to change the default precious metal prices used
#    when one isn't supplied
#
#    * Purchases are supported, but no script is yet available for adding them.
#
#    Finally, make sure to read README.md or README.txt for more information
#    about the program and how to use it to its fullest potential.
#
#    Thank you.
#
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

from coins import Coins
import config
import general

import sys  # Used to check if stdin is not from a terminal (piping input)
from setup import initialSetup,setupMetals
from db_interface import DB_Interface


# Enumeration used for argument tuples for searches
COUNTRY = 0
DENOMINATION = 1
YEAR = 2
FACE_VALUE = 3
FACE_VALUE_NAME = 4


def search(args,db,purchases,prices):
    # Determines if the user provided any search criteria, either by
    # Exact command line flags, a search string, or a search file
    if args["country"] or args["denomination"] or args["year"] or args["face_value"] or args["face_value_name"]:
        arguments_list = [
            (args["country"], args["denomination"], args["year"], args["face_value"],args["face_value_name"])
        ]
    else:
        arguments_list = []
    input_strings = []
    # If multiple searches are to be performed
    if not sys.stdin.isatty():  # Input is a piped in file
        input_strings = sys.stdin
    elif args["search_file"]:  # Search file was provided
        with open(args["search_file"], "r") as f:
            input_strings = f.readlines()
    if args["search_string"]:
        input_strings.append(args["search_string"])

    # Parses all of the search strings and gets 4 element tuples of arguments
    for item in input_strings:
        arguments_list.append(
            Coins.parseSearchString(db, item, debug=args["verbose"])
        )

    # Goes through each set of arguments and searches
    if arguments_list:
        for arguments in arguments_list:  # Loops through each search
            # At least one argument is defined
            if (
                arguments[COUNTRY]
                or arguments[DENOMINATION]
                or arguments[YEAR]
                or arguments[FACE_VALUE]
                or arguments[FACE_VALUE_NAME]
            ):
                fail_year = False
                fail_face_value = False
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
                            arguments[FACE_VALUE_NAME],
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
                    fail_year = True
                if arguments[FACE_VALUE]:
                    fail_face_value,face_value = general.strToNum(arguments[FACE_VALUE])
                    if fail_face_value:
                        print(
                            f"The specified face_value ({arguments[FACE_VALUE]}) is not valid. It must be a number"
                        )
                    else:
                        arguments = (
                            arguments[COUNTRY],
                            arguments[DENOMINATION],
                            arguments[YEAR],
                            face_value,
                            arguments[FACE_VALUE_NAME]
                        )
                        print(
                            f"Face value was successfully converted to {arguments[FACE_VALUE]}"
                        )
                else:
                    if args["verbose"]:
                        print("face_value was not provided. Ignoring...")
                if (
                    not fail_year and not fail_face_value
                ):  # The year and face_value could be converted to numeric types if applicable
                    if args["verbose"]:
                        print(
                            "The year and/or face_value arguments were successfully converted."
                        )
                    search_arguments = {
                        "country":arguments[COUNTRY],
                        "denomination":arguments[DENOMINATION],
                        "year":arguments[YEAR],
                        "face_value":arguments[FACE_VALUE],
                        "face_value_name":arguments[FACE_VALUE_NAME],
                        "debug":args["verbose"],
                        "show_only_owned":args["owned"],
                        "show_only_not_owned":args["not_owned"],
                    }
                    results = db.fetchCoins(search_arguments)
                    results = Coins.build(
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
                            f"{arguments[DENOMINATION]}"
                            if arguments[DENOMINATION]
                            else ""
                        )
                        results.set_name(
                            f"Results for '{text_year}{text_country}{text_face_value}{text_denomination}'".strip()
                        )
                        results.cascading_set_fancy(config.tree_fancy_characters)
                        if not args["no_tree"]:
                            for line in results.print():
                                print(line)

    # Done when no search specifiers were provided.
    else:  # Simply prints out all of the coins.
        search_arguments = {
            "debug":args["verbose"],
            "show_only_owned":args["owned"],
            "show_only_not_owned":args["not_owned"],
        }
        results = db.fetchCoins(search_arguments)
        results = Coins.build(
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
        )
        results.cascading_set_fancy(config.tree_fancy_characters)

        if not args["no_tree"]:
            for line in results.print():
                print(line)

if __name__ == "__main__":
    args = initialSetup()

    if args["command"] in ["collection","search"]:
        try:  # Connects to database
            db = DB_Interface(debug=args["verbose"])
            db.connect(config.db_config)
            
            purchases,prices = setupMetals(db,args)

            if args["command"] == "search":
                search(args,db,purchases,prices)
        finally:
            # 4. Close Cursor and Connection
            db.closeConnection()
