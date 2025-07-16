__version_info__ = ("0","2","0")
__version__ = ".".join(__version_info__)
import argparse
import collection
import data as d
import search
from metals import Metals
import country
import coinData





def setupParser():
    parser = argparse.ArgumentParser(description="Prints information and prices on various coins made of gold and silver. These command line arguments are optional.")
    parser.add_argument("-v","--version",action="version",version=f"%(prog)s {__version__}")
    parser.add_argument("-g","--gold",metavar="PRICE",help="Use to supply the gold price for melt value calculations.")
    parser.add_argument("-s","--silver",metavar="PRICE",help="Use to supply the silver price for melt value calculations.")
    parser.add_argument("-c","--country",metavar="COUNTRY",help="Name of the country to return results for. Ex: France")
    parser.add_argument("-y","--year",metavar="YEAR",help="Year of coin to return results for. Ex: 1898")
    parser.add_argument("-d","--denomination",metavar="DENOMINATION",help="Coin denomination to return results for. Ex: Franc")
    parser.add_argument("-f","--face_value",metavar="FACE_VALUE",help="Face value of coin to return results for. Ex: 10")
    parser.add_argument("-p","--hide_price",action="store_true",help="Use to disable printing of the melt value of the coins.")
    parser.add_argument("-C","--hide_collection",action="store_true",help="Use to disable printing of the personal collection of coins.")
    parser.add_argument("-V","--verbose",action="store_true",help="Turns on additional printing. Useful for debugging.")
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
if args["verbose"]:
    print(f"arguments: {args}")
display_price = not args["hide_price"]

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

data = None

# If a country was specified on the command line, build its object here
if args["country"] and isinstance(args["country"],str):
    build = search.Search.countryInfo(args["country"])
    if args["verbose"]:
        if build is not None:
            print(f"Country {build[0].name} was successfully found from {args['country']}.")
        else:
            print(f"No country was found with the name {args['country']}")
    if build is not None:
        result = build[1](not args["hide_collection"])
        if args["verbose"]:
            print(f"Successfully built coin data for country {build[0].name}")
        data = collection.CoinCollection(countries=[result],name="Results")
else:
    # Builds Country objects for each country defined in data.countries
    country_coins = []
    for country in d.countries:
        country_coins.append(country[1](not args["hide_collection"]))
    country_coins = sorted(country_coins, key = lambda x: x.name)

    # Creates the final CoinCollection object of all of the countries
    data = collection.CoinCollection(
        countries=sorted(country_coins, key=lambda x: x.name),
        name="Precious Metals",
    )

if data is not None and args["hide_price"]:
    data.togglePrice(not args["hide_price"])

if display_price:
    if data is not None:
        price(data,args["silver"],args["gold"])
    print(f"Silver Spot: ${d.silver_spot_price:.2f}")
    print(f"Gold Spot: ${d.gold_spot_price:.2f}")
# Narrow down results if any of the more specific filters are present in the command line
if args["year"] or args["denomination"] or args["face_value"]:
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
        if args["face_value"] is not None:
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
                print(f"face value was successfully converted to {face_value}")
        else:
            if args["verbose"]:
                print("face_value was not provided. Ignoring...")
    except ValueError:
        print(f"The specified face_value ({args['face_value']}) is not valid. It must be a number")
        fail = True

    if not fail:
        if args["verbose"]:
            print("The year and/or face_value arguments were successfully converted.")
        lines = []
        if data is not None:
            s = search.Search()
            s.data = data
            s.year = year
            s.face_value = face_value
            s.debug = args["verbose"]
            s.denomination = args["denomination"]
            results = s.search(as_a_collection=True)
        else:
            results = None
        if results is None:
            print(f"No results found for {args['country']} {year} {args['denomination']} {face_value}")
        else: # Search found some results
            # Sorts results into their types and stores them in their respective lists
            text_year = f'{year} ' if year else ""
            text_country = f'{args["country"]} ' if args["country"] else ""
            text_face_value = f'{face_value} ' if face_value else ""
            text_denomination = args["denomination"] if args["denomination"] else ""
            results.tree.set_name(f"Results for \'{text_year}{text_country}{text_face_value}{text_denomination}\'")
            results.rebuildTree()
            results.tree.cascading_set_fancy(True)
            lines = results.tree.print()
            for line in lines:
                print(line)



else: 
    if data is not None:
        data.tree.cascading_set_fancy(True)
    interactive_mode = False


    lines = []
    if interactive_mode: # Test section. Will probably be deleted in the future
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
