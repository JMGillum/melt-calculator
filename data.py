from datetime import datetime
import collection
from coinData import CoinData,Purchase
from metals import Metals
import weights
from country import CountryName


silver_spot_price = 36.00
gold_spot_price = 3350.00


def coinsItaly(show_personal_collection=True):
    """Builds a CoinCollection object about the precious metal content of Italian coins"""
    centesimi_20 = CoinData(years=list(range(1863,1918)),weight=1,fineness=0.835)



    silver_coins = [centesimi_20]
    gold_coins = []

    """
    for item in silver_coins:
        item.metal = Metals.SILVER
        item.country = "Italy"
    for item in gold_coins:
        item.metal = Metals.GOLD
        item.country = "Italy"
    """

    italy_20_centesimi = collection.Value(coins=[centesimi_20],face_value=20)

    centesimi = collection.Denomination(values=[italy_20_centesimi],name="Centesimi")

    italy = collection.Country(denominations=[centesimi],name="Italy")
    
    for denomination in italy.denominations:
        for value in denomination.values:
            for coin in value.coins:
                coin.face_value = value.face_value
                coin.denomination = denomination.name
                coin.country = "Italy"
                if coin in silver_coins:
                    coin.metal = Metals.SILVER
                    silver_coins.remove(coin)
                if coin in gold_coins:
                    coin.metal = Metals.GOLD
                    gold_coins.remove(coin)

    if show_personal_collection:
        # Personal collection below
        pass
        # Personal collection above

    return italy

