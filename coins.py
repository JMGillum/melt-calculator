"""
   Author: Josh Gillum              .
   Date: 3 August 2025             ":"         __ __
                                  __|___       \ V /
                                .'      '.      | |
                                |  O       \____/  |
^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

    This file stores the Coins class, which provides an interface for
    interacting with the database that stores the coin information.

    Thie class has no functions for actually getting data. It simply turns 
    data from the database into CoinData objects and builds a tree to represent
    them. 

    See db_interface.py and queries.py for database specific functions.

^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
"""

from coinData import CoinData, Purchase, PurchaseStats
from tree.tree import Tree
from tree.node import Node
from metals import Metals
from config import currency_symbol, current_year, minimum_year
import config
from colors import printColored

import re


class Coins:
    """Container class for various functions related to displaying coins."""
    def __unpack(dictionary,key,default_value=None):
        try:
            return dictionary[key]
        except KeyError:
            return default_value

    # Calculates the value of all defined coin objects, using the provided precious metal values
    def price(coin, **prices):
        for key in prices:
            Coins.__unpack(prices,key)
        try:
            spot = prices[coin.metal][1]
            coin.value = coin.precious_metal_weight.as_troy_ounces() * spot
            coin.togglePrice(True)
        except KeyError:
            coin.value = -1

    def __gainOrLossString(value):
        if value > 0:
            return printColored(f"+{currency_symbol}{value:.2f}", config.gain_color)
        elif value < 0:
            return printColored(f"(-{currency_symbol}{-value:.2f})", config.loss_color)
        else:
            return f"{value}"

    # Prints summary statistics for a group of purchases (really just a total,count and worth)
    def print_statistics(
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
            other_value = round(other_value,2)
        if count > 0:
            total_value = round(value * count, 2)
            other_total_value = round(other_value * count, 2)
            average = round(total / count, 2)
            gain_loss = round(total_value - total, 2)
            other_gain_loss = round(other_total_value - total, 2)
            average_gain_loss = round(value - average, 2)
            other_average_gain_loss = round(other_value - average, 2)
            gain_loss_string = Coins.__gainOrLossString(gain_loss)
            average_gain_loss_string = Coins.__gainOrLossString(average_gain_loss)
            other_gain_loss_string = Coins.__gainOrLossString(other_gain_loss)
            other_average_gain_loss_string = Coins.__gainOrLossString(other_average_gain_loss)
            return_string = ""
            return_string += f"[Count:{count}] [Sum:{currency_symbol}{total:.2f}] [Avg:{currency_symbol}{average:.2f}]"
            return_string += f" [Value:{currency_symbol}{total_value:.2f}/{currency_symbol}{other_total_value:.2f}]"
            return_string += (
                f" [G/L:{gain_loss_string}/{other_gain_loss_string}] [Avg G/L:{average_gain_loss_string}/{other_average_gain_loss_string}]"
            )
            return return_string
        return "N/A"

    # Adds the summary node to a coin object
    def __summarizePurchase(coin):
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
                Coins.print_statistics(
                    total, count, coin.data.value * coin.data.retention
                )
            )

        return None

    # Returns a tree object for a collection of countries, their denominations, their values, and their coins
    def buildTree(
        countries,
        denominations,
        values,
        coins,
        purchases=None,
        debug=False,
        only_coin_ids=False,
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
                                                Purchase(*match[1:6])
                                        )
                                    Coins.__summarizePurchase(current_coins[-1])
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
                                name=printColored(
                                    str(value[0]).title(), config.value_color
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
                color = config.denomination_color

                if denomination[2]:
                    name += config.bullion_hint
                    color = config.bullion_color
                current_denominations.append(
                    Tree(
                        name=printColored(name, color),
                        nodes=current_values,
                    )
                )

            # Sorts the denominations by name
            current_denominations = sorted(current_denominations, key=lambda x: str(x))
            # Appends country tree
            current_countries.append(
                Tree(
                    name=printColored(str(country[0]).title(), config.country_color),
                    nodes=current_denominations,
                )
            )
        # Sorts the countries by name
        current_countries = sorted(current_countries, key=lambda x: str(x))
        results = Tree(name="Results", nodes=current_countries)
        return results

    # Given a set of coins, Fills out dictionaries that can be easily turned into a tree structure
    def build(
        entries,
        prices=None,
        purchases=None,
        debug=False,
        show_only_bullion=False,
        show_only_not_bullion=False,
        hide_coins=False,
        only_coin_ids=False,
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
            if show_only_bullion and not entry[14]:
                continue
            if show_only_not_bullion and entry[14]:
                continue
            coins[entry[0]] = (entry[0], None)
            if not hide_coins:
                coins[entry[0]] = (
                    coins[entry[0]][0],
                    CoinData(
                        weight=entry[1],
                        fineness=entry[2],
                        precious_metal_weight=entry[3],
                        years=entry[4],
                        metal=entry[5],
                        nickname=entry[6],
                    ),
                )
            if coins[entry[0]][1] is not None:
                if prices:
                    Coins.price(coins[entry[0]][1],**prices)
                else:
                    coins[entry[0]][1].togglePrice(False)
            try:
                values[entry[7]]
            except KeyError:
                # Display name, child coins, sorting number
                values[entry[7]] = (entry[9] if entry[9] else entry[8], [], entry[8])
            if entry[0] not in values[entry[7]][1]:
                values[entry[7]][1].append(entry[0])
            try:
                denominations[entry[10]]
            except KeyError:
                # Display name, child values, bullion tag
                denominations[entry[10]] = (entry[11], [], entry[14])
            if entry[7] not in denominations[entry[10]][1]:
                denominations[entry[10]][1].append(entry[7])
            try:
                countries[entry[12]]
            except KeyError:
                countries[entry[12]] = (entry[13], [])
            if entry[10] not in countries[entry[12]][1]:
                countries[entry[12]][1].append(entry[10])

        return Coins.buildTree(
            countries,
            denominations,
            values,
            coins,
            purchases=purchases,
            debug=debug,
            only_coin_ids=only_coin_ids,
        )


    # Parses a string into the four specifiers (country, denomination, year, and face value)
    # countries should be a list of tuples or lists. Each item of countries represents a 
    # country. The first value in the item is the proper name and each subsequent value
    # is an alternative name
    def parseSearchString(text: str, countries: list[list[str]] | list[tuple[str]], debug: bool = False):
        """Parses a string to extract the country's name, year, denomination, and face value"""
        numbers = re.findall("\d+", text)  # Regex finds all strings of digits
        words = re.findall("[a-zA-Z]+", text)  # Same for words

        year = ""
        denomination = ""
        country = ""
        face_value = ""
        # If more than two numbers, picks year and denomination
        if len(numbers) >= 2:
            if len(numbers[0]) != 4 and len(numbers[1]) == 4:
                year = numbers[1]
                face_value = numbers[0]
            else:
                year = numbers[0]
                face_value = numbers[1]
        elif len(numbers) == 1:  # Only one number found
            if (
                len(numbers[0]) == 4
            ):  # Checks if number is 4 digits (a year), then checks if within provided range
                temp = int(numbers[0])
                if temp >= minimum_year and temp <= current_year:
                    year = numbers[0]
                else:  # If not, uses number as face value
                    face_value = numbers[0]
            else:
                face_value = numbers[0]

        # Sets the country name and denomination
        if len(words) >= 2:
            for word in words:
                temp = ""
                for item in countries:
                    for name in item:
                        if name and word.lower() == name.lower():
                            temp = item[0]
                if debug:
                    print(f"Found country name: {temp if temp else 'None'}")
                if temp is not None:
                    country = temp
                    words.remove(word)
                    break
            denomination = words[0]
        elif len(words) > 0:
            temp = None
            for item in countries:
                for name in item:
                    if name and words[0].lower() == name.lower():
                        temp = item[0]
            if debug:
                print(f"Found country name: {temp if temp else 'None'}")
            if temp:
                country = temp
            else:
                denomination = words[0]

        if debug:
            print(
                f"COUNTRY:{country},DENOMINATION:{denomination},YEAR:{year},FACE VALUE:{face_value}"
            )

        # Sets values to None if they weren't found
        return (country, denomination, year, face_value)
