"""
   Author: Josh Gillum              .
   Date: 31 July 2025              ":"         __ __
   Code Start: Line 98            __|___       \ V /
                                .'      '.      | |
                                |  O       \____/  |
^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

    This file contains the actual data about all the coins used in the program.
    The typical structure used is:
        <Country> - Ex: Germany
            <Denomination> - Ex: Mark
                <Face value> - Ex: 10
                    <Set of years> - 1871-1915

    This structure allows for changes within the composition of a coin to be
    reflected. In order to add any new coins, each element of the structure
    must exist. First off is to add the actual coin data, with the aptly named
    CoinData class. See coinData.py for more information on the different data
    that can be stored.

    An example of the structure will follow. This is useful if you wish to add
    any new coins or modify existing ones.

    1. An entry must to the coins dictionary within the Coins class must be
    made. Below represents the 5 dollar Canadian Silver Maple Leaf coin,
    minted from 1988 to 2025 (current-year as of writing).


        "canada_dollar_5": Node(
            CoinData(
                nickname="Silver Maple Leaf Bullion",
                years=list(range(1988, current_year+1)),
                weight=31.11,
                fineness=0.9999,
                precious_metal_weight=weights.Weight(1, weights.Units.TROY_OUNCES),
                metal=Metals.SILVER,
                country="Canada",
                face_value=5,
                denomination="Dollars",
            )
        ),

    * The key needs to be some unique name that describes the coin. This value 
    is never displayed, so do not worry if it is a bit long or drawn out. 
    * The CoinData object must be the data variable of a Node object. See
    tree/node.py for more information on the Node class.
    * The CoinData object stores the actual information about the coin, once
    again, see coinData.py for information on the fields.

    2. An entry to the values dictionary in the Coins class must be added.
    This entry represents all of the coins of this face value, so all 5 
    dollar Canadian coins. If there are multiple coins of this face value, 
    place all of their keys inside the list. Using the above coin, the entry
    would be:

        "canada_dollar_5": NamedList("5", ["canada_dollar_5"]),

    * The NamedList class is simply a list with a name. The name gets returned
    whenever the list is cast to a string.

    3. An entry to the denominations dictionary in the Coins class must then
    be added. This entry represents all Canadian coins of the Dollar
    denomination. The modern Canadian monetary system also uses cents (ex:
    1 cent, 5 cent, 10 cent, etc.), which would have to be its own entry in
    this dictionary. Continuing with the example, the entry would be:

        "canada_dollar": NamedList("Dollars", ["canada_dollar_5"]),

    * Inside the list would be all face values of the Canadian dollar.

    4. Finally, an entry to the countries dictionary in the Coins class must
    be added. This represents all coins of the country (it could also be an
    issuing authority...). Below is the example entry:


        "canada": NamedList("Canada", ["canada_dollar"]),

    * The list stores all denominations for this country, so if coins 
    of the Canadian cent denomination were also defined, the Canadian cent
    denomination would have to be included in the list.

    * The coins_reverse_build dictionary must also be updated. Each entry
    is of the form <coin_id>:(face_value_id, denomination_id, country_id).
    Where each id is the corresponding key in each of the dictionaries. See
    helper.py for information on how to update this.

    ** Note that the NamedList object stores the keys for the objects of the
    lower tier that they represent. So, the "canada_dollar" denomination entry
    stores the keys of all Canadian dollar face_values, as defined in the
    values dictionary.

    ** See purchases.py if you would like to add your personal collection.

^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
"""

from coinData import CoinData,Purchase,PurchaseStats
from tree.tree import Tree
from tree.node import Node
from metals import Metals
from purchases import purchases
from config import currency_symbol,current_year
import config
from search import validCountry
import weights
from colors import printColored
from alternativeNames import AlternativeNames

from coins.namedList import NamedList
from coins.taggedList import TaggedList
from coins.tags import Tags





