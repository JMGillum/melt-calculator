import re
from countryName import CountryName
import data


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


def countryInfo(name, return_name=True, return_build=True, countries=None):
    """Returns information about a country, if it exists.
    Name is the name of the country
    return_name is boolean for whether the proper/main name of the country will be returned
    return_build is boolean for whether the build function of the country will be returned
    countries is a list of (countryName,buildFunction) tuples to search through. If not provided,
    the ones specified in data.countries will be used."""
    if return_name or return_build:
        if countries is None:
            countries = countryNames()
            if not isinstance(countries, list):
                countries = [countries]
            for item in countries:
                item_name = item
                if isinstance(item, tuple):
                    item_name = item[0]
                else:
                    item = (item, None)
                answer = item_name.lookup(name)
                if answer is not None:  # Determines what to return
                    if return_name and return_build:
                        return item
                    if return_name and not return_build:
                        return item_name
                    if not return_name and return_build:
                        return item[1]
                    else:
                        return None
    return None


def validCountry(text, countries=None):
    """Determines if the string is a valid country name. Returns country's
    proper/main name on success, and None on failure. Wrapper for Search.countryInfo()"""
    return countryInfo(text, return_build=False, countries=countries)


def lookupCountryBuild(name, countries=None):
    """Finds the coin build function of a country, if the country is valid.
    Returns a tuple of (countryName,buildFunction) on success, None on fail."""
    return countryInfo(name, return_name=False, countries=countries)


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
            if temp is not None:
                country = temp.name
                words.remove(word)
                break
        denomination = words[0]
    elif len(words) > 0:
        temp = validCountry(words[0])
        if temp:
            country = temp.name
        else:
            denomination = words[0]

    if debug:
        print(
            f"COUNTRY:{country},DENOMINATION:{denomination},YEAR:{year},FACE VALUE:{face_value}"
        )

    # Sets values to None if they weren't found
    return (country, denomination, year, face_value)
