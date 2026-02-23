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


    def __SetupCoin(entry,mapping,prices,config,show_id=False):

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
        if show_id:
            coin_specs |= {"coin_id":entry[mapping["coin_id"]]}

        coin = CoinData(**coin_specs)
        if coin is None:
            raise ValueError

        else:
            # Metal prices exist
            if prices:
                Coins.Price(coin, prices)

            # No metal prices exist, so don't display prices.
            else:
                coin.togglePrice(False)
        return coin

    def __RecursiveSetupTree(parent_tree,keys):
        if len(keys) == 0:
            return
        current_tree = parent_tree.search(keys[0])
        val = (current_tree,True)
        if current_tree is None:
            current_tree = parent_tree.add_node(Tree(nodes={}),keys[0])
            val = (current_tree,False)
        result = Coins.__RecursiveSetupTree(current_tree,keys[1:])
        if result is None:
            return (val,)
        else:
            return (val,*result)

    def __NameElement(tree,existed,name):
        if not existed:
            tree.set_name(name)
        return tree

    def __ParseSortString(string,separator="|",default_method=None,default_direction="asc"):
        if string is None:
            return default_method, default_direction
        vals = string.split(separator)
        if len(vals) != 2:
            return default_method, default_direction
        else:
            vals[0] = str(vals[0]).lower()
            vals[1] = str(vals[1])
            if vals[1].lower() == "asc" or vals[1].lower() == "ascend" or vals[1].lower() == "ascending":
                vals[1] = "asc"
            elif vals[1].lower() == "desc" or vals[1].lower() == "descend" or vals[1].lower() == "descending":
                vals[1] = "desc"
            else:
                vals[1] = default_direction

            return vals[0], vals[1]

            
    def __SortBasic(tree, sort_string):
        method, direction = Coins.__ParseSortString(sort_string)
        if method is not None:
            direction = True if direction == "desc" else False
            if method == "name":
                keys = [(x[0],str(x[1])) for x in tree]
                keys = sorted(keys, key=lambda x: x[1], reverse=direction)
                tree.set_display_order([x[0] for x in keys])


    def __SortValues(tree, sort_string):
        method, direction = Coins.__ParseSortString(sort_string)
        if method is not None:
            direction = True if direction == "desc" else False
            if method == "value":
                values = []
                for key,val in tree:
                    val = val.name
                    value = None
                
                    try:  # converts name from decimal to integer if possible
                        value = float(val)
                        if value - int(value) < 0.1:
                            value = int(value)

                        values.append((key,value))

                    # If name is string, append sorting number to end.
                    except ValueError:
                        try:
                            start = val.rfind("(")
                            end = val.rfind(")",start)
                            value = round(float(val[start+1:end]), 2)
                        except ValueError:
                            value = val
                        values.append((key,value))
                values = sorted(values, key=lambda x: x[1], reverse=direction)
                tree.set_display_order([x[0] for x in values])

    def __SortCoins(tree, sort_string):
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
        method, direction = Coins.__ParseSortString(sort_string)
        if method is not None:
            direction = True if direction == "desc" else False

            # Sorts by first year the coin was made
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
        sort_countries="name|asc", 
        sort_denominations="name|asc", 
        sort_values="value|asc", 
        sort_coins="year|asc", 
        sort_purchases="date|asc"
    ):

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
        entries,
        mapping,
        config={},
        prices=None,
        purchases=None,
        debug=False,
        show_only_bullion=False,
        show_only_not_bullion=False,
        hide_coins=False,
        hide_values=False,
        hide_denominations=False,
        only_coin_ids=False,
        sorting_methods={},
    ):

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
            if show_only_bullion and not entry[mapping["tag_bullion"]]:
                continue
            if show_only_not_bullion and entry[mapping["tag_bullion"]]:
                continue


            coin_id = entry[mapping["coin_id"]]
            coin = Coins.__SetupCoin(entry,mapping,prices,config,only_coin_ids)

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
                                matches = [x for x in purchases if x[0] == coin_id]
                                if matches:
                                    if (
                                        debug
                                    ):  # Prints out matched purchases if debugging
                                        print(f"Coin '{coin_id}' has purchases:")
                                    for match in matches:
                                        if debug:
                                            print(f"  {match}")
                                        coin_tree.nodes.append(
                                            Purchase(
                                                *(match[1:4] + match[5:]),
                                                config["date_format"],
                                                config["currency_symbol"],
                                                config["show_color"],
                                                config["colors_8_bit"],
                                                config["types_colors"]["purchase"],
                                            )
                                        )
                                    Coins.__SummarizePurchase(coin_tree, config)

        Coins.Sort(tree_root,**sorting_methods)

        return tree_root

    # Parses a string into the four specifiers (country, denomination, year, and face value)
    # countries should be a list of tuples or lists. Each item of countries represents a
    # country. The first value in the item is the proper name and each subsequent value
    # is an alternative name
    def ParseSearchString(db, text: str, debug: bool = False, config={}):
        """Parses a string to extract the country's name, year, denomination, and face value"""

        # Regex finds all strings of digits
        numbers_matched = [
            x for x in re.findall(r"(((\d+(\s|\-))?\d+\/\d+)|(\d*\.\d+)|(\d+))", text)
        ]
        print(numbers_matched)
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
        print(numbers)

        year = ""
        denomination = ""
        country = ""
        face_value = ""
        face_value_name = ""
        # If more than two numbers, picks year and denomination
        if len(numbers) >= 2:
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
            else:  # Neither are tuples (dont have fractional number)
                if len(numbers[0]) != 4 and len(numbers[1]) == 4:
                    year = numbers[1]
                    face_value = numbers[0]
                else:
                    year = numbers[0]
                    face_value = numbers[1]
        elif len(numbers) == 1:  # Only one number found
            if isinstance(numbers[0], tuple):
                face_value = numbers[0][0]
                face_value_name = numbers[0][1]
            else:
                if (
                    len(numbers[0]) == 4
                ):  # Checks if number is 4 digits (a year), then checks if within provided range
                    temp = int(numbers[0])
                    if (
                        temp >= config["minimum_year"]
                        and temp <= config["current_year"]
                    ):
                        year = numbers[0]
                    else:  # If not, uses number as face value
                        face_value = numbers[0]
                else:
                    face_value = numbers[0]

        # Sets the country name and denomination
        if len(words) > 0:
            # Attempts to find a country name in the string
            for word in words:
                temp = None
                result = db.FetchCountryId(word)
                if result is not None and len(result) > 0:
                    temp = db.FetchCountryDisplayName(result[0][0])
                    if temp is not None and len(result) > 0:
                        temp = temp[0][0]
                if debug:
                    print(f"Found country name: {temp if temp else 'None'}")
                if temp is not None:
                    country = temp
                    words.remove(
                        word
                    )  # Removes the country name from list so it isn't considered a denomination.
                    break
            # If any words are left after searching for country name, the first is the denomination
            if len(words) > 0:
                denomination = words[0]

        if debug:
            print(
                f"COUNTRY:{country},DENOMINATION:{denomination},YEAR:{year},FACE VALUE:{face_value},FACE VALUE NAME:{face_value_name}"
            )

        if face_value_name and face_value_name.strip()[0] == ".":
            face_value_name = "0" + face_value_name
        if face_value == face_value_name:
            face_value_name = None
        return (country, denomination, year, face_value, face_value_name)