def coinsFrance(show_personal_collection=True):
    """Builds a CoinCollection object about the precious metal content of French coins"""
    centimes_20 = CoinData(
        years=list(range(1848, 1921)),
        weight=1,
        fineness=0.9,
    )

    centimes_50_1 = CoinData(
        years=list(range(1848, 1867)),
        weight=2.5,
        fineness=0.9,
    )
    centimes_50_2 = CoinData(
        years=list(range(1866, 1921)),
        weight=2.5,
        fineness=0.835,
    )
    centimes_50 = [centimes_50_1, centimes_50_2]

    franc_1_1 = CoinData(
        years=list(range(1848, 1867)), weight=5, fineness=0.9
    )
    franc_1_2 = CoinData(
        years=list(range(1866, 1921)), weight=5, fineness=0.835
    )
    franc_1 = [franc_1_1, franc_1_2]

    franc_2 = CoinData(
        years=list(range(1848, 1921)), weight=10, fineness=0.9
    )

    franc_5_1 = CoinData(
        years=list(range(1848, 1921)), weight=25, fineness=0.9
    )
    franc_5_2 = CoinData(
        years=list(range(1960, 1970)), weight=12, fineness=0.835
    )
    franc_5_3 = CoinData(
        years=list(range(1848, 1915)),
        weight=1.6129,
        fineness=0.9,
    )
    franc_5_silver = [franc_5_1, franc_5_2]
    franc_5_gold = [franc_5_3]

    franc_10_1 = CoinData(
        years=[x for x in list(range(1929, 1940)) if x not in [1935, 1936]],
        weight=10,
        fineness=0.68,
    )
    franc_10_2 = CoinData(
        years=list(range(1848, 1915)),
        weight=3.2258,
        fineness=0.90,
    )
    franc_10_silver = [franc_10_1]
    franc_10_gold = [franc_10_2]

    franc_20_1 = CoinData(
        years=[x for x in range(1906, 1915)],
        weight=6.4516,
        fineness=0.9,
    )
    franc_20_2 = CoinData(
        years=list(range(1929, 1940)),
        weight=20,
        fineness=0.68,
    )
    franc_20_silver = [franc_20_2]
    franc_20_gold = [franc_20_1]

    franc_50 = CoinData(
        years=list(range(1848, 1915)),
        weight=16.129,
        fineness=0.9,
    )

    franc_100_1 = CoinData(
        years=[x for x in range(1982, 2001)],
        weight=15,
        fineness=0.9,
    )
    franc_100_2 = CoinData(
        years=list(range(1848, 1915)),
        weight=32.2581,
        fineness=0.9,
    )
    franc_100_3 = CoinData(
        years=list(range(1929, 1937)),
        weight=6.55,
        fineness=0.9,
    )
    franc_100_silver = [franc_100_1]
    franc_100_gold = [franc_100_2, franc_100_3]

    # Assign metal type and country to all coins
    silver_coins = (
        [centimes_20, franc_2]
        + centimes_50
        + franc_1
        + franc_5_silver
        + franc_10_silver
        + franc_20_silver
        + franc_100_silver
    )
    gold_coins = (
        [franc_50] + franc_5_gold + franc_10_gold + franc_20_gold + franc_100_gold
    )
    """
    for coin in silver_coins:
        coin.metal = Metals.SILVER
        coin.country = "France"
    for coin in gold_coins:
        coin.metal = Metals.GOLD
        coin.country = "France"
    # french_coins = silver_coins + gold_coins
    """

    # Centimes
    france_20_centimes = collection.Value(coins=centimes_20, face_value=20)
    france_50_centimes = collection.Value(coins=centimes_50, face_value=50)

    centime = collection.Denomination(
        values=[france_20_centimes, france_50_centimes], name="Centime"
    )

    # Francs
    france_1_franc = collection.Value(coins=franc_1, face_value=1)
    france_2_franc = collection.Value(coins=franc_2, face_value=2)
    france_5_franc = collection.Value(coins=franc_5_silver + franc_5_gold, face_value=5)
    france_10_franc = collection.Value(
        coins=franc_10_silver + franc_10_gold, face_value=10
    )
    france_20_franc = collection.Value(
        coins=franc_20_silver + franc_20_gold, face_value=20
    )
    france_50_franc = collection.Value(coins=franc_50, face_value=50)
    france_100_franc = collection.Value(
        coins=franc_100_silver + franc_100_gold, face_value=100
    )

    franc = collection.Denomination(
        values=[
            france_1_franc,
            france_2_franc,
            france_5_franc,
            france_10_franc,
            france_20_franc,
            france_50_franc,
            france_100_franc,
        ],
        name="Franc",
    )

    france = collection.Country(denominations=[centime, franc], name="France")

    for denomination in france.denominations:
        for value in denomination.values:
            for coin in value.coins:
                coin.face_value = value.face_value
                coin.denomination = denomination.name
                coin.country = "France"
                if coin in silver_coins:
                    coin.metal = Metals.SILVER
                    silver_coins.remove(coin)
                if coin in gold_coins:
                    coin.metal = Metals.GOLD
                    gold_coins.remove(coin)

    if show_personal_collection:
        # Personal collection below
        franc_10_1.addCollection(Purchase(price=8.00,mint_date=1931,purchase_date = datetime(2025,7,4)))
        franc_100_1.addCollection(Purchase(price=11.95,purchase_date=datetime(2025,7,3),mint_date=1982))
        # Personal collection above

    return france



def coinsGermany(show_personal_collection=True):
    """Builds a CoinCollection object about the precious metal content of German coins"""
    mark_10 = CoinData(years=list(range(1871,1916)),weight=3.9825,fineness=0.900,retention=0.97)

    german_10_mark = collection.Value(coins=mark_10,face_value=10)

    mark = collection.Denomination(values=[german_10_mark],name="Mark")

    silver_coins = []
    gold_coins = [mark_10]

    germany = collection.Country(denominations=[mark],name="Germany")

    for denomination in germany.denominations:
        for value in denomination.values:
            for coin in value.coins:
                coin.face_value = value.face_value
                coin.denomination = denomination.name
                coin.country = "Germany"
                if coin in silver_coins:
                    coin.metal = Metals.SILVER
                    silver_coins.remove(coin)
                if coin in gold_coins:
                    coin.metal = Metals.GOLD
                    gold_coins.remove(coin)

    if show_personal_collection:
        # Personal collection below
        mark_10.addCollection(Purchase(price=373.98,purchase_date=datetime(2025,7,5),mint_date=1898,mint_mark="A"))
        # Personal collection above

    return germany


