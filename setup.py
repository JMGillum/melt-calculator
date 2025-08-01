from __init__ import __version__
import argparse

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
        "-b",
        "--only_bullion",
        action="store_true",
        help="Show only the coins that are tagged as bullion. Does nothing when used with the --hide_bullion flag.",
    )
    parser.add_argument(
        "-B",
        "--hide_bullion",
        action="store_true",
        help="Shows only the coins that are not tagged as bullion. Does nothing when used with the --only_bullion flag.",
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
        "-H",
        "--hide_price",
        action="store_true",
        help="Use to disable printing of the melt value of the coins.",
    )
    parser.add_argument(
        "-n",
        "--no_coins",
        action="store_true",
        help="Disables printing of the actual coin objects. Will only print countries, denominations, and face values.",
    )
    parser.add_argument(
        "-N",
        "--no_tree",
        action="store_true",
        help="Disables printing of the output tree. Only really useful for seeing debugging output.",
    )
    parser.add_argument(
        "-i",
        "--only_coin_ids",
        action="store_true",
        help="Disables printing of actual coin objects, only printing their id's instead",
    )
    parser.add_argument(
        "-s",
        "--silver",
        metavar="PRICE",
        help="Use to supply the silver price for melt value calculations.",
    )
    parser.add_argument(
        "-p",
        "--platinum",
        metavar="PRICE",
        help="Use to supply the platinum price for melt value calculations.",
    )
    parser.add_argument(
        "-P",
        "--palladium",
        metavar="PRICE",
        help="Use to supply the palladium price for melt value calculations.",
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
