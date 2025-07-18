__version_info__ = ("0","2","2")
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

# List of input for searches. Items are either a tuple of (country,year,denomination,face_value) or are searches as strings
if args["country"] or args["year"] or args["denomination"] or args["face_value"] or args["search_string"] or args["search_file"] or not sys.stdin.isatty():
    inputs = [(args["country"],args["year"],args["denomination"],args["face_value"])]
    if not sys.stdin.isatty():
        inputs = sys.stdin
    else:
        if args["search_file"]:
            with open(args["search_file"],"r") as f:
                inputs += f.readlines()
        if args["search_string"]:
            inputs.append(args["search_string"])

    data = None

    search_parameter_country = args["country"]
    search_parameter_year = args["year"]
    search_parameter_denomination = args["denomination"]
    search_parameter_face_value = args["face_value"]
    search_object = search.Search(country_name=args["country"],year=args["year"],denomination=args["denomination"],face_value=args["face_value"],debug=args["verbose"],text=args["search_string"])

    for item in inputs:
        if item is None:
            continue
        search_object = None
        if isinstance(item,tuple):
            if item[0] is None and item[1] is None and item[2] is None and item[3] is None:
                continue
            else:
                search_object = search.Search(country_name=item[0],year=item[1],denomination=item[2],face_value=item[3])
        elif isinstance(item,str):
            if args["verbose"]:
                print(f"The search string to be parsed is: {item}")
            search_object = search.Search(text=item)
        search_object.debug=args["verbose"]

        if search_object.text:
            search_object.parseSearchString()



        # If a country was specified on the command line, build its object here
        if search_object.country_name is not None:
            build = search.Search.countryInfo(search_object.country_name)
            if args["verbose"]:
                if build is not None:
                    print(f"Country {build[0].name} was successfully found from {search_object.country_name}.")
                else:
                    print(f"No country was found with the name {search_object.country_name}")
            if build is not None:
                search_object.country_name = build[0].name
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
        if search_object.country_name or search_object.denomination or search_object.face_value:
            fail = False
            year = None
            face_value = None
            try:
                if search_object.year is not None:
                    year = int(search_object.year)
                    if args["verbose"]:
                        print(f"Year was successfully converted to {year}")
                else:
                    if args["verbose"]:
                        print("Year was not provided. Ignoring...")
            except ValueError:
                print(f"The specified year ({search_object.year}) is not valid. It must be an integer")
                fail = True
            try:
                if search_object.face_value is not None and isinstance(search_object.face_value,str):
                    index = search_object.face_value.find(".")
                    if index > 0:
                        is_float = False
                        for i in range(index+1,len(search_object.face_value)):
                            if not (search_object.face_value[i] == '0'):
                                face_value = float(search_object.face_value)
                                is_float = True
                                break
                        if not is_float:
                            face_value = int(search_object.face_value[:index])
                    else:
                        face_value = int(search_object.face_value)
                    if args["verbose"]:
                        print(f"face value was successfully converted to {search_object.face_value}")
                else:
                    if args["verbose"]:
                        print("face_value was not provided. Ignoring...")
            except ValueError:
                print(f"The specified face_value ({search_object.face_value}) is not valid. It must be a number")
                fail = True

            if not fail:
                if args["verbose"]:
                    print("The year and/or face_value arguments were successfully converted.")
                lines = []
                if data is not None:
                    search_object.data = data
                    search_object.year = year
                    search_object.face_value = face_value
                    results = search_object.search(as_a_collection=True)
                else:
                    results = None
                if results is None:
                    print(f"No results found for {args['country']} {year} {args['denomination']} {face_value}")
                else: # Search found some results
                    # Sorts results into their types and stores them in their respective lists
                    text_year = f'{search_object.year} ' if year else ""
                    text_country = f'{search_object.country_name} ' if search_object.country_name else ""
                    text_face_value = f'{search_object.face_value} ' if search_object.face_value else ""
                    text_denomination = search_object.denomination if search_object.denomination else ""
                    results.tree.set_name(f"Results for \'{text_year}{text_country}{text_face_value}{text_denomination}\'".strip())
                    results.rebuildTree()
                    results.tree.cascading_set_fancy(True)
                    lines = results.tree.print()
                    for line in lines:
                        print(line)



        else: # If only the country was specified
            if data is not None:
                data.tree.cascading_set_fancy(True)
                for line in data.tree.print():
                    print(line)


else:
    Coins.linkPurchases()
    # Builds Country objects for each country defined in data.countries
    countries = list(Coins.countries.keys())
    data = Coins.buildTree(countries)

    data.set_name("Precious Metals")
    data.cascading_set_fancy(True)
    for line in data.print():
        print(line)
