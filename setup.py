from __init__ import __version__
import argparse

from updateMetalPrices import UpdateMetalPrices
from colorama import just_fix_windows_console
import data as d
from datetime import datetime
from colors import Colors


# Initializes all of the available command line arguments
def SetupParser():
    version_parser = argparse.ArgumentParser(add_help=False)
    version_parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    verbose_parser = argparse.ArgumentParser(add_help=False)
    verbose_parser.add_argument(
        "-V",
        "--verbose",
        action="store_true",
        help="Turns on additional printing. Useful for debugging.",
    )
    database_parser = argparse.ArgumentParser(add_help=False)
    database_parser.add_argument(
        "-D",
        "--database",
        metavar="DB",
        help="Name of the database to connect to.",
    )
    metal_prices_parser = argparse.ArgumentParser(add_help=False)
    metal_prices_parser.add_argument(
        "-g",
        "--gold",
        metavar="PRICE",
        help="Use to supply the gold price for melt value calculations.",
    )
    metal_prices_parser.add_argument(
        "-r",
        "--rhodium",
        metavar="PRICE",
        help="Use to supply the rhodium price for melt value calculations.",
    )
    metal_prices_parser.add_argument(
        "-s",
        "--silver",
        metavar="PRICE",
        help="Use to supply the silver price for melt value calculations.",
    )
    metal_prices_parser.add_argument(
        "-p",
        "--platinum",
        metavar="PRICE",
        help="Use to supply the platinum price for melt value calculations.",
    )
    metal_prices_parser.add_argument(
        "-P",
        "--palladium",
        metavar="PRICE",
        help="Use to supply the palladium price for melt value calculations.",
    )
    metal_prices_parser.add_argument(
        "-u",
        "--update_prices",
        action="store_true",
        help="Will push any prices set in the command line to the database.",
    )

    bullion_parser = argparse.ArgumentParser(add_help=False)
    bullion_parser.add_argument(
        "-b",
        "--only_bullion",
        action="store_true",
        help="Show only the coins that are tagged as bullion. Does nothing when used with the --hide_bullion flag.",
    )
    bullion_parser.add_argument(
        "-B",
        "--hide_bullion",
        action="store_true",
        help="Shows only the coins that are not tagged as bullion. Does nothing when used with the --only_bullion flag.",
    )

    search_parameter_parser = argparse.ArgumentParser(add_help=False)
    search_parameter_parser.add_argument(
        "-c",
        "--country",
        metavar="COUNTRY",
        help="Name of the country to return results for. Ex: France",
    )
    search_parameter_parser.add_argument(
        "-d",
        "--denomination",
        metavar="DENOMINATION",
        help="Coin denomination to return results for. Ex: Franc",
    )
    search_parameter_parser.add_argument(
        "-f",
        "--face_value",
        metavar="FACE_VALUE",
        help="Face value of coin to return results for. Ex: 10",
    )
    search_parameter_parser.add_argument(
        "-m",
        "--face_value_name",
        metavar="FACE_VALUE_NAME",
        help="Name of face value of coin to return results for. Ex: Dime",
    )
    search_parameter_parser.add_argument(
        "-F",
        "--search_file",
        metavar="FILE",
        help="Name of file containing searches. Multiple searches are supported, and must be separated by newlines.",
    )
    search_parameter_parser.add_argument(
        "-S",
        "--search_string",
        metavar="STRING",
        help="String enclosed in quotes, containing a search to be performed. Ex: '1898 German 10 mark'",
    )
    search_parameter_parser.add_argument(
        "-y",
        "--year",
        metavar="YEAR",
        help="Year of coin to return results for. Ex: 1898",
    )

    tree_output_modification_parser = argparse.ArgumentParser(add_help=False)
    tree_output_modification_parser.add_argument(
        "-n",
        "--no_coins",
        action="store_true",
        help="Disables printing of the actual coin objects. Will only print countries, denominations, and face values.",
    )
    tree_output_modification_parser.add_argument(
        "-z",
        "--no_values",
        action="store_true",
        help="Disables printing of the values down. Will only print countries and denominations.",
    )
    tree_output_modification_parser.add_argument(
        "-x",
        "--no_denominations",
        action="store_true",
        help="Disables printing of the denominations down. Will only print the countries.",
    )
    tree_output_modification_parser.add_argument(
        "-N",
        "--no_tree",
        action="store_true",
        help="Disables printing of the output tree. Only really useful for seeing debugging output.",
    )
    tree_output_modification_parser.add_argument(
        "-i",
        "--only_coin_ids",
        action="store_true",
        help="Disables printing of actual coin objects, only printing their id's instead",
    )

    parser = argparse.ArgumentParser(
        description="Prints information and prices on various coins made of gold and silver. These command line arguments are optional.", parents=[version_parser]
    )

    subparsers = parser.add_subparsers(dest="command")
    search_parser = subparsers.add_parser("search",parents=[metal_prices_parser,bullion_parser,search_parameter_parser,version_parser,verbose_parser,database_parser,tree_output_modification_parser])

    manage_parser = subparsers.add_parser("manage",parents=[version_parser])
    manage_subparsers = manage_parser.add_subparsers(dest="manage_command")
    backup_parser = manage_subparsers.add_parser("backup",parents=[version_parser,verbose_parser,database_parser])
    prices_parser = manage_subparsers.add_parser("prices",parents=[version_parser,verbose_parser,database_parser])

    backup_parser.add_argument("-p","--backup_purchases",action="store_true",help="Will backup the purchases and specific coin tables.")
    backup_parser.add_argument("-c","--backup_countries",action="store_true",help="Will backup the countries and country_names tables.")
    backup_parser.add_argument("-d","--backup_denominations",action="store_true",help="Will backup the denominations and denomination_names tables.")
    backup_parser.add_argument("-f","--backup_face_values",action="store_true",help="Will backup the face_values and face_values_names tables.")
    backup_parser.add_argument("-C","--backup_coins",action="store_true",help="Will backup the coins table.")
    backup_parser.add_argument("-F","--backup_config",action="store_true",help="Will backup the config file.")
    backup_parser.add_argument("-a","--backup_all",action="store_true",help="Will backup all of the tables. Shorthand for -pcCdf")
    backup_parser.add_argument(
        "-o",
        "--output_destination",
        metavar="STRING",
        help="Path to the directory that will store the backups. Backups will be stored /path/<timestamp>/xx. Default location is ./backups/<timestamp>/xx",
    )

    collection_parser = subparsers.add_parser("collection",parents=[version_parser])
    collection_subparsers = collection_parser.add_subparsers(dest="collection_command")
    report_parser = collection_subparsers.add_parser("report",parents=[metal_prices_parser,bullion_parser,version_parser,verbose_parser,database_parser,tree_output_modification_parser])
    collection_manage_parser = collection_subparsers.add_parser("manage",parents=[database_parser,version_parser,verbose_parser])
    collection_manage_parser.add_argument("-d","--delete",action="store_true",help="Switches to delete mode. (Deletes the entry from the purchases table)")
    search_parser.add_argument(
        "-C",
        "--hide_collection",
        action="store_true",
        help="Use to disable printing of the personal collection of coins. Does nothing when used with --owned flag",
    )
    search_parser.add_argument(
        "-o",
        "--owned",
        action="store_true",
        help="Show only the coins that are in the personal collection. Takes precedence over --hide_collection. Does nothing when used with the --not_owned flag.",
    )
    search_parser.add_argument(
        "-O",
        "--not_owned",
        action="store_true",
        help="Show only the coins that are not in the personal collection. Does nothing when used with the --owned flag.",
    )
    search_parser.add_argument(
        "-H",
        "--hide_price",
        action="store_true",
        help="Use to disable printing of the melt value of the coins.",
    )
    return parser

