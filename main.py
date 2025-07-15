import argparse
import collection
import data as d
import search
from metals import Metals

import test


def setupParser():
    __version_info__ = ("0","0","1")
    __version__ = ".".join(__version_info__)
    parser = argparse.ArgumentParser(description="Prints information and prices on various coins made of gold and silver. These command line arguments are optional.")
    parser.add_argument("-v","--version",action="version",version=f"%(prog)s {__version__}")
    parser.add_argument("-n","--no_price",action="store_true",help="Use to disable printing of the melt value of the coins.")
    parser.add_argument("-g","--gold",metavar="PRICE",help="Use to supply the gold price for melt value calculations.")
    parser.add_argument("-s","--silver",metavar="PRICE",help="Use to supply the silver price for melt value calculations.")
    parser.add_argument("-c","--country",metavar="COUNTRY",help="Name of the country to return results for. Ex: France")
    parser.add_argument("-y","--year",metavar="YEAR",help="Year of coin to return results for. Ex: 1898")
    parser.add_argument("-d","--denomination",metavar="DENOMINATION",help="Coin denomination to return results for. Ex: Franc")
    parser.add_argument("-f","--face_value",metavar="FACE_VALUE",help="Face value of coin to return results for. Ex: 10")
    return parser


def price(data,silver_price=None,gold_price=None):
    silver = d.silver_spot_price
    gold = d.gold_spot_price
    if silver_price is not None and (isinstance(silver_price,int) or isinstance(silver_price,float)):
        silver = silver_price
    if gold_price is not None and (isinstance(gold_price,int) or isinstance(gold_price,float)):
        gold = gold_price
    if isinstance(data,collection.CoinCollection):
        data.price(silver,gold)


parser = setupParser()
args = vars(parser.parse_args())
print(f"arguments: {args}")
display_price = not args["no_price"]

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

# United States
united_states = d.coinsUnitedStates()

# France
france = d.coinsFrance()

# Germany
germany = d.coinsGermany()

# Mexico
mexico = d.coinsMexico()

# Italy
italy = d.coinsItaly()

# Canada
canada = d.coinsCanada()


data = collection.CoinCollection(
    countries=sorted([canada,united_states, mexico, france, germany, italy], key=lambda country: country.name),
    name="Precious Metals",
)

if display_price:
    price(data,args["silver"],args["gold"])
    print(f"Silver Spot: ${d.silver_spot_price:.2f}")
    print(f"Gold Spot: ${d.gold_spot_price:.2f}")

data.tree.cascading_set_fancy(True)
interactive_mode = False


lines = []
if interactive_mode:
    s = search.Search()
    results = s.performSearch(data, "France")
    # results = search.performSearch(data, "France")
    if results is None or len(results) == 0:
        print("No results found")
    else:
        if not isinstance(results, list):
            results = [results]
        for item in results:
            if isinstance(item, collection.Country) or isinstance(
                item, collection.Denomination
            ):
                item.tree.cascading_set_fancy(True)
                lines += item.tree.print()
            else:
                print(item)
else:
    lines = data.tree.print()

for line in lines:
    print(line)
