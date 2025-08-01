"""
   Author: Josh Gillum              .
   Date: 31 July 2025              ":"         __ __
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
        -p <platinum_price> same as above, but for platinum.

    * Checkout the data.py to change the default gold and silver prices that are
    used when you don't manually supply one.
    * Checkout purchases.py to add your own personal collection. This lets
    you quickly see what your purchases of a single coin are, and how they
    compare to its intrinsic value.
    * Checkout coins/coins.py to add other coins to the program if you aren't
    happy with the selection.

    Finally, make sure to read README.md or README.txt for more information
    about the program and how to use it to its fullest potential.

    Thank you.

^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
"""
import data as d
import search
from coins.coins import Coins
import config

import sys # Used to check if stdin is not from a terminal (piping input)
from setup import setupParser
import mariadb
import sys
import getpass


# Enumeration used for argument tuples for searches
COUNTRY = 0
DENOMINATION = 1
YEAR = 2
FACE_VALUE = 3





# Calculates the value of every defined coin.
def price(silver_price=None, gold_price=None, platinum_price=None, palladium_price=None):
    silver = d.silver_spot_price
    gold = d.gold_spot_price
    platinum = d.platinum_spot_price
    palladium = d.palladium_spot_price
    if silver_price is not None and (
        isinstance(silver_price, int) or isinstance(silver_price, float)
    ):
        silver = silver_price
    if gold_price is not None and (
        isinstance(gold_price, int) or isinstance(gold_price, float)
    ):
        gold = gold_price
    if platinum_price is not None and (isinstance(platinum_price,int) or isinstance(platinum_price,float)):
        platinum = platinum_price
    if palladium_price is not None and (isinstance(palladium_price,int) or isinstance(palladium_price,float)):
        palladium = palladium_price
    return(silver, gold, platinum,palladium)


def connect_to_mariadb(db_config):
    try:
        password = db_config["password"]
    except KeyError:
        password = db_config["password"] = None
    if password is None:
        if not sys.stdin.isatty():
            print("The program must be run from a terminal or password must be supplied in db_config")
            sys.exit(1)
        else:
            db_config["password"] = getpass.getpass("Password for mariadb: ")

    try: 
        print("Connecting to MariaDB...")
        conn = mariadb.connect(**db_config)
        print("Connection successful!")

        # 3. Create a Cursor Object
    except mariadb.Error as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    return conn


    




parser = setupParser()
args = vars(parser.parse_args())
if args["verbose"]:
    print(f"arguments: {args}")



# Updates data.silver_spot_price and data.gold_spot_price with values provided on command line, if applicable
try:
    if args["silver"] is not None:
        d.silver_spot_price = round(float(args["silver"]), 2)
except ValueError:
    print(
        f"Silver price provided is invalid type. Using value ({config.currency_symbol}{d.silver_spot_price:.2f}) defined in data.py instead."
    )
try:
    if args["gold"] is not None:
        d.gold_spot_price = round(float(args["gold"]), 2)
except ValueError:
    print(
        f"Gold price provided is invalid type. Using value ({config.currency_symbol}{d.gold_spot_price:.2f}) defined in data.py instead."
    )
try:
    if args["platinum"] is not None:
        d.platinum_spot_price = round(float(args["platinum"]), 2)
except ValueError:
    print(
        f"Platinum price provided is invalid type. Using value ({config.currency_symbol}{d.platinum_spot_price:.2f}) defined in data.py instead."
    )
try:
    if args["palladium"] is not None:
        d.palladium_spot_price = round(float(args["palladium"]), 2)
except ValueError:
    print(
        f"Palladium price provided is invalid type. Using value ({config.currency_symbol}{d.palladium_spot_price:.2f}) defined in data.py instead."
    )


# Prints out the precious metal prices and calculates the coins' worth
prices = price()
if not args["hide_price"]:
    print(f"Silver Spot: {config.currency_symbol}{d.silver_spot_price:.2f}")
    print(f"Gold Spot: {config.currency_symbol}{d.gold_spot_price:.2f}")
    print(f"Platinum Spot: {config.currency_symbol}{d.platinum_spot_price:.2f}")
    print(f"Palladium Spot: {config.currency_symbol}{d.palladium_spot_price:.2f}")
