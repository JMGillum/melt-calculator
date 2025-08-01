"""
   Author: Josh Gillum              .
   Date: 1 August 2025             ":"         __ __
                                  __|___       \ V /
                                .'      '.      | |
                                |  O       \____/  |
^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

    This file stores the Coins class, which provides an interface for
    interacting with the database that stores the coin information.

    Future plans are to move all database specific functionality to a
    separate class that can be modified if the database is switcher or updated.
    This class will thus only contain functions for working with the data, not
    for getting it from the database.

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
    # Calculates the value of all defined coin objects, using the provided precious metal values
    def price(silver_price, gold_price, platinum_price, palladium_price, coin):
        if coin.metal == Metals.SILVER:
            coin.value = coin.precious_metal_weight.as_troy_ounces() * silver_price
        if coin.metal == Metals.GOLD:
            coin.value = coin.precious_metal_weight.as_troy_ounces() * gold_price
        if coin.metal == Metals.PLATINUM:
            coin.value = coin.precious_metal_weight.as_troy_ounces() * platinum_price
        if coin.metal == Metals.PALLADIUM:
            coin.value = coin.precious_metal_weight.as_troy_ounces() * palladium_price
        coin.togglePrice(True)

    # Prints summary statistics for a group of purchases (really just a total,count and worth)
    def print_statistics(
        total: float = 0.0,
        count: int = 0,
        value: float = 0.0,
        stats: PurchaseStats = None,
    ):
        if stats and isinstance(stats, PurchaseStats):
            total = round(stats.total, 2)
            count = int(stats.count)
            if count > 0:
                value = round((stats.total + stats.delta) / stats.count, 2)
        else:
            total = round(total, 2)
            count = int(count)
            value = round(value, 2)
        if count > 0:
            total_value = round(value * count, 2)
            average = round(total / count, 2)
            gain_loss = round(total_value - total, 2)
            average_gain_loss = round(value - average, 2)
            gain_loss_string = (
                printColored(f"+{currency_symbol}{gain_loss:.2f}", config.gain_color)
                if gain_loss > 0
                else printColored(
                    f"(-{currency_symbol}{-gain_loss:.2f})", config.loss_color
                )
            )
            average_gain_loss_string = (
                printColored(
                    f"+{currency_symbol}{average_gain_loss:.2f}", config.gain_color
                )
                if average_gain_loss > 0
                else printColored(
                    f"(-{currency_symbol}{-average_gain_loss:.2f})", config.loss_color
                )
            )
            return_string = ""
            return_string += f"Sum: {currency_symbol}{total:.2f} ~ Avg: {currency_symbol}{average:.2f}"
            return_string += f" ~ Value: {currency_symbol}{total_value:.2f}  ({currency_symbol}{value:.2f} * {count})"
            return_string += (
                f" ~ G/L: {gain_loss_string} ~ Avg G/L: {average_gain_loss_string}"
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
                                            Purchase(
                                                match[1],
                                                match[2],
                                                match[3],
                                                match[4],
                                                match[5],
                                            )
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
                if prices is not None:
                    Coins.price(
                        prices[0], prices[1], prices[2], prices[3], coins[entry[0]][1]
                    )
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

    # Returns a search query for finding coins given some specifiers
    def search(
        country=None,
        denomination=None,
        face_value=None,
        face_value_name=None,
        year=None,
        debug=False,
        show_only_owned=False,
        show_only_not_owned=False,
    ):
        if show_only_owned and show_only_not_owned:
            show_only_owned = False
            show_only_not_owned = False
        select_columns = "coins.coin_id,coins.gross_weight,coins.fineness,coins.precious_metal_weight,coins.years,coins.metal,coins.name,face_values.value_id,face_values.value,face_values.name as value_name,denominations.denomination_id,denominations.name as denomination_name,countries.country_id,countries.name as country_name,tags.bullion"
        base_query = "from coins inner join face_values on coins.face_value_id = face_values.value_id inner join denominations on face_values.denomination_id = denominations.denomination_id inner join countries on denominations.country_id = countries.country_id inner join tags on denominations.tags = tags.tag_id"
        if show_only_owned:
            base_query = f"SELECT DISTINCT {select_columns} {base_query} right join purchases on purchases.coin_id = coins.coin_id"
        elif show_only_not_owned:
            base_query = f"SELECT * from (SELECT DISTINCT {select_columns},purchases.coin_id as filter {base_query} left join purchases on coins.coin_id = purchases.coin_id "
        else:
            base_query = f"SELECT {select_columns} {base_query}"
        found_first_specifier = False
        country_query = ""
        denomination_query = ""
        value_name_query = ""
        value_query = ""
        year_query = ""
        queries = [
            (country_query, country, "countries"),
            (denomination_query, denomination, "denominations"),
            (value_name_query, face_value_name, "face_values"),
        ]
        for i in range(len(queries)):
            item = queries[i]
            if item[1]:
                queries[i] = (
                    f"""(
                    {item[2]}.name like ? or
                    {item[2]}.alternative_name_1 like ? or
                    {item[2]}.alternative_name_2 like ? or
                    {item[2]}.alternative_name_3 like ? or
                    {item[2]}.alternative_name_4 like ? or
                    {item[2]}.alternative_name_5 like ?
                )
                """,
                    item[1],
                )
                if found_first_specifier:
                    queries[i] = (f"AND {queries[i][0]}", item[1])
                found_first_specifier = True

        # Adds specifier for actual value
        if face_value:
            queries.append((value_query, face_value, 1))
            queries[-1] = ("    face_values.value=?", queries[-1][1], queries[-1][2])
            if found_first_specifier:
                queries[-1] = (
                    f"\nAND\n  {queries[-1][0].strip()}",
                    queries[-1][1],
                    queries[-1][2],
                )
            found_first_specifier = True

        # Adds specifier for actual value
        if year:
            queries.append((year_query, f"%{year}%", 1))
            queries[-1] = ("    coins.years like ?", queries[-1][1], queries[-1][2])
            if found_first_specifier:
                queries[-1] = (
                    f"\nAND\n  {queries[-1][0].strip()}",
                    queries[-1][1],
                    queries[-1][2],
                )
            found_first_specifier = True

        return_query = base_query
        variables = []
        if (
            country is not None
            or denomination is not None
            or face_value is not None
            or year is not None
        ):
            return_query += " where "
            for item in queries:
                if item[0]:
                    return_query += item[0]
                    repetitions = 6
                    if len(item) == 3:
                        repetitions = item[2]
                    for _ in range(repetitions):
                        variables.append(item[1])

        if show_only_not_owned:
            return_query += ") as filter_by_owned where filter_by_owned.filter is null"
        return_query += ";"
        if debug:
            print("-----------------------------------")
            print(f"Query:\n{return_query}")
            print(f"Variables:\n{variables}")
            print("-----------------------------------")

        return (return_query, tuple(variables))

    def countryNames():
        return "SELECT name,alternative_name_1,alternative_name_2,alternative_name_3,alternative_name_4,alternative_name_5 from countries;"

    # Parses a string into the four specifiers (country, denomination, year, and face value)
    def parseSearchString(text: str, countries, debug: bool = False):
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
