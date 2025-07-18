__version_info__ = ("0","3","0")
__version__ = ".".join(__version_info__)
import argparse
import collection
import data as d
import search
from metals import Metals
import country
import coinData
from tree.tree import Tree
from coinInfo import Coins

import sys





def setupParser():
    parser = argparse.ArgumentParser(description="Prints information and prices on various coins made of gold and silver. These command line arguments are optional.")
    parser.add_argument("-c","--country",metavar="COUNTRY",help="Name of the country to return results for. Ex: France")
    parser.add_argument("-C","--hide_collection",action="store_true",help="Use to disable printing of the personal collection of coins. Does nothing when used with --owned flag")
    parser.add_argument("-d","--denomination",metavar="DENOMINATION",help="Coin denomination to return results for. Ex: Franc")
    parser.add_argument("-f","--face_value",metavar="FACE_VALUE",help="Face value of coin to return results for. Ex: 10")
    parser.add_argument("-F","--search_file",metavar="FILE",help="Name of file containing searches. Multiple searches are supported, and must be separated by newlines.")
    parser.add_argument("-g","--gold",metavar="PRICE",help="Use to supply the gold price for melt value calculations.")
    parser.add_argument("-o","--owned",action="store_true",help="Show only the coins that are in the personal collection. Takes precedence over --hide_collection. Does nothing when used with the --not_owned flag.")
    parser.add_argument("-O","--not_owned",action="store_true",help="Show only the coins that are not in the personal collection. Does nothing when used with the --owned flag.")
    parser.add_argument("-p","--hide_price",action="store_true",help="Use to disable printing of the melt value of the coins.")
    parser.add_argument("-s","--silver",metavar="PRICE",help="Use to supply the silver price for melt value calculations.")
    parser.add_argument("-S","--search_string",metavar="STRING",help="String enclosed in quotes, containing a search to be performed. Ex: \'1898 German 10 mark\'")
    parser.add_argument("-v","--version",action="version",version=f"%(prog)s {__version__}")
    parser.add_argument("-V","--verbose",action="store_true",help="Turns on additional printing. Useful for debugging.")
    parser.add_argument("-y","--year",metavar="YEAR",help="Year of coin to return results for. Ex: 1898")
    return parser


def price(silver_price=None,gold_price=None):
    silver = d.silver_spot_price
    gold = d.gold_spot_price
    if silver_price is not None and (isinstance(silver_price,int) or isinstance(silver_price,float)):
        silver = silver_price
    if gold_price is not None and (isinstance(gold_price,int) or isinstance(gold_price,float)):
        gold = gold_price
    Coins.price(silver,gold)

parser = setupParser()
args = vars(parser.parse_args())
if args["verbose"]:
    print(f"arguments: {args}")

if not args["hide_collection"]:
    Coins.linkPurchases(True) # Links purchases to all of the coinData objects stored in coinInfo.Coins


# Updates data.silver_spot_price and data.gold_spot_price with values provided on command line, if applicable
try:
    if args["silver"] is not None:
        d.silver_spot_price = round(float(args["silver"]),2)
except ValueError:
    print(f"Silver price provided is invalid type. Using value (${d.silver_spot_price:.2f}) defined in data.py instead.")
try:
    if args["gold"] is not None:
        d.gold_spot_price = round(float(args["gold"]),2)
except ValueError:
    print(f"Gold price provided is invalid type. Using value (${d.gold_spot_price:.2f}) defined in data.py instead.")

if not args["hide_price"]:
    price()
    print(f"Silver Spot: ${d.silver_spot_price:.2f}")
    print(f"Gold Spot: ${d.gold_spot_price:.2f}")
else:
    Coins.togglePrice(False)

if args["country"] or args["denomination"] or args["face_value"] or args["year"]:
    fail = False
    year = None
    face_value = None
    try:
        if args["year"] is not None:
            year = int(args["year"])
            if args["verbose"]:
                print(f"Year was successfully converted to {year}")
        else:
            if args["verbose"]:
                print("Year was not provided. Ignoring...")
    except ValueError:
        print(f"The specified year ({args['year']}) is not valid. It must be an integer")
        fail = True
    try:
        if args["face_value"] is not None and isinstance(args["face_value"],str):
            index = args["face_value"].find(".")
            if index > 0:
                is_float = False
                for i in range(index+1,len(args["face_value"])):
                    if not (args["face_value"][i] == '0'):
                        face_value = float(args["face_value"])
                        is_float = True
                        break
                if not is_float:
                    face_value = int(args["face_value"][:index])
            else:
                face_value = int(args["face_value"])
            if args["verbose"]:
                print(f"face value was successfully converted to {args['face_value']}")
        else:
            if args["verbose"]:
                print("face_value was not provided. Ignoring...")
    except ValueError:
        print(f"The specified face_value ({args['face_value']}) is not valid. It must be a number")
        fail = True

    if not fail:
        data = None
        if args["verbose"]:
            print("The year and/or face_value arguments were successfully converted.")
        lines = []
        if data is not None:
            results = None
        else:
            results = None
        if results is None:
            print(f"No results found for {args['country']} {year} {args['denomination']} {face_value}")
        else: # Search found some results
            # Sorts results into their types and stores them in their respective lists
            text_year = f'{year} ' if year else ""
            text_country = f'{args["country"]} ' if args["country"] else ""
            text_face_value = f'{face_value} ' if args["face_value"] else ""
            text_denomination = args["denomination"] if args["denomination"] else ""
            results.tree.set_name(f"Results for \'{text_year}{text_country}{text_face_value}{text_denomination}\'".strip())
            results.rebuildTree()
            results.tree.cascading_set_fancy(True)
            lines = results.tree.print()
            for line in lines:
                print(line)

else: 
    # Builds Country objects for each country defined in data.countries
    countries = list(Coins.countries.keys())
    data = Coins.buildTree(countries,debug=args["verbose"])

    data.set_name("Precious Metals")
    data.cascading_set_fancy(True)
    for line in data.print():
        print(line)