def coinsMexico(show_personal_collection=True):
    """Builds a CoinCollection object about the precious metal content of Mexican coins"""
    peso_1 = CoinData(
        years=[
            x
            for x in list(range(1920, 1946))
            if x not in (list(range(1928, 1932)) + [1936, 1937, 1939, 1941, 1942])
        ],
        country="Mexico",
        weight=16.66,
        fineness=0.72,
    )

    mexico_un_peso = collection.Value(
        coins=[peso_1], name="Un Peso", face_value=1
    )


    silver_coins = [peso_1]
    gold_coins = []

    peso = collection.Denomination(values=[mexico_un_peso], name="Peso")

    mexico = collection.Country(denominations=[peso], name="Mexico")
    
    for denomination in mexico.denominations:
        for value in denomination.values:
            for coin in value.coins:
                coin.face_value = value.face_value
                coin.denomination = denomination.name
                coin.country = "Mexico"
                if coin in silver_coins:
                    coin.metal = Metals.SILVER
                    silver_coins.remove(coin)
                if coin in gold_coins:
                    coin.metal = Metals.GOLD
                    gold_coins.remove(coin)

    if show_personal_collection:
        # Personal collection below
        pass
        # Personal collection above

    return mexico


def coinsUnitedStates(show_personal_collection=True):
    """Builds a CoinCollection object about the precious metal content of United States coins"""
    barber_dime = CoinData(
        nickname="Barber Dime",
        years=[x for x in list(range(1892, 1917))],
        weight=2.5,
        fineness=0.900,
    )
    mercury_dime = CoinData(
        nickname="Mercury Dime",
        years=[x for x in list(range(1916, 1946)) if x not in [1922, 1932, 1933]],
        weight=2.5,
        fineness=0.900,
    )
    roosevelt_dime = CoinData(
        nickname="Roosevelt Dime",
        years=[x for x in list(range(1946, 1965))],
        weight=2.5,
        fineness=0.900,
    )


    barber_quarter = CoinData(
        nickname="Barber Quarter",
        years=list(range(1892,1917)),
        weight=6.25,
        fineness=0.900,
    )
    standing_liberty_quarter = CoinData(
        nickname="Standing Liberty Quarter",
        years=[x for x in list(range(1916, 1931)) if x not in [1922]],
        weight=6.25,
        fineness=0.900,
    )
    washington_quarter = CoinData(
        nickname="Washington Quarter",
        years=[x for x in list(range(1932, 1965)) if x not in [1933]],
        weight=6.25,
        fineness=0.900,
    )


    walking_liberty_half = CoinData(
        nickname="Walking Liberty Half",
        years=[
            x
            for x in list(range(1916, 1948))
            if x not in ([1922] + list(range(1924, 1927)) + list(range(1930, 1933)))
        ],
        country="United States",
        metal=Metals.SILVER,
        weight=12.5,
        fineness=0.900,
    )
    benjamin_half = CoinData(
        nickname="Benjamin Half",
        years=[x for x in list(range(1948, 1964))],
        weight=12.5,
        fineness=0.900,
    )
    kennedy_half_1 = CoinData(
        nickname="90% Kennedy Half",
        years=[1964],
        weight=12.5,
        fineness=0.900,
    )
    kennedy_half_2 = CoinData(
        nickname="40% Kennedy Half",
        years=[x for x in list(range(1965, 1971))],
        weight=11.5,
        fineness=0.400,
    )


    morgan_dollar = CoinData(
        nickname="Morgan Dollar",
        years=[x for x in (list(range(1878, 1905)) + [1921])],
        weight=26.73,
        fineness=0.900,
    )
    peace_dollar = CoinData(
        nickname="Peace Dollar",
        years=[x for x in (list(range(1921, 1929)) + [1934, 1935])],
        weight=26.73,
        fineness=0.900,
    )

    silver_coins = [barber_dime,mercury_dime,roosevelt_dime,barber_quarter,standing_liberty_quarter,washington_quarter,walking_liberty_half,benjamin_half,kennedy_half_1,kennedy_half_2,morgan_dollar,peace_dollar]
    gold_coins = []
    
    dimes = collection.Value(
        coins=[barber_dime, mercury_dime, roosevelt_dime], name="Dimes", face_value=10
    )
    quarters = collection.Value(
        coins=[barber_quarter,standing_liberty_quarter, washington_quarter],
        name="Quarters",
        face_value=25,
    )
    halves = collection.Value(
        coins=[walking_liberty_half, benjamin_half, kennedy_half_1, kennedy_half_2],
        name="Halves",
        face_value=50,
    )
    dollar_coins = collection.Value(
        coins=[morgan_dollar, peace_dollar], name="Dollar Coins", face_value=1
    )


    cents = collection.Denomination(values=[dimes, quarters, halves], name="Cents")
    dollars = collection.Denomination(values=[dollar_coins], name="Dollars")

    unitedStates = collection.Country(denominations=[cents, dollars], name="United States")

    for denomination in unitedStates.denominations:
        for value in denomination.values:
            for coin in value.coins:
                coin.face_value = value.face_value
                coin.denomination = denomination.name
                coin.country = "United States"
                if coin in silver_coins:
                    coin.metal = Metals.SILVER
                    silver_coins.remove(coin)
                if coin in gold_coins:
                    coin.metal = Metals.GOLD
                    gold_coins.remove(coin)

    if show_personal_collection:
        # Personal collection below
        mercury_dime.addCollection(Purchase(price=2.56,purchase_date=datetime(2025,7,12),quantity=1))
        roosevelt_dime.addCollection([Purchase(price=2.56,purchase_date=datetime(2025,7,12),quantity=48),Purchase(price=0.1,purchase_date=datetime(2025,7,12),quantity=1)])
        barber_quarter.addCollection(Purchase(price=6.43,purchase_date=datetime(2025,7,12),quantity=4))
        standing_liberty_quarter.addCollection(Purchase(price=6.43,purchase_date=datetime(2025,7,12),quantity=4))
        washington_quarter.addCollection(Purchase(price=2.56,purchase_date=datetime(2025,7,12),quantity=28))
        walking_liberty_half.addCollection(Purchase(price=12.86,purchase_date=datetime(2025,7,12),quantity=9))
        benjamin_half.addCollection(Purchase(price=12.86,purchase_date=datetime(2025,7,12),quantity=1))
        # Personal collection above

    return unitedStates

