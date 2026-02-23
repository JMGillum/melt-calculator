#   Author: Josh Gillum              .
#   Date: 10 February 2026          ":"         __ __
#                                  __|___       \ V /
#                                .'      '.      | |
#                                |  O       \____/  |
# ~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
#
#    This script provides a function for performing a search on the coins
#    within the database.
#
# ~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

import sys  # Used to check if stdin is not from a terminal (input was piped)


from coins import Coins  # Functions for finding coins and building tree
import treasure.text  # Used to convert strings to numbers


def Search(args, db, purchases, prices, config):
    """Searches the database for coins that match the given criteria."""
    # Enumeration used for argument tuples for searches
    COUNTRY = 0
    DENOMINATION = 1
    YEAR = 2
    FACE_VALUE = 3
    FACE_VALUE_NAME = 4

    # Determines if the user provided any search criteria, either by
    # Exact command line flags, a search string, or a search file
    if (
        args["country"]
        or args["denomination"]
        or args["year"]
        or args["face_value"]
        or args["face_value_name"]
    ):
        arguments_list = [
            (
                args["country"],
                args["denomination"],
                args["year"],
                args["face_value"],
                args["face_value_name"],
            )
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
        arguments_list.append(Coins.ParseSearchString(db, item, debug=args["verbose"],config=config))

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
                    fail_face_value, face_value = treasure.text.FractionStrToNum(
                        arguments[FACE_VALUE]
                    )
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
                            arguments[FACE_VALUE_NAME],
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
                        "country": arguments[COUNTRY],
                        "denomination": arguments[DENOMINATION],
                        "year": arguments[YEAR],
                        "face_value": arguments[FACE_VALUE],
                        "face_value_name": arguments[FACE_VALUE_NAME],
                        "debug": args["verbose"],
                        "show_only_owned": args["owned"],
                        "show_only_not_owned": args["not_owned"],
                    }
                    results, mapping = db.FetchCoins(
                        search_arguments
                    )  # Fetches coins based on search criteria
                    # Builds the results into a tree
                    results = Coins.Build(
                        results,
                        mapping,
                        config=config,
                        prices=prices,
                        purchases=purchases,
                        debug=args["verbose"],
                        show_only_bullion=args["only_bullion"],
                        show_only_not_bullion=args["hide_bullion"],
                        show_coin_ids=args["show_coin_ids"],
                        hide_coins=args["no_coins"],
                        hide_values=args["no_values"],
                        hide_denominations=args["no_denominations"],
                    )
                    if results is None:
                        print(
                            f"No results found for {arguments[COUNTRY]} {arguments[YEAR]} {arguments[DENOMINATION]} {arguments[FACE_VALUE]}"
                        )
                    else:  # Search found some results
                        # Determines how to present the search performed as a string, then sets the title of the tree to it.
                        # the provided year, otherwise nothing
                        text_year = f"{arguments[YEAR]} " if arguments[YEAR] else ""
                        # The provided country, otherwise nothing
                        text_country = (
                            f"{arguments[COUNTRY]} " if arguments[COUNTRY] else ""
                        )
                        # The provided face value, otherwise nothing
                        text_face_value = (
                            f"{arguments[FACE_VALUE]} " if arguments[FACE_VALUE] else ""
                        )
                        # The provided denomination, otherwise nothing
                        text_denomination = (
                            f"{arguments[DENOMINATION]}"
                            if arguments[DENOMINATION]
                            else ""
                        )
                        # Sets the title for the tree
                        results.set_name(
                            f"Results for '{text_year}{text_country}{text_face_value}{text_denomination}'".strip()
                        )
                        # Updates whether the tree will use fancy characters or not
                        results.set_fancy(config["tree_fancy_characters"], cascade=True)
                        if not args["no_tree"]:  # If tree is to be printed, print it.
                            for line in results.print():
                                print(line)

    # Done when no search specifiers were provided.
    else:  # Simply prints out all of the coins.
        search_arguments = {
            "debug": args["verbose"],
            "show_only_owned": args["owned"],
            "show_only_not_owned": args["not_owned"],
        }
        results, mapping = db.FetchCoins(search_arguments)
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
        results.set_fancy(config["tree_fancy_characters"], cascade=True)

        if not args["no_tree"]:
            for line in results.print():
                print(line)


if __name__ == "__main__":
    print(
        "This script is not meant to be called on its own. Please use the main script."
    )
