import re
from coinData import CoinData
import weights
from metals import Metals
import collection
from country import CountryName
silver_spot_price = 36.00
minimum_year = 1800
current_year = 2025


def parseSearchString(text:str):
    """Search must be of the form <country> <year> <value> <denomination>"""
    debug = True # Flag for whether to print out information or not
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


def coinsFrance():

    centimes_20 = CoinData(years= list(range(1848,1921)),denomination = "20 centimes",weight = 1,fineness=0.9)
    
    centimes_50_1 = CoinData(years= list(range(1848,1867)),denomination = "50 centimes",weight = 2.5,fineness=0.9)
    centimes_50_2 = CoinData(years= list(range(1866,1921)),denomination = "50 centimes",weight = 2.5,fineness=0.835)
    centimes_50 = [centimes_50_1,centimes_50_2]

    franc_1_1 = CoinData(years = list(range(1848,1867)),denomination = "1 Franc",weight=5,fineness = 0.9)
    franc_1_2 = CoinData(years = list(range(1866,1921)),denomination = "1 Franc",weight=5,fineness = 0.835)
    franc_1 = [franc_1_1,franc_1_2]

    franc_2 = CoinData(years=list(range(1848,1921)),denomination = "2 Franc",weight=10,fineness=0.9)

    franc_5_1 = CoinData(years=list(range(1848,1921)),denomination = "5 Franc",weight = 25,fineness=0.9)
    franc_5_2 = CoinData(years=list(range(1960,1970)),denomination = "5 Franc",weight = 12,fineness=0.835)
    franc_5_3 = CoinData(years=list(range(1848,1915)),denomination = "5 Franc",weight = 1.6129,fineness=0.9)
    franc_5_silver = [franc_5_1,franc_5_2]
    franc_5_gold = [franc_5_3]

    franc_10_1 = CoinData(years = [x for x in list(range(1929,1940)) if x not in [1935,1936]], denomination = "10 Francs",weight = 10,fineness=0.68)
    franc_10_2 = CoinData(years = list(range(1848,1915)), denomination = "10 Francs",weight = 3.2258,fineness=0.90)
    franc_10_silver = [franc_10_1]
    franc_10_gold = [franc_10_2]

    franc_20_1 = CoinData(years = [x for x in range(1906,1915)], denomination = "20 Francs",weight = 6.4516,fineness=0.9)
    franc_20_2 = CoinData(years = list(range(1929,1940)), denomination = "20 Francs",weight = 20,fineness=0.68)
    franc_20_silver = [franc_20_2]
    franc_20_gold = [franc_20_1]

    franc_50 = CoinData(years=list(range(1848,1915)),denomination = "50 Francs",weight=16.129,fineness=0.9)

    franc_100_1 = CoinData(years = [x for x in range(1982,2001)], denomination = "100 Francs",weight = 15,fineness=0.9)
    franc_100_2 = CoinData(years = list(range(1848,1915)), denomination = "100 Francs",weight = 32.2581,fineness=0.9)
    franc_100_3 = CoinData(years = list(range(1929,1937)), denomination = "100 Francs",weight = 6.55,fineness=0.9)
    franc_100_silver = [franc_100_1]
    franc_100_gold = [franc_100_2,franc_100_3]


    # Assign metal type and country to all coins
    silver_coins = [centimes_20,franc_2] + centimes_50 + franc_1 + franc_5_silver + franc_10_silver + franc_20_silver + franc_100_silver
    gold_coins = [franc_50] + franc_5_gold + franc_10_gold + franc_20_gold + franc_100_gold
    for coin in silver_coins:
        coin.metal = Metals.SILVER
        coin.country = "France"
    for coin in gold_coins:
        coin.metal = Metals.GOLD
        coin.country = "France"
    # french_coins = silver_coins + gold_coins

    # Centimes
    france_20_centimes = collection.Value(coins=centimes_20,face_value=20)
    france_50_centimes = collection.Value(coins=centimes_50,face_value=50)

    centime = collection.Denomination(values=[france_20_centimes,france_50_centimes],name="Centime")

    # Francs
    france_1_franc = collection.Value(coins=franc_1,face_value=1)
    france_2_franc = collection.Value(coins=franc_2,face_value=2)
    france_5_franc = collection.Value(coins=franc_5_silver+franc_5_gold,face_value=5)
    france_10_franc = collection.Value(coins=franc_10_silver+franc_10_gold,face_value=10)
    france_20_franc = collection.Value(coins=franc_20_silver+franc_20_gold,face_value=20)
    france_50_franc = collection.Value(coins=franc_50,face_value=50)
    france_100_franc = collection.Value(coins=franc_100_silver+franc_100_gold,face_value=100)

    franc = collection.Denomination(values=[france_1_franc,france_2_franc,france_5_franc,france_10_franc,france_20_franc,france_50_franc,france_100_franc],name="Franc")

    return collection.Country(denominations=[centime,franc],name="France")


def coinsMexico():

    mexico_un_peso = CoinData(years = [x for x in list(range(1920,1946)) if x not in (list(range(1928,1932))+[1936,1937,1939,1941,1942])],country="Mexico",metal=Metals.SILVER,denomination = "1 Peso", weight = weights.Weight(16.66,weights.Units.GRAMS),fineness=0.72,precious_metal_weight=weights.Weight(0.3857,weights.Units.TROY_OUNCES))

    mexico_un_peso = collection.Value(coins=mexico_un_peso,name="Un Peso",face_value=1)

    peso = collection.Denomination(values=[mexico_un_peso],name="Peso")

    return collection.Country(denominations=peso,name="Mexico")