def coinsCanada(show_personal_collection=True):
    dollar_5 = CoinData(nickname="Silver Maple Leaf Bullion",years=list(range(1988,2026)),weight=31.11,fineness=0.9999,precious_metal_weight=weights.Weight(1,weights.Units.TROY_OUNCES))

    silver_coins = [dollar_5]
    gold_coins = []

    canada_5_dollars = collection.Value(coins=dollar_5,name="5 Dollar Coins",face_value=5)

    dollars = collection.Denomination(values=[canada_5_dollars],name="Dollars")
    
    canada = collection.Country(denominations=[dollars],name="Canada")

    for denomination in canada.denominations:
        for value in denomination.values:
            for coin in value.coins:
                coin.face_value = value.face_value
                coin.denomination = denomination.name
                coin.country = "Canada"
                if coin in silver_coins:
                    coin.metal = Metals.SILVER
                    silver_coins.remove(coin)
                if coin in gold_coins:
                    coin.metal = Metals.GOLD
                    gold_coins.remove(coin)

    if show_personal_collection:
        # Personal collection below
        dollar_5.addCollection([Purchase(price=33.9,purchase_date=datetime(2025,4,18)),Purchase(price=37.95,purchase_date=datetime(2025,6,24)),Purchase(price=38.2,purchase_date=datetime(2025,7,8))])
        # Personal collection above
    return canada


countries = [
        (CountryName("France", ["French"]),coinsFrance),
        (CountryName("Mexico", ["Mexican"]),coinsMexico),
        (CountryName(
            "United States",
            ["US", "USA", "United States of America", "America", "American"],
        ),coinsUnitedStates),
        (CountryName("Germany", ["Deutschland", "German"]),coinsGermany),
        (CountryName("Italy",["Italian","Italia"]),coinsItaly),
        (CountryName("Canada",["Canadian"]),coinsCanada),
        ]