else:
    prices = None

conn = None
cursor = None
try: # Connects to database
    conn = connect_to_mariadb(config.db_config)
    cursor = conn.cursor()

    purchases = None
    if not args["hide_collection"]:
        cursor.execute("select purchases.coin_id,purchases.unit_price,purchases.purchase_quantity,purchases.purchase_date,specific_coins.year,specific_coins.mintmark from purchases left join specific_coins on purchases.specific_coin=specific_coins.id")
        purchases = list(cursor)




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
                    try:  # Converts the face_value from a string to either an int or float
                        face_value = int(arguments[FACE_VALUE])
                    except ValueError:
                        try:
                            face_value = float(arguments[FACE_VALUE])
                        except ValueError:
                            index = arguments[FACE_VALUE].find("/")
                            dash = arguments[FACE_VALUE].find("-")
                            if dash < 0:
                                dash = arguments[FACE_VALUE].find(" ")
                            if index > 0:
                                if dash > 0:
                                    prefix = arguments[FACE_VALUE][:dash]
                                    numerator = arguments[FACE_VALUE][dash+1:index]
                                else:
                                    prefix = 0
                                    numerator = arguments[FACE_VALUE][:index]
                                try:
                                    denominator = arguments[FACE_VALUE][index+1:]
                                    try:
                                        numerator = int(numerator)
                                        denominator = int(denominator)
                                        prefix = int(prefix)
                                        face_value = round(prefix + numerator/denominator,2)
                                    except ValueError:
                                        fail_face_value = True
                                except IndexError:
                                    fail_face_value = True
                            else:
                                fail_face_value = True
                    
                else:
                    if args["verbose"]:
                        print("face_value was not provided. Ignoring...")
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
                    )
                    print(f"Face value was successfully converted to {arguments[FACE_VALUE]}")

                if not fail_year and not fail_face_value:  # The year and face_value could be converted to numeric types if applicable
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
                        show_only_not_owned = args["not_owned"],
                        )
                    cursor.execute(results[0],results[1])
                    results = Coins.build(list(cursor),prices=prices,purchases=purchases,debug=args["verbose"],show_only_bullion=args["only_bullion"],show_only_not_bullion=args["hide_bullion"],only_coin_ids=args["only_coin_ids"],hide_coins=args["no_coins"])
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
                        if not args["no_tree"]:
                            for line in results.print():
                                print(line)

    # Done when no search specifiers were provided.
    else:  # Simply prints out all of the coins.
        query = Coins.search(debug=args["verbose"],show_only_owned = args["owned"],show_only_not_owned = args["not_owned"])
        cursor.execute(query[0],query[1])
        results = Coins.build(list(cursor),prices=prices,purchases=purchases,debug=args["verbose"],show_only_bullion=args["only_bullion"],show_only_not_bullion=args["hide_bullion"],only_coin_ids=args["only_coin_ids"],hide_coins=args["no_coins"])
        results.cascading_set_fancy(config.tree_fancy_characters)

        if not args["no_tree"]:
            for line in results.print():
                print(line)
        """
        # Builds Country objects for each country defined in data.countries
        countries = list(Coins.countries.keys())
        data = Coins.buildTree(countries, debug=args["verbose"], show_only_owned = args["owned"], show_only_not_owned = args["not_owned"], show_only_bullion=args["only_bullion"], show_only_not_bullion=args["hide_bullion"], hide_coins=args["no_coins"],only_coin_ids=args["only_coin_ids"])

        data.set_name("Precious Metals")
        data.cascading_set_fancy(config.tree_fancy_characters)
        for line in data.print():
            print(line)
        """

finally:
    # 4. Close Cursor and Connection
    if cursor:
        cursor.close()
        print("Cursor closed.")
    if conn:
        conn.close()
        print("Connection closed.")