class Coins:

    # Enables or disables printing of the coins value
    def togglePrice(show_price=True):
        for coin_id in list(Coins.coins.keys()):
            coin = Coins.coins[coin_id]
            if isinstance(coin, Node):
                coin = coin.data
            coin.togglePrice(show_price)

    # Calculates the value of all defined coin objects, using the provided precious metal values
    def price(silver_price, gold_price, platinum_price, palladium_price,coin):
            if coin.metal == Metals.SILVER:
                coin.value = coin.precious_metal_weight.as_troy_ounces() * silver_price
            if coin.metal == Metals.GOLD:
                coin.value = coin.precious_metal_weight.as_troy_ounces() * gold_price
            if coin.metal == Metals.PLATINUM:
                coin.value = coin.precious_metal_weight.as_troy_ounces() * platinum_price
            if coin.metal == Metals.PALLADIUM:
                coin.value = coin.precious_metal_weight.as_troy_ounces() * palladium_price
            coin.togglePrice(True)



    def print_statistics(total:float=0.0,count:int=0,value:float=0.0,stats:PurchaseStats=None):
        if stats and isinstance(stats,PurchaseStats):
            total = round(stats.total,2)
            count = int(stats.count)
            if count > 0:
                value = round((stats.total+stats.delta)/stats.count,2)
        else:
            total = round(total,2)
            count = int(count)
            value = round(value,2)
        if count > 0:
            total_value = round(value*count,2)
            average = round(total/count,2)
            gain_loss = round(total_value-total,2)
            average_gain_loss = round(value-average,2)
            gain_loss_string = printColored(f"+{currency_symbol}{gain_loss:.2f}",config.gain_color) if gain_loss > 0 else printColored(f"(-{currency_symbol}{-gain_loss:.2f})",config.loss_color)
            average_gain_loss_string = printColored(f"+{currency_symbol}{average_gain_loss:.2f}",config.gain_color) if average_gain_loss > 0 else printColored(f"(-{currency_symbol}{-average_gain_loss:.2f})",config.loss_color)
            return_string = ""
            return_string += f"Sum: {currency_symbol}{total:.2f} ~ Avg: {currency_symbol}{average:.2f}"
            return_string += f" ~ Value: {currency_symbol}{total_value:.2f}  ({currency_symbol}{value:.2f} * {count})"
            return_string += f" ~ G/L: {gain_loss_string} ~ Avg G/L: {average_gain_loss_string}"
            return return_string
        return "N/A"


    # Adds the summary node to a coin object
    def __summarizePurchase(coin_id):
        try:
            coin = Coins.coins[coin_id]
            if isinstance(coin,Node):
                i = 0
                total = 0.0
                count = 0
                while i < len(coin.nodes):
                    node = coin.nodes[i]
                    if isinstance(node,Purchase):
                        total += node.price * node.quantity
                        count += node.quantity
                    elif isinstance(node,str):
                        del coin.nodes[i]
                        i-=1
                    i+=1
                coin.nodes.append(Coins.print_statistics(total,count,coin.data.value*coin.data.retention))

        except KeyError:
            pass
        return None
    
    def __summarizePurchases():
        for coin in Coins.owned:
            Coins.__summarizePurchase(coin)

    # Removes associated purchases from all defined coins
    def removePurchases():
        Coins.owned = set()
        Coins.not_owned = set()
        for coin_id in list(Coins.coins.keys()):
            coin = Coins.coins[coin_id]
            if isinstance(coin, Node):
                coin.nodes = []




    def buildTree(countries,denominations,values,coins,purchases=None,debug=False,show_only_owned=False, show_only_not_owned=False,only_coin_ids=False):
        if debug:
            for item in [(countries,"Countries"),(denominations,"Denominations"),(values,"Values"),(coins,"Coins")]:
                print(item[1])
                for key in item[0]:
                    print(f"  {key}:{item[0][key]}")
        if show_only_owned and show_only_not_owned:
            show_only_owned = False
            show_only_not_owned = False
        # Actually builds tree with given information
        current_countries = []
        for country in countries:
            country = countries[country]
            current_denominations = []
            for denomination in country[1]:
                denomination = denominations[denomination]
                current_values = []
                for value in denomination[1]:
                    value = values[value]
                    current_coins = []
                    for coin in value[1]:
                        try:
                            coin = coins[coin]
                        except KeyError:
                            continue
                        if not coin[1]:
                            continue
                        if only_coin_ids:
                            current_coins.append((Node(data=coin[1]),coin[0]))
                        else:
                            coin_id = coin[0]
                            # Links purchases as child nodes of the coin
                            current_coins.append(Node(data=coin[1]))
                            if purchases:
                                matches = [x for x in purchases if x[0] == coin_id]
                                if matches:
                                    if debug: # Prints out matched purchases if debugging
                                        print(f"Coin '{coin_id}' has purchases:")
                                    for match in matches:
                                        if debug:
                                            print(f"  {match}")
                                        current_coins[-1].nodes.append(Purchase(match[1],match[2],match[3],match[4],match[5]))
                        # Sorts the coins by first year available
                    if only_coin_ids:
                        current_coins = sorted(current_coins, key = lambda x: x[0].data.years[0])
                        current_coins = [x[1] for x in current_coins]
                    else:
                        current_coins = sorted(
                            current_coins, key=lambda x: x.data.years[0]
                        )
                    try: # converts name from decimal to integer if possible
                        value = (float(value[0]),value[1],value[2])
                        if value[0] - int(value[0]) < 0.1:
                            value = (int(value[0]),value[1],value[2])
                    except ValueError: # If name is string, append sorting number to end.
                        try:
                            value = (f"{value[0]} ({round(float(value[2]),2):.2f})",value[1],value[2])
                        except ValueError:
                            value = (f"{value[0]} ({value[2]})",value[1],value[2])
                    current_values.append((
                        Tree(name=printColored(str(value[0]).title(),config.value_color), nodes=current_coins),value[2]))
                    # Sorts the list of trees by sorting names
                    current_values = sorted(current_values,key = lambda x: x[1])
                # Then converts the list back to a list of trees
                current_values = [x[0] for x in current_values]
                # Appends denomination tree
                name = str(denomination[0]).title()
                color = config.denomination_color

                if denomination[2]:
                    name += config.bullion_hint
                    color = config.bullion_color
                current_denominations.append(
                    Tree(
                        name=printColored(name,color),
                        nodes=current_values,
                    )
                )

            # Sorts the denominations by name
            current_denominations = sorted(current_denominations, key = lambda x: str(x))
            # Appends country tree
            current_countries.append(
                Tree(
                    name=printColored(str(country[0]).title(),config.country_color), nodes=current_denominations
                )
            )
        # Sorts the countries by name
        current_countries = sorted(current_countries, key=lambda x: str(x))
        results = Tree(name="Results", nodes=current_countries)
        return results

    def linkPurchases(keep_old_purchases=False):
        if not keep_old_purchases:
            Coins.removePurchases()
        for purchase in purchases:
            try:
                coin = Coins.coins[purchase]
                if isinstance(coin, Node):
                    coin.nodes += purchases[purchase]
                    Coins.owned.add(purchase)
            except KeyError:
                print(f"{purchase} is not a valid key")
        Coins.owned = set(Coins.owned)
        Coins.not_owned = set(Coins.coins.keys())
        Coins.not_owned = Coins.not_owned - Coins.owned
        Coins.__summarizePurchases()

    def build(entries,prices=None,purchases=None,debug=False, show_only_bullion=False, show_only_not_bullion=False,show_only_owned=False, show_only_not_owned=False,hide_coins=False, only_coin_ids=False):
        if not isinstance(entries,list):
            entries = [entries]
        if show_only_bullion and show_only_not_bullion:
            show_only_bullion = False
            show_only_not_bullion = False
        coins = {}
        values = {}
        denominations = {}
        countries = {}
        for entry in entries:
            if show_only_bullion and not entry[14]:
                continue
            if show_only_not_bullion and entry[14]:
                continue
            coins[entry[0]] = (entry[0],None)
            if not hide_coins:
                coins[entry[0]]=(coins[entry[0]][0],CoinData(
                        weight=entry[1],
                        fineness=entry[2],
                        precious_metal_weight=entry[3],
                        years=entry[4],
                        metal = entry[5],
                        nickname = entry[6]
                    ))
            if coins[entry[0]][1] is not None:
                if prices is not None:
                    Coins.price(prices[0],prices[1],prices[2],prices[3],coins[entry[0]][1])
                else:
                    coins[entry[0]][1].togglePrice(False)
            try:
                values[entry[7]]
            except KeyError:
                # Display name, child coins, sorting number
                values[entry[7]] = (entry[9] if entry[9] else entry[8],[],entry[8])
            if entry[0] not in values[entry[7]][1]:
                values[entry[7]][1].append(entry[0])
            try:
                denominations[entry[10]]
            except KeyError:
                # Display name, child values, bullion tag
                denominations[entry[10]] = (entry[11],[],entry[14])
            if entry[7] not in denominations[entry[10]][1]:
                denominations[entry[10]][1].append(entry[7])
            try:
                countries[entry[12]]
            except KeyError:
                countries[entry[12]] = (entry[13],[])
            if entry[10] not in countries[entry[12]][1]:
                countries[entry[12]][1].append(entry[10])
            

        return Coins.buildTree(countries,denominations,values,coins,purchases=purchases,debug=debug,show_only_owned=show_only_owned, show_only_not_owned=show_only_not_owned,only_coin_ids=only_coin_ids)





    def search(country=None,denomination=None,face_value=None,face_value_name=None,year=None,debug=False):
        base_query = """
        select coins.coin_id,coins.gross_weight,coins.fineness,coins.precious_metal_weight,coins.years,coins.metal,coins.name,face_values.value_id,face_values.value,face_values.name,denominations.denomination_id,denominations.name,countries.country_id,countries.name,tags.bullion from coins inner join face_values on coins.face_value_id = face_values.value_id inner join denominations on face_values.denomination_id = denominations.denomination_id inner join countries on denominations.country_id = countries.country_id inner join tags on denominations.tags = tags.tag_id
        """
        found_first_specifier = False
        country_query = ""
        denomination_query = ""
        value_name_query = ""
        value_query = ""
        year_query = ""
        queries = [(country_query,country,"countries"),(denomination_query,denomination,"denominations"),(value_name_query,face_value_name,"face_values")]
        for i in range(len(queries)):
            item = queries[i]
            if item[1] is not None:
                queries[i] = (f"""
                (
                    {item[2]}.name like ? or
                    {item[2]}.alternative_name_1 like ? or
                    {item[2]}.alternative_name_2 like ? or
                    {item[2]}.alternative_name_3 like ? or
                    {item[2]}.alternative_name_4 like ? or
                    {item[2]}.alternative_name_5 like ?
                )
                """,item[1])
                if found_first_specifier:
                    queries[i]=(f"AND {queries[i][0]}",item[1])
                found_first_specifier = True

        # Adds specifier for actual value
        if face_value:
            queries.append((value_query,face_value,1))
            queries[-1] = ("    face_values.value=?",queries[-1][1],queries[-1][2])
            if found_first_specifier:
                queries[-1] = (f"\nAND\n  {queries[-1][0].strip()}",queries[-1][1],queries[-1][2])
            found_first_specifier = True

        # Adds specifier for actual value
        if year:
            queries.append((year_query,f"%{year}%",1))
            queries[-1] = ("    coins.years like ?",queries[-1][1],queries[-1][2])
            if found_first_specifier:
                queries[-1] = (f"\nAND\n  {queries[-1][0].strip()}",queries[-1][1],queries[-1][2])
            found_first_specifier = True

        return_query = base_query
        variables = []
        if country is not None or denomination is not None or face_value is not None or year is not None:
            return_query += " where "
            for item in queries:
                if item[0]:
                    return_query += item[0]
                    repetitions = 6
                    if len(item) == 3:
                        repetitions = item[2]
                    for _ in range(repetitions):
                        variables.append(item[1])
        if debug:
            print("-----------------------------------")
            print(f"Query:\n{return_query}")
            print(f"Variables:\n{variables}")
            print("-----------------------------------")

        return (f"{return_query};",tuple(variables))
    """
    def search(
        country=None, denomination=None, face_value=None, year=None, debug=False, show_only_owned=False, show_only_not_owned=False, show_only_bullion=False, show_only_not_bullion=False, hide_coins=False, only_coin_ids=False
    ):
        found_denominations = list(Coins.denominations.keys())
        if country:
            country = validCountry(country)
            if country:
                country = country.replace(" ","_")
                try:
                    found_denominations = Coins.countries[country.lower()]
                except KeyError:
                    return None
            else:
                return None

        if debug:
            print("Denominations found:")
            for item in found_denominations:
                print(f"  {item}")

        found_values = []
        if denomination:
            matches = []
            for x in found_denominations:
                test = Coins.denominations[x].name
                if isinstance(test,AlternativeNames):
                    temp = test.lookup(denomination)
                    if temp:
                        matches.append(x)
                elif test.lower() == denomination.lower():
                    matches.append(x)
            if matches:
                for match in matches:
                    try:
                        found_values += Coins.denominations[match]
                    except KeyError:
                        continue
            else:
                return None
        else:
            for denom in found_denominations:
                found_values += Coins.denominations[denom]

        if debug:
            print("Values found:")
            for item in found_values:
                print(f"  {item}")

        found_coins = []
        if face_value:
            matches = []
            for x in found_values:
                test = Coins.values[x].name
                if isinstance(test,AlternativeNames):
                    temp = test.lookup(face_value)
                    if temp:
                        matches.append(x)
                else:
                    if str(test).lower() == str(face_value).lower():
                        matches.append(x)
            if debug:
                print("Pruned values found:")
                for item in matches:
                    print(f"  {item}")
            if matches:
                for match in matches:
                    try:
                        found_coins += Coins.values[match]
                    except KeyError:
                        continue
            else:
                return None
        else:
            for value in found_values:
                found_coins += Coins.values[value]

        if debug:
            print("Coins found:")
            for item in found_coins:
                print(f"  {item}")

        results = []
        if year:
            matches = [
                x
                for x in found_coins
                if year
                in (
                    Coins.coins[x].years
                    if isinstance(Coins.coins[x], CoinData)
                    else Coins.coins[x].data.years
                )
            ]
            if matches:
                for match in matches:
                    try:
                        results += [match]
                    except KeyError:
                        continue
            else:
                return None
        else:
            results = found_coins

        if debug:
            print("Results:")
            for item in results:
                print(f"  {item}")

        return Coins.buildTree(results, debug, show_only_owned, show_only_not_owned, show_only_bullion, show_only_not_bullion, hide_coins, only_coin_ids)
    """