def coinsUnitedStates():
    barber_dime = CoinData(nickname="Barber Dime",years=[x for x in list(range(1892,1917))],country="United States",metal=Metals.SILVER,denomination = "10 cents",weight = weights.Weight(2.50,weights.Units.GRAMS),fineness=0.900,precious_metal_weight=weights.Weight(0.07234,weights.Units.TROY_OUNCES))
    mercury_dime = CoinData(nickname="Mercury Dime",years=[x for x in list(range(1916,1946)) if x not in [1922,1932,1933]],country="United States",metal=Metals.SILVER,denomination = "10 cents",weight = weights.Weight(2.50,weights.Units.GRAMS),fineness=0.900,precious_metal_weight=weights.Weight(0.07234,weights.Units.TROY_OUNCES))
    roosevelt_dime = CoinData(nickname="Roosevelt Dime",years=[x for x in list(range(1946,1965))],country="United States",metal=Metals.SILVER,denomination = "10 cents",weight = weights.Weight(2.50,weights.Units.GRAMS),fineness=0.900,precious_metal_weight=weights.Weight(0.07234,weights.Units.TROY_OUNCES))

    dimes = collection.Value(coins=[barber_dime,mercury_dime,roosevelt_dime],name="Dimes",face_value=10)

    standing_liberty_quarter = CoinData(nickname="Standing Liberty Quarter",years=[x for x in list(range(1916,1931)) if x not in [1922]],country="United States",metal=Metals.SILVER,denomination = "25 cents",weight = weights.Weight(6.25,weights.Units.GRAMS),fineness=0.900,precious_metal_weight=weights.Weight(0.18084,weights.Units.TROY_OUNCES))
    washington_quarter = CoinData(nickname="Washington Quarter",years=[x for x in list(range(1932,1965)) if x not in [1933]],country="United States",metal=Metals.SILVER,denomination = "25 cents",weight = weights.Weight(6.25,weights.Units.GRAMS),fineness=0.900,precious_metal_weight=weights.Weight(0.18084,weights.Units.TROY_OUNCES))

    quarters = collection.Value(coins=[standing_liberty_quarter,washington_quarter],name = "Quarters",face_value=25)

    walking_liberty_half = CoinData(nickname = "Walking Liberty Half",years=[x for x in list(range(1916,1948)) if x not in ([1922]+list(range(1924,1927))+list(range(1930,1933)))],country="United States",metal=Metals.SILVER,denomination = "50 cents",weight = weights.Weight(12.5,weights.Units.GRAMS),fineness=0.900,precious_metal_weight=weights.Weight(0.36169,weights.Units.TROY_OUNCES))
    benjamin_half = CoinData(nickname = "Benjamin Half",years=[x for x in list(range(1948,1964))],country="United States",metal=Metals.SILVER,denomination = "50 cents",weight = weights.Weight(12.5,weights.Units.GRAMS),fineness=0.900,precious_metal_weight=weights.Weight(0.36169,weights.Units.TROY_OUNCES))
    kennedy_half_1 = CoinData(nickname = "90% Kennedy Half",years=[1964],country="United States",metal=Metals.SILVER,denomination = "50 cents",weight = weights.Weight(12.5,weights.Units.GRAMS),fineness=0.900,precious_metal_weight=weights.Weight(0.36169,weights.Units.TROY_OUNCES))
    kennedy_half_2 = CoinData(nickname="40% Kennedy Half",years=[x for x in list(range(1965,1971))],country="United States",metal=Metals.SILVER,denomination = "50 cents",weight = weights.Weight(11.5,weights.Units.GRAMS),fineness=0.400,precious_metal_weight=weights.Weight(0.1479,weights.Units.TROY_OUNCES))

    halves = collection.Value(coins=[walking_liberty_half,benjamin_half,kennedy_half_1,kennedy_half_2],name="Halves",face_value=50)

    morgan_dollar = CoinData(nickname="Morgan Dollar",years=[x for x in (list(range(1878,1905))+[1921])],country="United States",metal=Metals.SILVER,denomination = "1 dollar",weight = weights.Weight(26.73,weights.Units.GRAMS),fineness=0.900,precious_metal_weight=weights.Weight(0.77344,weights.Units.TROY_OUNCES))
    peace_dollar = CoinData(nickname="Peace Dollar",years=[x for x in (list(range(1921,1929))+[1934,1935])],country="United States",metal=Metals.SILVER,denomination = "1 dollar",weight = weights.Weight(26.73,weights.Units.GRAMS),fineness=0.900,precious_metal_weight=weights.Weight(0.77344,weights.Units.TROY_OUNCES))

    dollar_coins = collection.Value(coins=[morgan_dollar,peace_dollar],name="Dollar Coins",face_value=1)

    cents = collection.Denomination(values=[dimes,quarters,halves],name="Cents")
    dollars = collection.Denomination(values=[dollar_coins],name="Dollars")
    
    return collection.Country(denominations=[cents,dollars],name="United States")

# United States
united_states = coinsUnitedStates()

# France
france = coinsFrance()

# Mexico
mexico = coinsMexico()


data = collection.CoinCollection(countries=sorted([united_states,mexico,france],key=lambda country: country.name),name="Precious Metals")


data.tree.cascading_set_fancy(True)
interactive_mode = True

lines = []
if interactive_mode:
    results = performSearch(data,"France")
    if results is None or len(results) == 0:
        print("No results found")
    else:
        if not isinstance(results,list):
            results = [results]
        for item in results:
            if isinstance(item,collection.Country) or isinstance(item,collection.Denomination):
                item.tree.cascading_set_fancy(True)
                lines += item.tree.print()
            else:
                print(item)
else:
    lines = data.tree.print()

for line in lines:
    print(line)
