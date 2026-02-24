#   Author: Josh Gillum              .
#   Date: 23 February 2026           ":"         __ __
#                                  __|___       \ V /
#                                .'      '.      | |
#                                |  O       \____/  |
# ~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
#
#    This file stores the Coins class, which provides an interface for
#    interacting with the database that stores the coin information.
#
#    Thie class has no functions for actually getting data. It simply turns
#    data from the database into CoinData objects and builds a tree to represent
#    them.
#
#    See db_interface.py and queries.py for database specific functions.
#
# ~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

from coinData import CoinData, Purchase, PurchaseStats, Value, Denomination, Country
from tree.tree import Tree
from tree.node import Node
from colors import Colors
import treasure.text

import re


class Coins:
    """Container class for various functions related to displaying coins."""

    def Price(coin:CoinData, prices:dict):
        """ Calculates the value of the coin object, using the provided precious metal values

        Args:
            coin: The coin that will be priced.
            prices: dictionary of metals. Each key should be the key for the metal, as used by the CoinData object. Each value should be a tuple of (name, price)
        """

        try:
            spot = prices[coin.metal][1]
            coin.value = coin.precious_metal_weight.AsTroyOunces() * spot
            coin.TogglePrice(True)

        # The metal defined in the coin is not in the prices dict
        except KeyError:
            coin.value = -1

    def __GainOrLossString(value:float, config:dict, round_to_places:int=2):
        """ Generates a string depicting a price change

        Args:
            value: The change in price that will generate the string
            config: Must have 'currency_symbol' as a string, 'show_color' as bool, 'colors_8_bit' as bool, and 'misc_colors'['gain'] and 'misc_colors'['loss'] defined.
            round_to_places: Number of places to round value to. Pass 0 or None to perform no rounding.

        Returns: A formatted string with colored output (if appropriate as determined by config)
            
        """

        # Gain
        if round_to_places is not None and round_to_places > 0:
            value = round(value,round_to_places)
        string_to_print = f"{value}"
        color = None
        if value > 0:
            string_to_print = f"+{config['currency_symbol']}{value:.2f}"
            color = config["misc_colors"]["gain"]

        # Loss
        elif value < 0:
            string_to_print = f"-{config['currency_symbol']}{-value:.2f}"
            color = config["misc_colors"]["loss"]

        # No change
        else:
            return f"{value}"

        return Colors.PrintColored(
            string_to_print,
            config["show_color"],
            config["colors_8_bit"],
            color
        )

    def PrintStatistics(
        config: dict,
        total: float = 0.0,
        count: int = 0,
        value: float = 0.0,
        other_value: float = 0.0,
        stats: PurchaseStats = None,
    ):
        """ Prints summary statistics for a group of purchases (really just a total, count, and worth)

        Args:
            config: Requires 'currency_symbol' to be set. Passed to __GainOrLossString, so there may be extra requirements.
            total: Stores the total value
            count: Stores the number of items counted to arrive at the total
            value: Stores the value to compare total to.
            other_value: Stores a second value to compare total to
            stats: Can be used in place of total, count, value, and other_value.

        Returns: String of the summary statistics.
            
        """

        # Uses the stats variable if present
        if stats and isinstance(stats, PurchaseStats):
            total = stats.total
            count = int(stats.count)
            if count > 0:
                value = (stats.total + stats.delta) / stats.count
            if count > 0:
                other_value = (stats.total + stats.delta2) / stats.count

        if count > 0:
            total_value = value * count
            other_total_value = other_value * count
            average = total / count

            # Calculates deltas
            gain_loss = total_value - total
            other_gain_loss = other_total_value - total
            average_gain_loss = value - average
            other_average_gain_loss = other_value - average

            # Creates strings
            gain_loss_string = Coins.__GainOrLossString(gain_loss, config)
            average_gain_loss_string = Coins.__GainOrLossString(
                average_gain_loss, config
            )
            other_gain_loss_string = Coins.__GainOrLossString(other_gain_loss, config)
            other_average_gain_loss_string = Coins.__GainOrLossString(
                other_average_gain_loss, config
            )
            return_string = ""
            return_string += f"[Count:{count}] [Sum:{config['currency_symbol']}{total:.2f}] [Avg:{config['currency_symbol']}{average:.2f}]"
            return_string += f" [Value:{config['currency_symbol']}{total_value:.2f}/{config['currency_symbol']}{other_total_value:.2f}]"
            return_string += f" [G/L:{gain_loss_string}/{other_gain_loss_string}] [Avg G/L:{average_gain_loss_string}/{other_average_gain_loss_string}]"
            return return_string
        return "N/A"

    # Adds the summary node to a coin object
    def __SummarizePurchase(coin:Node, config:dict):
        """ Calculates statistics for all purchases of a coin, then prints them.

        Args:
            coin: The coin to summarize the purchases for. Purchases to be summarized must be within the nodes attribute.
            config: Passed to PrintStatistics, so any requirements for that are needed.

        """
        if isinstance(coin, Node):
            i = 0
            total = 0.0
            count = 0

            # Adds each purchase to summary statistics
            while i < len(coin.nodes):
                node = coin.nodes[i]
                if isinstance(node, Purchase):
                    total += node.price * node.quantity
                    count += node.quantity

                # Removes unused strings. Unsure of purpose. Perhaps if a purchase 
                # was mistakenly added as a string instead of a Purchase object.
                elif isinstance(node, str):
                    del coin.nodes[i]
                    i -= 1
                i += 1

            # Appends the summary string after all of the Purchase objects.
            coin.nodes.append(
                Coins.PrintStatistics(
                    config,
                    total,
                    count,
                    coin.data.value,
                    coin.data.value * coin.data.retention,
                )
            )


    def __SetupCoin(entry:list|tuple,mapping:dict,prices:dict,config:dict,show_id:bool=False):

        """ Creates a CoinData object and prices it, if needed.

        Args:
            entry: Individual row returned from database
            mapping: Maps keys to indices in entry
            prices: Stores metal prices
            config: Config options, passed to CoinData.__init__()
            show_id: Whether to pass the coin_id to CoinData.__init__()

        Returns: The created CoinDate object
            
        """
        # Information to pass to CoinData.__init__()
        coin_specs = {
            "weight": entry[mapping["gross_weight"]],
            "fineness": entry[mapping["fineness"]],
            "precious_metal_weight": entry[
                mapping["precious_metal_weight"]
            ],
            "years": entry[mapping["years"]],
            "metal": entry[mapping["metal"]],
            "nickname": entry[mapping["coin_display_name"]],
            "config": config,
        }

        # Passes the coin_id to be displayed by the CoinData object
        if show_id:
            coin_specs |= {"coin_id":entry[mapping["coin_id"]]}

        coin = CoinData(**coin_specs)
        if coin is None:
            raise ValueError

        # Metal prices exist
        if prices:
            Coins.Price(coin, prices)

        # No metal prices exist, so don't display prices.
        else:
            coin.togglePrice(False)
        return coin

    def __RecursiveSetupTree(parent_tree:Tree|Node,keys:list[str]):
        """ Ensures that the arbitrary depth Tree object exists.
        Recursively traverses the tree, creating new nodes if they don't exist.
        Functions similarly to `mkdir -p a/b/c`.

        ex: keys= ["a","b","c"]
        Creates the tree:
        root -> "a" -> "b" -> "c"

        Args:
            parent_tree: The tree object to search for the key within
            keys: Each key specifies one level down in the tree structure. The first
            element is searched for in the current level. Then the function traverses one level
            down with the first key popped off.

        Returns: Tuple containing every Tree object along the specified
            
        """

        # return condition
        if len(keys) == 0:
            return

        # Looks for key within current tree's nodes
        current_tree = parent_tree.search(keys[0])
        val = (current_tree,True)

        # Key was not within current tree's nodes
        if current_tree is None:

            # Add new Tree object at key index in current tree's nodes
            current_tree = parent_tree.add_node(Tree(nodes={}),keys[0])
            val = (current_tree,False)

        # Recursively traverse deeper
        result = Coins.__RecursiveSetupTree(current_tree,keys[1:])

        # Returns tuple (level1, level2, level3, ...)
        if result is None:
            return (val,)
        else:
            return (val,*result)

    def __NameElement(tree:Tree,existed:bool,name:str):
        """ Sets the name of the tree if existed is True, otherwise does nothing

        Args:
            existed: Whether to set the name of the tree or not
            name: The name of which tree.name will be set to. Only does something if existed is True 

        Returns: tree
            
        """

        if not existed:
            tree.set_name(name)
        return tree

    def __ParseSortString(string:str,separator:str="|",default_method:str=None,default_direction:str="asc"):
        """ Sort strings are of the format <method><separator><direction>. Parses and extracts elements from this.

        Args:
            string: The string to parse
            separator: The character that separates method from direction
            default_method: What to return for the method if an error occured
            default_direction: What to return for the direction if an error occured

        Returns: (method, direction), both as strings
            
        """

        if string is None:
            return default_method, default_direction
        vals = string.split(separator)

        # Invalid format
        if len(vals) != 2:
            return default_method, default_direction
        else:
            # Converts method to lower
            vals[0] = str(vals[0]).lower()
            vals[1] = str(vals[1])
            
            # Direction must be some form of ascend or descend
            if vals[1].lower() == "asc" or vals[1].lower() == "ascend" or vals[1].lower() == "ascending":
                vals[1] = "asc"
            elif vals[1].lower() == "desc" or vals[1].lower() == "descend" or vals[1].lower() == "descending":
                vals[1] = "desc"

            # Direction is some other value. Use default
            else:
                vals[1] = default_direction

            return vals[0], vals[1]

            
    def __SortBasic(tree:Tree, sort_string:str):
        """ Sorts basic tree structures. Can only sort off of what each node cast to str returns.
        Sorting only occurs at this level. Does not sort deeper.

        Args:
            tree: The tree to sort the nodes of.
            sort_string: Formatted sort string of <method>|<direction>. See Coins.__ParseSortString()
        """

        method, direction = Coins.__ParseSortString(sort_string)
        if method is not None:
            direction = True if direction == "desc" else False

            # Sorts alphabetically by name
            if method == "name":
                keys = [(x[0],str(x[1])) for x in tree]
                keys = sorted(keys, key=lambda x: x[1], reverse=direction)
                tree.set_display_order([x[0] for x in keys])


    def __SortValues(tree:Tree, sort_string:str):
        """ Sorts a tree with nodes of Value objects.
        Sorting only occurs at this level. Does not sort deeper.

        Args:
            tree: The tree to sort the nodes of.
            sort_string: Formatted sort string of <method>|<direction>. See Coins.__ParseSortString()
        """

        method, direction = Coins.__ParseSortString(sort_string)
        if method is not None:
            direction = True if direction == "desc" else False

            # Sorts numerically by value
            if method == "value":
                values = []
                for key,val in tree:
                    val = val.name
                    value = None
                
                    # Attempts to convert value to an integer
                    try:  
                        value = float(val)

                        # Checks if float value is very close to a whole number. If so,
                        # truncate it.
                        if value - int(value) < 0.1:
                            value = int(value)

                        values.append((key,value))

                    # If value is a string, search within final parentheses for its numeric value
                    except ValueError:
                        try:
                            start = val.rfind("(")
                            end = val.rfind(")",start)

                            # Value is within last () in str
                            value = round(float(val[start+1:end]), 2)
                        except ValueError:
                            value = val
                        values.append((key,value))

                values = sorted(values, key=lambda x: x[1], reverse=direction)
                tree.set_display_order([x[0] for x in values])

    def __SortCoins(tree:Tree, sort_string:str):
        """ Sorts a tree with nodes of CoinData objects.
        Sorting only occurs at this level. Does not sort deeper.

        Args:
            tree: The tree to sort the nodes of.
            sort_string: Formatted sort string of <method>|<direction>. See Coins.__ParseSortString()
        """

        method, direction = Coins.__ParseSortString(sort_string)
        if method is not None:
            direction = True if direction == "desc" else False

            # Sorts by first year the coin was made
            if method == "year":
                coins = [(x[0],x[1].data.years[0]) for x in tree]
                coins = sorted(
                    coins, key=lambda x: x[1], reverse=direction
                )
                tree.set_display_order([x[0] for x in coins])


    def __SortPurchases(tree,sort_string):
        """ Sorts a tree with nodes of Purchase objects.
        Sorting only occurs at this level. Does not sort deeper.

        Args:
            tree: The tree to sort the nodes of.
            sort_string: Formatted sort string of <method>|<direction>. See Coins.__ParseSortString()
        """

        method, direction = Coins.__ParseSortString(sort_string)
        if method is not None:
            direction = True if direction == "desc" else False

            # Sorts by the date of the purchase
            if method == "date":
                purchases = []
                extras = []
                for key,val in tree:
                    if isinstance(val,Purchase):
                        purchases.append((key,val.purchase_date))
                    else:
                        extras.append(key)

                purchases = sorted(purchases, key=lambda x: x[1], reverse=direction)
                purchases = [x[0] for x in purchases] + extras
                tree.set_display_order(purchases)


    def Sort(
        root, 
        sort_countries:str="name|asc", 
        sort_denominations:str="name|asc", 
        sort_values:str="value|asc", 
        sort_coins:str="year|asc", 
        sort_purchases:str="date|asc"
    ):

        """ Sorts a Tree with levels of country -> denomination -> value -> coin -> purchase

        Args:
            sort_countries: str to pass to Coins.__SortBasic()
            sort_denominations: formatted sort str to pass to Coins.__SortBasic()
            sort_values: formatted sort str to pass to Coins.__SortValues()
            sort_coins: formatted sort str to pass to Coins.__SortCoins()
            sort_purchases: formatted sort str to pass to Coins.__SortPurchases()
        """
        if sort_countries is not None:
            Coins.__SortBasic(root,sort_countries)

        for _,country in root:

            if sort_denominations is not None:
                Coins.__SortBasic(country,sort_denominations)

            # Sort Values
            for _,denomination in country:

                if sort_values is not None:
                    Coins.__SortValues(denomination,sort_values)

                # Sorts coins
                for _,value in denomination:
                    Coins.__SortCoins(value,sort_coins)

                    # Sorts Purchases
                    for _,coin in value:
                        Coins.__SortPurchases(coin,sort_purchases)
        

    # Given a set of coins, Fills out dictionaries that can be easily turned into a tree structure
    def Build(
        entries:list|tuple,
        mapping:dict,
        config:dict={},
        prices:dict=None,
        purchases:list|tuple=None,
        debug:bool=False,
        show_only_bullion:bool=False,
        show_only_not_bullion:bool=False,
        hide_coins:bool=False,
        hide_values:bool=False,
        hide_denominations:bool=False,
        show_coin_ids:bool=False,
        sorting_methods:dict={},
    ):

        """ Given a list of rows, create a tree structure to display them.

        Args:
            entries: Rows from the database. This is the data that will be represented in the tree
            mapping: Maps keywords to indices in entries.
            config: Passed to CoinData.__init__()
            prices: Stores metal prices
            purchases: Stores purchases
            debug: Pass True to enable extra printing
            show_only_bullion: Pass True to display only denominations with the Bullion tag
            show_only_not_bullion: Pass True to display only denominations without the Bullion tag
            hide_coins: Will not include any coins in the output.
            hide_values: Will not include any values or coins in the output.
            hide_denominations: Will not include any denominations, values, or coins in the output.
            show_coin_ids: Sends the coin's coin_id to the CoinData object to be displayed.
            sorting_methods: Unpacked as the args to Coins.__Sort()

        Returns: A Tree object representing all of the data stored within entries.
            
        """
        if not isinstance(entries, list):
            entries = [entries]
        if show_only_bullion and show_only_not_bullion:
            show_only_bullion = False
            show_only_not_bullion = False

        tree_root = Tree(nodes={})

        # How many levels of the tree should be displayed
        tree_keys = ["country_id"]
        if not hide_denominations:
            tree_keys.append("denomination_id")

            if not hide_values:
                tree_keys.append("value_id")

                if not hide_coins:
                    tree_keys.append("coin_id")
        
        for entry in entries:

            # Checks bullion filters and skips entry if necessary
            # Should really be done in the search function, but that is a problem
            # for another day
            if show_only_bullion and not entry[mapping["tag_bullion"]]:
                continue
            if show_only_not_bullion and entry[mapping["tag_bullion"]]:
                continue

            coin_id = entry[mapping["coin_id"]]
            coin = Coins.__SetupCoin(entry,mapping,prices,config,show_coin_ids)

            vals = Coins.__RecursiveSetupTree(tree_root,[entry[mapping[x]] for x in tree_keys])

            # Show country
            if len(vals) > 0:
                country_tree = vals[0]
                country_name = Country(
                    entry[mapping["country_display_name"]],
                    config["show_color"],
                    config["colors_8_bit"],
                    config["types_colors"]["country"]
                )

                country_tree = Coins.__NameElement(*country_tree,country_name)

                # Show denomination
                if len(vals) > 1:
                    denomination_tree = vals[1]
                    denomination_name = Denomination(
                        entry[mapping["denomination_display_name"]],
                        config["show_color"],
                        config["colors_8_bit"],
                        config["types_colors"]["denomination"]
                    )
                    denomination_tree = Coins.__NameElement(*denomination_tree,denomination_name)

                    # Show value
                    if len(vals) > 2:
                        value_tree = vals[2]
                        value_name = Value(
                            entry[mapping["value"]],
                            entry[mapping["value_display_name"]],
                            config["show_color"],
                            config["colors_8_bit"],
                            config["types_colors"]["value"],
                        )
                        value_tree = Coins.__NameElement(*value_tree,value_name)


                        # Show coin
                        if len(vals) > 3:
                            coin_tree = Node(data=coin)
                            value_tree.nodes[coin_id] = coin_tree
                            if purchases:
                                matches = []
                                try:
                                    matches = purchases[coin_id]
                                except KeyError:
                                    pass
                                #matches = [x for x in purchases if x[0] == coin_id]

                                # Prints out matched purchases if debugging
                                if matches:
                                    if debug:
                                        print(f"Coin '{coin_id}' has purchases:")
                                        print(f"  {matches}")

                                    # Creates Purchase object and adds to coin tree
                                    coin_tree.nodes += matches
                                    Coins.__SummarizePurchase(coin_tree, config)

        Coins.Sort(tree_root,**sorting_methods)

        return tree_root


    def ParseSearchString(db, text: str, debug: bool = False, config:dict={}):
        """ Parses a string to extract the country name, denomination, year, face value, and face value's name.

        Args:
            text: The string to parse
            debug: Pass True to enable extra output.
            config: dictionary of config options

        Returns: Tuple storing (country_id, denomination_id, year, face_value_id, face value name)
            
        """

        # Regex finds all strings of digits
        numbers_matched = [
            x for x in re.findall(r"(((\d+(\s|\-))?\d+\/\d+)|(\d*\.\d+)|(\d+))", text)
        ]
        if debug:
            print(f"Numbers matched: {numbers_matched}")
        numbers = []
        for number in numbers_matched:
            test_num = None
            if number[1]:
                test_num = number[1]
            if number[4]:
                test_num = number[4]
            if test_num is not None:
                fail, result = treasure.text.FractionStrToNum(test_num)
                if not fail:
                    numbers.append((str(result), test_num))
            else:
                numbers.append(number[0])
        words = re.findall("[a-zA-Z]+", text)  # Same for words
        print(f"Numbers found: {numbers}")

        year = ""
        denomination = ""
        country = ""
        face_value = ""
        face_value_name = ""

        # If more than two numbers, picks year and denomination
        if len(numbers) >= 2:

            # Fractinal number
            if isinstance(numbers[0], tuple):
                if isinstance(numbers[1], tuple):
                    year = numbers[1][0]
                else:
                    year = numbers[1]
                face_value = numbers[0][0]
                face_value_name = numbers[0][1]
            elif isinstance(numbers[1], tuple):
                year = numbers[0]
                face_value = numbers[1][0]
                face_value_name = numbers[1][1]

            # Neither of the first two numbers are tuples (dont have fractional number)
            else:  
                if len(numbers[0]) != 4 and len(numbers[1]) == 4:
                    year = numbers[1]
                    face_value = numbers[0]
                else:
                    year = numbers[0]
                    face_value = numbers[1]

        # Only one number was found
        elif len(numbers) == 1:  
            if isinstance(numbers[0], tuple):
                face_value = numbers[0][0]
                face_value_name = numbers[0][1]
            else:

                # Checks if number is 4 digits (a year), then checks if within provided range
                if len(numbers[0]) == 4:  
                    temp = int(numbers[0])
                    if (
                        temp >= config["minimum_year"]
                        and temp <= config["current_year"]
                    ):
                        year = numbers[0]

                    # Number was not in acceptable range for year,
                    # so use as face value
                    else:  
                        face_value = numbers[0]

                # Number is less than four digits, so use as face value
                else:
                    face_value = numbers[0]

        # Sets the country name and denomination
        if len(words) > 0:

            # Attempts to find a country name in the string
            for word in words:
                temp = None

                # Check if word is a name associated with any country
                result = db.FetchCountryId(word)
                if result is not None and len(result) > 0:

                    # Fetches the official name to display for the country
                    temp = db.FetchCountryDisplayName(result[0][0])
                    if temp is not None and len(result) > 0:
                        temp = temp[0][0]
                if debug:
                    print(f"Found country name: {temp if temp else 'None'}")
                if temp is not None:
                    country = temp
                    # Removes the country name from list so it isn't considered a denomination.
                    words.remove(word)  
                    break

            # If any words are left after searching for country name, the first is the denomination
            if len(words) > 0:
                denomination = words[0]

        if debug:
            print(
                f"COUNTRY:{country},DENOMINATION:{denomination},YEAR:{year},FACE VALUE:{face_value},FACE VALUE NAME:{face_value_name}"
            )

        # Checks if the face value name is set and if it's first
        # character is a '.'
        if face_value_name and face_value_name.strip()[0] == ".":
            # Prepend a zero to the name. Ex: .0 -> 0.0
            face_value_name = "0" + face_value_name

        # Remove face value name if it is just a copy of the face value
        if face_value == face_value_name:
            face_value_name = None

        return (country, denomination, year, face_value, face_value_name)
