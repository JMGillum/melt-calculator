import re
import collection
from country import CountryName


minimum_year = 1800
current_year = 2025

def parseSearchString(text:str):
    """Search must be of the form <country> <year> <value> <denomination>"""
    debug = False # Flag for whether to print out information or not
    numbers = re.findall("\d+",text)
    words = re.findall("[a-zA-Z]+",text)

    year = ""
    denomination = ""
    country = ""
    face_value = ""
    if len(numbers) >= 2:
        if(len(numbers[0]) != 4 and len(numbers[1]) == 4):
            year = numbers[1]
            face_value = numbers[0]
        else:
            year = numbers[0]
            face_value = numbers[1]
    elif len(numbers) == 1:
        if(len(numbers[0]) == 4):
            temp = int(numbers[0])
            if(temp >= minimum_year and temp <= current_year):
                year = numbers[0]
            else:
                face_value = numbers[0]
        else:
            face_value = numbers[0]

    country_names = countryNames()

    if len(words) >= 2:
        for word in words:
            temp = validCountry(country_names,word)
            if temp is not None:
                country = temp
                words.remove(word)
                break
    elif len(words) > 0:
        temp = validCountry(country_names,words[0])
        if(temp):
            country = temp
        else:
            denomination = words[0]
        
    if(debug):
        print(f"COUNTRY:{country},DENOMINATION:{denomination},YEAR:{year},FACE VALUE:{face_value}")

    return (country,year,face_value,denomination)

def search(data:collection.CoinCollection,country_name:str|None=None,year:str|int|None=None,denomination:str|None=None,face_value:str|int|None=None,nickname:str|None=None):
    if country_name == "":
        country_name = None
    if year == "":
        year = None
    if denomination == "":
        denomination = None
    if face_value == "":
        face_value = None
    if nickname == "":
        nickname = None
    coins = []
    countries = []
    denominations = []
    values = []

    # Narrows down the countries if possible
    if country_name is not None:
        countries = lookupCountry(data,country_name)
        if year is None and denomination is None and face_value is None and nickname is None:
            return countries
    if countries is None or len(countries) <= 0: # Country doesn't exist in data or name wasn't provided
        countries = data.countries


    # Narrows down the denomination if possible
    if denomination is not None:
        for item in countries:
            denominations += lookupDenomination(item,denomination)
        if year is None and face_value is None and nickname is None:
            return denominations
    if denominations is None or len(denominations) <= 0: # Denomination doesn't exist or wasn't provided
        denominations = []
        for item in countries:
            denominations += item.denominations
    

    if face_value is not None:
        for item in denominations:
            values += lookupValue(item,face_value)
    if values is None or len(values) <= 0:
        values = []
        for item in denominations:
            values += item.values


    if year is not None and not (year == ""):
        coins = []
        for item in values:
           coins += lookupYear(item,year) 
        return coins

    if nickname is not None and not (nickname == ""):
        coins = []
        for item in values:
            coins += lookupValueByNickname(item,nickname)
        return coins

    for item in values:
        coins += item.coins

    return coins

def performSearch(data:collection.CoinCollection,search_string:str):
    arguments = parseSearchString(search_string)
    return search(data,country_name=arguments[0],year=arguments[1],denomination=arguments[3],face_value=arguments[2])

def lookupCountry(data:collection.CoinCollection,name:str|list[str]):
    if isinstance(name,str):
        return [x for x in data.countries if x.name.lower() == name.lower()]
    elif isinstance(name,list):
        countries = []
        for item in name:
            countries += [x for x in data.countries if x.name.lower() == item.lower()]
        return countries

def lookupDenomination(data:collection.Country,name:str):
    return [x for x in data.denominations if x.name.lower() == name.lower()]

def lookupValue(data:collection.Denomination,face_value:int):
    try:
        face_value = int(face_value)
    except ValueError:
        return []
    return [x for x in data.values if x.face_value == face_value]

def lookupValueByNickname(data:collection.Value,nickname:str):
    return [x for x in data.coins if x.nickname.lower() == nickname.lower()]

def lookupYear(data:collection.Value,year:int):
    try:
        year = int(year)
    except ValueError:
        return []
    return [x for x in data.coins if year in x.years]

def validCountry(countries,text):
    for name in countries:
       answer = name.lookup(text)
       if answer is not None:
           return answer
    return None

def countryNames():
    france = CountryName("France",["French"])
    mexico = CountryName("Mexico",["Mexican"])
    united_states = CountryName("United States",["US","USA","United States of America","America","American"])
    germany = CountryName("Germany",["Deutschland","German"])

    return [france,mexico,united_states,germany]