def InitialSetup(config):
    just_fix_windows_console() # Enables ANSI code support on windows or strips them if necessary
    # Command line arguments
    parser = SetupParser()
    args = vars(parser.parse_args())
    if args["verbose"]:
        print(f"arguments: {args}")

    # The database was specified in the command line
    if args["database"]:
        config["db_config"]["database"] = args["database"]

    return args

def UpdatePrices(prices,args,config,db=None):
    # Updates data.silver_spot_price and data.gold_spot_price with values provided on command line, if applicable
    update_prices = False
    try:
        update_prices = args["update_prices"]
    except KeyError:
        pass
    updates = []
    for key in prices:
        if not key == "other":
            name,price,date = prices[key]
            try:
                try:
                    current_date = datetime.today().strftime("%Y-%m-%d")
                    if args[name] is not None:
                        prices[key] = (name,round(float(args[name]), 2),current_date)
                        if update_prices:
                            updates.append((key,prices[key][1],current_date))
                except KeyError:
                    try:
                        if args["verbose"]:
                            print(f"Error updating price for key: {key}")
                    except KeyError:
                        pass

            except ValueError:
                print(
                    f"{name.title()} price provided is invalid type. Using value from database ({config["currency_symbol"]}{price})..."
                )
    if updates and db:
        results = UpdateMetalPrices(db,*updates)
        for item,result in results:
            if not result:
                print(f"{item} was not updated.")



def SetupMetals(db,args,config):
    hide_collection = False
    try:
        hide_collection = args["hide_collection"]
    except KeyError:
        pass
    hide_price = False
    try:
        hide_price = args["hide_price"]
    except KeyError:
        pass
        
    purchases = None
    if not hide_collection:
        purchases = db.FetchPurchases()

    # Fetches prices for the metals, as well as their names.
    # Updates prices if they were specified in the command line
    prices = {}
    if not hide_price:
        entries = db.FetchMetals()
        for entry in entries:
            key,name,price,date = entry 
            if not key == "other":
                prices[key] = (name,float(price),date)
        UpdatePrices(prices,args,config,db)
        d.metals = prices
        for key in prices:
            name,price,date = prices[key]
            if config["enforce_prices_set"] and price < 0:
                print(f"WARNING: PRICE FOR [{key}]({name.title()}) HAS NOT BEEN SET. PLEASE UPDATE DATABASE BEFORE CONTINUING...")
                exit(1)

        for key in prices:
            name,price,date = prices[key]
            if not hide_price:
                printed = False
                if config["show_metal_colors"]:
                    try:
                        print(f"{Colors.PrintColored(name.title(),config["show_color"],config["colors_8_bit"],config["metals_colors"][key])} spot: {config["currency_symbol"]}{price:.2f} as of: {date}")
                        printed = True
                    except KeyError:
                        pass
                if not printed:
                    print(f"{name.title()} spot: {config["currency_symbol"]}{price:.2f} as of: {date}")
    return purchases,prices

if __name__ == "__main__":
    print("This script is not meant to be called on its own. Please use the main script.")
