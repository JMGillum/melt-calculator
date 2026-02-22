#   Author: Josh Gillum              .
#   Date: 7 February 2026           ":"         __ __
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

from coinData import CoinData, Purchase, PurchaseStats
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

    def __gainOrLossString(value:float, config:dict):
        """ Generates a string depicting a price change

        Args:
            value: The change in price that will generate the string
            config: Must have 'currency_symbol' as a string, 'show_color' as bool, 'colors_8_bit' as bool, and 'misc_colors'['gain'] and 'misc_colors'['loss'] defined.

        Returns: A formatted string with colored output (if appropriate as determined by config)
            
        """

        # Gain
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

    # Prints summary statistics for a group of purchases (really just a total,count and worth)
    def PrintStatistics(
        config: dict,
        total: float = 0.0,
        count: int = 0,
        value: float = 0.0,
        other_value: float = 0.0,
        stats: PurchaseStats = None,
    ):
        if stats and isinstance(stats, PurchaseStats):
            total = round(stats.total, 2)
            count = int(stats.count)
            if count > 0:
                value = round((stats.total + stats.delta) / stats.count, 2)
            if count > 0:
                other_value = round((stats.total + stats.delta2) / stats.count, 2)
        else:
            total = round(total, 2)
            count = int(count)
            value = round(value, 2)
            other_value = round(other_value, 2)
        if count > 0:
            total_value = round(value * count, 2)
            other_total_value = round(other_value * count, 2)
            average = round(total / count, 2)
            gain_loss = round(total_value - total, 2)
            other_gain_loss = round(other_total_value - total, 2)
            average_gain_loss = round(value - average, 2)
            other_average_gain_loss = round(other_value - average, 2)
            gain_loss_string = Coins.__gainOrLossString(gain_loss, config)
            average_gain_loss_string = Coins.__gainOrLossString(
                average_gain_loss, config
            )
            other_gain_loss_string = Coins.__gainOrLossString(other_gain_loss, config)
            other_average_gain_loss_string = Coins.__gainOrLossString(
                other_average_gain_loss, config
            )
            return_string = ""
            return_string += f"[Count:{count}] [Sum:{config['currency_symbol']}{total:.2f}] [Avg:{config['currency_symbol']}{average:.2f}]"
            return_string += f" [Value:{config['currency_symbol']}{total_value:.2f}/{config['currency_symbol']}{other_total_value:.2f}]"
            return_string += f" [G/L:{gain_loss_string}/{other_gain_loss_string}] [Avg G/L:{average_gain_loss_string}/{other_average_gain_loss_string}]"
            return return_string
        return "N/A"

    # Adds the summary node to a coin object
    def __summarizePurchase(coin, config):
        if isinstance(coin, Node):
            i = 0
            total = 0.0
            count = 0
            while i < len(coin.nodes):
                node = coin.nodes[i]
                if isinstance(node, Purchase):
                    total += node.price * node.quantity
                    count += node.quantity
                elif isinstance(node, str):
                    del coin.nodes[i]
                    i -= 1
                i += 1
            coin.nodes.append(
                Coins.PrintStatistics(
                    config,
                    total,
                    count,
                    coin.data.value,
                    coin.data.value * coin.data.retention,
                )
            )

        return None

    # Returns a tree object for a collection of countries, their denominations, their values, and their coins
    def BuildTree(
        countries,
        denominations,
        values,
        coins,
        purchases=None,
        debug=False,
        only_coin_ids=False,
        config={},
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
                                    Coins.__summarizePurchase(current_coins[-1], config)
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
        for entry in entries:
            if show_only_bullion and not entry[mapping["tag_bullion"]]:
                continue
            if show_only_not_bullion and entry[mapping["tag_bullion"]]:
                continue
            coins[entry[mapping["coin_id"]]] = (
                entry[mapping["coin_id"]],
                None,
            )  # (coin_id, CoinData object)
            if not hide_denominations:
                if not hide_values:
                    if not hide_coins:
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
                        coins[entry[mapping["coin_id"]]] = (
                            coins[entry[mapping["coin_id"]]][0],
                            CoinData(**coin_specs),
                        )
                    if coins[entry[mapping["coin_id"]]][1] is not None:
                        if prices:
                            Coins.Price(coins[entry[mapping["coin_id"]]][1], prices)
                        else:
                            coins[entry[mapping["coin_id"]]][1].togglePrice(False)
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
                try:
                    denominations[entry[mapping["denomination_id"]]]
                except KeyError:
                    # Display name, child values, bullion tag
                    denominations[entry[mapping["denomination_id"]]] = (
                        entry[mapping["denomination_display_name"]],
                        [],
                        entry[mapping["tag_bullion"]],
                    )
                if (
                    entry[mapping["value_id"]]
                    not in denominations[entry[mapping["denomination_id"]]][1]
                ):
                    denominations[entry[mapping["denomination_id"]]][1].append(
                        entry[mapping["value_id"]]
                    )
            try:
                countries[entry[mapping["country_id"]]]
            except KeyError:
                countries[entry[mapping["country_id"]]] = (
                    entry[mapping["country_display_name"]],
                    [],
                )
            if (
                entry[mapping["denomination_id"]]
                not in countries[entry[mapping["country_id"]]][1]
            ):
                countries[entry[mapping["country_id"]]][1].append(
                    entry[mapping["denomination_id"]]
                )

        if do_not_build_tree:
            return (countries, denominations, values, coins)
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
