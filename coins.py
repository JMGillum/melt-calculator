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


    # Returns a tree object for a collection of countries, their denominations, their values, and their coins
    def BuildTree(
        countries:list[tuple],
        denominations:list[tuple],
        values:list[tuple],
        coins:list[tuple],
        purchases:list[Purchase]=None,
        debug:bool=False,
        only_coin_ids:bool=False,
        config:dict={},
    ):
        if debug:
            for item in [
                (countries, "Countries"),
                (denominations, "Denominations"),
                (values, "Values"),
                (coins, "Coins"),
            ]:
                print(item[1])
                for key in item[0]:
                    print(f"  {key}:{item[0][key]}")
        # Actually builds tree with given information
        current_countries = []
        for country in countries:
            country = countries[country]
            current_denominations = []
            for denomination in country[1]:
                try:
                    denomination = denominations[denomination]
                except KeyError:
                    continue
                current_values = []
                for value in denomination[1]:
                    try:
                        value = values[value]
                    except KeyError:
                        continue
                    current_coins = []
                    for coin in value[1]:
                        try:
                            coin = coins[coin]
                        except KeyError:
                            continue
                        if not coin[1]:
                            continue
                        if only_coin_ids:
                            current_coins.append((Node(data=coin[1]), coin[0]))
                        else:
                            coin_id = coin[0]
                            # Links purchases as child nodes of the coin
                            current_coins.append(Node(data=coin[1]))
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
                                        current_coins[-1].nodes.append(
                                            Purchase(
                                                *(match[1:4] + match[5:]),
                                                config["date_format"],
                                                config["currency_symbol"],
                                                config["show_color"],
                                                config["colors_8_bit"],
                                                config["types_colors"]["purchase"],
                                            )
                                        )
                                    Coins.__SummarizePurchase(current_coins[-1], config)
                        # Sorts the coins by first year available
                    if only_coin_ids:
                        current_coins = sorted(
                            current_coins, key=lambda x: x[0].data.years[0]
                        )
                        current_coins = [x[1] for x in current_coins]
                    else:
                        current_coins = sorted(
                            current_coins, key=lambda x: x.data.years[0]
                        )
                    try:  # converts name from decimal to integer if possible
                        value = (float(value[0]), value[1], value[2])
                        if value[0] - int(value[0]) < 0.1:
                            value = (int(value[0]), value[1], value[2])
                    except (
                        ValueError
                    ):  # If name is string, append sorting number to end.
                        try:
                            value = (
                                f"{value[0]} ({round(float(value[2]), 2):.2f})",
                                value[1],
                                value[2],
                            )
                        except ValueError:
                            value = (f"{value[0]} ({value[2]})", value[1], value[2])
                    current_values.append(
                        (
                            Tree(
                                name=Colors.PrintColored(
                                    str(value[0]).title(),
                                    config["show_color"],
                                    config["colors_8_bit"],
                                    config["types_colors"]["value"],
                                ),
                                nodes=current_coins,
                            ),
                            value[2],
                        )
                    )
                    # Sorts the list of trees by sorting names
                    current_values = sorted(current_values, key=lambda x: x[1])
                # Then converts the list back to a list of trees
                current_values = [x[0] for x in current_values]
                # Appends denomination tree
                name = str(denomination[0]).title()
                color = config["types_colors"]["denomination"]

                if denomination[2]:
                    name += config["bullion_hint"]
                    color = config["tags_colors"]["bullion"]
                current_denominations.append(
                    Tree(
                        name=Colors.PrintColored(
                            name, config["show_color"], config["colors_8_bit"], color
                        ),
                        nodes=current_values,
                    )
                )

            # Sorts the denominations by name
            current_denominations = sorted(current_denominations, key=lambda x: str(x))
            # Appends country tree
            current_countries.append(
                Tree(
                    name=Colors.PrintColored(
                        str(country[0]).title(),
                        config["show_color"],
                        config["colors_8_bit"],
                        config["types_colors"]["country"],
                    ),
                    nodes=current_denominations,
                )
            )
        # Sorts the countries by name
        current_countries = sorted(current_countries, key=lambda x: str(x))
        results = Tree(name="Results", nodes=current_countries)
        return results


    def __SetupCoin(entry,mapping,coins,prices,config):

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

        coin = CoinData(**coin_specs)
        if coin is None:
            raise ValueError

        # (Coin id of coin, CoinData object of coin)
        coins[entry[mapping["coin_id"]]] = (
            coins[entry[mapping["coin_id"]]][0],
            coin
        )

        if coin is not None:
            # Metal prices exist
            if prices:
                Coins.Price(coins[entry[mapping["coin_id"]]][1], prices)

            # No metal prices exist, so don't display prices.
            else:
                coins[entry[mapping["coin_id"]]][1].togglePrice(False)



    def __SetupValue(entry,mapping,values):
        try:
            values[entry[mapping["value_id"]]]
        except KeyError:
            # Display name, child coins, sorting number
            values[entry[mapping["value_id"]]] = (
                entry[mapping["value_display_name"]]
                if entry[mapping["value_display_name"]]
                else entry[mapping["value"]],
                [],
                entry[mapping["value"]],
            )
        if (
            entry[mapping["coin_id"]]
            not in values[entry[mapping["value_id"]]][1]
        ):
            values[entry[mapping["value_id"]]][1].append(
                entry[mapping["coin_id"]]
            )


    def __SetupDenomination(entry,mapping,denominations):

        # Creates entry for this denomination if it is the first time encountering it.
        try:
            denominations[entry[mapping["denomination_id"]]]
        except KeyError:
            # Display name, child values, bullion tag
            denominations[entry[mapping["denomination_id"]]] = (
                entry[mapping["denomination_display_name"]],
                [],
                entry[mapping["tag_bullion"]],
            )

        # Associates value_id with this denomination if it isn't already
        if (
            entry[mapping["value_id"]]
            not in denominations[entry[mapping["denomination_id"]]][1]
        ):
            denominations[entry[mapping["denomination_id"]]][1].append(
                entry[mapping["value_id"]]
            )


    def __SetupCountry(entry,mapping,countries):

        # Creates entry for this country if it is the first time encountering it.
        try:
            countries[entry[mapping["country_id"]]]
        except KeyError:
            countries[entry[mapping["country_id"]]] = (
                entry[mapping["country_display_name"]],
                [],
            )

        # Associates denomination_id with this country if it isn't already
        if (
            entry[mapping["denomination_id"]]
            not in countries[entry[mapping["country_id"]]][1]
        ):
            countries[entry[mapping["country_id"]]][1].append(
                entry[mapping["denomination_id"]]
            )

    def __SetupCoin2(entry,mapping,prices,config,show_id=False):

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

    def Sort(root):
        countries = [(x[0],str(x[1])) for x in root]
        countries = sorted(countries, key=lambda x: x[1])
        root.set_display_order([x[0] for x in countries])

        for _,country in root:

            denominations = [(x[0],str(x[1])) for x in country]
            denominations = sorted(denominations, key=lambda x: x[1])
            country.set_display_order([x[0] for x in denominations])

            # Sort Values
            for _,denomination in country:

                values = []
                for key,val in denomination:
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
                values = sorted(values, key=lambda x: x[1])
                denomination.set_display_order([x[0] for x in values])

                # Sorts coins
                for _,value in denomination:
                    coins = [(x[0],x[1].data.years[0]) for x in value]
                    coins = sorted(
                        coins, key=lambda x: x[1], reverse=True
                    )
                    value.set_display_order([x[0] for x in coins])

                    for _,coin in value:
                        purchases = []
                        extras = []
                        for key,val in coin:
                            if isinstance(val,Purchase):
                                purchases.append((key,val.purchase_date))
                            else:
                                extras.append(key)

                        purchases = sorted(purchases, key=lambda x: x[1])
                        purchases = [x[0] for x in purchases] + extras
                        coin.set_display_order(purchases)
                        print(coin.nodes)
        

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
        do_not_build_tree=False,
    ):

        if not isinstance(entries, list):
            entries = [entries]
        if show_only_bullion and show_only_not_bullion:
            show_only_bullion = False
            show_only_not_bullion = False
        coins = {}
        values = {}
        denominations = {}
        countries = {}

        tree_root = Tree(nodes={})
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
            coin = Coins.__SetupCoin2(entry,mapping,prices,config,only_coin_ids)

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
                        #value_name = f"{entry[mapping["value_display_name"]]} ({round(float(entry[mapping["value"]]),2):.2f})" if entry[mapping["value_display_name"]] else entry[mapping["value"]]
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

            


            # Default values in case it is not updated in future.
            coins[entry[mapping["coin_id"]]] = (
                entry[mapping["coin_id"]],
                None,
            )  # (coin_id, CoinData object)

            # Sets up denomination information if needed
            if not hide_denominations:

                # Sets up value information if needed
                if not hide_values:

                    # Creates CoinData object and prices it if necessary
                    if not hide_coins:
                        Coins.__SetupCoin(entry,mapping,coins,prices,config)

                    Coins.__SetupValue(entry,mapping,values)

                Coins.__SetupDenomination(entry,mapping,denominations)

            Coins.__SetupCountry(entry,mapping,countries)

                    
        Coins.Sort(tree_root)
        for line in tree_root.print():
            print(line)

        return tree_root

        if do_not_build_tree:
            return (countries, denominations, values, coins)

        # Creates the tree display of results
        return Coins.BuildTree(
            countries,
            denominations,
            values,
            coins,
            purchases=purchases,
            debug=debug,
            only_coin_ids=only_coin_ids,
            config=config,
        )

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
