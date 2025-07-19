"""
   Author: Josh Gillum              .
   Date: 18 July 2025              ":"         __ __
                                  __|___       \ V /
                                .'      '.      | |
                                |  O       \____/  |
^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

    This file contains functions related to searching for coins. The notable
    function is parseSearchString(), which takes a string and parses it into
    the constituent arguments (country, denomination, face value, year). These
    are then used in the Coins class (in coinInfo.py) to find corresponding
    coins.

    There are also functions for finding information about a country (namely,
    its name), as well as determining if a name belongs to a country.

^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
"""

import re
from countryName import CountryName


minimum_year = 1800
current_year = 2025


def countryNames():
    """Initialization function for country names. Optional with_functions parameter
    will return a list of tuples of the form (CountryName,country coin build function)"""
    france = CountryName("France", ["French"])
    mexico = CountryName("Mexico", ["Mexican"])
    united_states = CountryName(
        "United States",
        ["US", "USA", "United States of America", "America", "American"],
    )
    germany = CountryName("Germany", ["Deutschland", "German"])
    italy = CountryName("Italy", ["Italian", "Italia"])
    canada = CountryName("Canada", ["Canadian"])

    return [france, mexico, united_states, germany, italy, canada]


def validCountry(name, countries=None):
    """Determines if the string is a valid country name. Returns country's
    proper/main name on success, and None on failure."""
    if countries is None:
        countries = countryNames()
    if not isinstance(countries, list):
        countries = [countries]
    for item in countries:
        answer = item.lookup(name)
        if answer:
            return answer
    return None



def parseSearchString(text: str, debug: bool = False):
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
            temp = validCountry(word)  # checks if word is a valid country name
            print(temp)
            if temp is not None:
                country = temp
                words.remove(word)
                break
        denomination = words[0]
    elif len(words) > 0:
        temp = validCountry(words[0])
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
