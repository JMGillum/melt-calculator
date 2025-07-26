"""
   Author: Josh Gillum              .
   Date: 25 July 2025              ":"         __ __
   Code: Line 50                  __|___       \ V /
                                .'      '.      | |
                                |  O       \____/  |
^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

 |->United States
     |->Bullion
     |  |->1/10 Oz Bullion
     |  |  |->american_gold_eagle_dollar_5
     |  |  |->american_platinum_eagle_dollar_10
     |  |  |->american_gold_buffalo_dollar_5
     |  |->1/4 Oz Bullion
     |  |  |->american_gold_eagle_dollar_10
     |  |  |->american_platinum_eagle_dollar_25
     |  |  |->american_gold_buffalo_dollar_10
     |  |->1/2 Oz Bullion
     |  |  |->american_gold_eagle_dollar_25
     |  |  |->american_platinum_eagle_dollar_50
     |  |  |->american_gold_buffalo_dollar_25
     |  |->1 Oz Bullion
     |      |->american_gold_eagle_dollar_50
     |      |->american_platinum_eagle_dollar_100
     |      |->american_gold_buffalo_dollar_50
     |      |->american_palladium_eagle_dollar_25
     |->Cent
     |  |->Dime
     |  |  |->barber_dime
     |  |  |->mercury_dime
     |  |  |->roosevelt_dime
     |  |->Quarter
     |  |  |->barber_quarter
     |  |  |->standing_liberty_quarter
     |  |  |->washington_quarter
     |  |->Half
     |      |->walking_liberty_half
     |      |->benjamin_half
     |      |->kennedy_half_1
     |      |->kennedy_half_2
     |->Dollar
         |->Dollar
             |->morgan_dollar
             |->peace_dollar

^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
"""

from coinData import CoinData
from tree.node import Node
from metals import Metals
from config import current_year
import weights
from coins.namedList import NamedList
from alternativeNames import AlternativeNames as AN
from coins.taggedList import TaggedList
from coins.tags import Tags

coins = {
    # United States
    "barber_dime": Node(
        CoinData(
            nickname="Barber Dime",
            years=[x for x in list(range(1892, 1917))],
            weight=2.5,
            fineness=0.900,
            metal=Metals.SILVER,
            country="United States",
            face_value=10,
            denomination="Cents",
        )
    ),
    "mercury_dime": Node(
        CoinData(
            nickname="Mercury Dime",
            years=[
                x for x in list(range(1916, 1946)) if x not in [1922, 1932, 1933]
            ],
            weight=2.5,
            fineness=0.900,
            metal=Metals.SILVER,
            country="United States",
            face_value=10,
            denomination="Cents",
        )
    ),
    "roosevelt_dime": Node(
        CoinData(
            nickname="Roosevelt Dime",
            years=[x for x in list(range(1946, 1965))],
            weight=2.5,
            fineness=0.900,
            metal=Metals.SILVER,
            country="United States",
            face_value=10,
            denomination="Cents",
        )
    ),
    "barber_quarter": Node(
        CoinData(
            nickname="Barber Quarter",
            years=list(range(1892, 1917)),
            weight=6.25,
            fineness=0.900,
            metal=Metals.SILVER,
            country="United States",
            face_value=25,
            denomination="Cents",
        )
    ),
    "standing_liberty_quarter": Node(
        CoinData(
            nickname="Standing Liberty Quarter",
            years=[x for x in list(range(1916, 1931)) if x not in [1922]],
            weight=6.25,
            fineness=0.900,
            metal=Metals.SILVER,
            country="United States",
            face_value=25,
            denomination="Cents",
        )
    ),
    "washington_quarter": Node(
        CoinData(
            nickname="Washington Quarter",
            years=[x for x in list(range(1932, 1965)) if x not in [1933]],
            weight=6.25,
            fineness=0.900,
            metal=Metals.SILVER,
            country="United States",
            face_value=25,
            denomination="Cents",
        )
    ),
    "walking_liberty_half": Node(
        CoinData(
            nickname="Walking Liberty Half",
            years=[
                x
                for x in list(range(1916, 1948))
                if x
                not in ([1922] + list(range(1924, 1927)) + list(range(1930, 1933)))
            ],
            weight=12.5,
            fineness=0.900,
            metal=Metals.SILVER,
            country="United States",
            face_value=50,
            denomination="Cents",
        )
    ),
    "benjamin_half": Node(
        CoinData(
            nickname="Benjamin Half",
            years=[x for x in list(range(1948, 1964))],
            weight=12.5,
            fineness=0.900,
            metal=Metals.SILVER,
            country="United States",
            face_value=50,
            denomination="Cents",
        )
    ),
    "kennedy_half_1": Node(
        CoinData(
            nickname="90% Kennedy Half",
            years=[1964],
            weight=12.5,
            fineness=0.900,
            metal=Metals.SILVER,
            country="United States",
            face_value=50,
            denomination="Cents",
        )
    ),
    "kennedy_half_2": Node(
        CoinData(
            nickname="40% Kennedy Half",
            years=[x for x in list(range(1965, 1971))],
            weight=11.5,
            fineness=0.400,
            metal=Metals.SILVER,
            country="United States",
            face_value=50,
            denomination="Cents",
        )
    ),
    "morgan_dollar": Node(
        CoinData(
            nickname="Morgan Dollar",
            years=[x for x in (list(range(1878, 1905)) + [1921])],
            weight=26.73,
            fineness=0.900,
            metal=Metals.SILVER,
            country="United States",
            face_value=1,
            denomination="Dollar",
        )
    ),
    "peace_dollar": Node(
        CoinData(
            nickname="Peace Dollar",
            years=[x for x in (list(range(1921, 1929)) + [1934, 1935])],
            weight=26.73,
            fineness=0.900,
            metal=Metals.SILVER,
            country="United States",
            face_value=1,
            denomination="Dollar",
        )
    ),
    "american_silver_eagle": Node(
        CoinData(
            nickname="Silver Eagle",
            years=list(range(1986,current_year+1)),
            weight=31.11,
            fineness=0.999,
            precious_metal_weight=weights.Weight(1,weights.Units.TROY_OUNCES),
            metal=Metals.SILVER,
            country="United States",
            face_value=1,
            denomination="Dollar",
        )
    ),
    "american_gold_eagle_dollar_5": Node(
        CoinData(
            nickname="Gold Eagle",
            years=list(range(1986,current_year+1)),
            weight=3.393,
            fineness=0.9167,
            precious_metal_weight=weights.Weight(0.1,weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="United States",
            face_value=5,
            denomination="Dollar",
        )
    ),
    "american_gold_eagle_dollar_10": Node(
        CoinData(
            nickname="Gold Eagle",
            years=list(range(1986,current_year+1)),
            weight=8.483,
            fineness=0.9167,
            precious_metal_weight=weights.Weight(0.25,weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="United States",
            face_value=10,
            denomination="Dollar",
        )
    ),
    "american_gold_eagle_dollar_25": Node(
        CoinData(
            nickname="Gold Eagle",
            years=list(range(1986,current_year+1)),
            weight=16.965,
            fineness=0.9167,
            precious_metal_weight=weights.Weight(0.5,weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="United States",
            face_value=25,
            denomination="Dollar",
        )
    ),
    "american_gold_eagle_dollar_50": Node(
        CoinData(
            nickname="Gold Eagle",
            years=list(range(1986,current_year+1)),
            weight=33.931,
            fineness=0.9167,
            precious_metal_weight=weights.Weight(1,weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="United States",
            face_value=50,
            denomination="Dollar",
        )
    ),
    "american_gold_buffalo_dollar_5": Node(
        CoinData(
            nickname="Gold Buffalo",
            years=[2008],
            weight=3.11,
            fineness=0.9999,
            precious_metal_weight=weights.Weight(0.1,weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="United States",
            face_value=5,
            denomination="Dollar",
        )
    ),
    "american_gold_buffalo_dollar_10": Node(
        CoinData(
            nickname="Gold Buffalo",
            years=[2008],
            weight=7.776,
            fineness=0.9999,
            precious_metal_weight=weights.Weight(0.25,weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="United States",
            face_value=10,
            denomination="Dollar",
        )
    ),
    "american_gold_buffalo_dollar_25": Node(
        CoinData(
            nickname="Gold Buffalo",
            years=[2008],
            weight=15.552,
            fineness=0.9999,
            precious_metal_weight=weights.Weight(0.5,weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="United States",
            face_value=25,
            denomination="Dollar",
        )
    ),
    "american_gold_buffalo_dollar_50": Node(
        CoinData(
            nickname="Gold Buffalo",
            years=list(range(2006,current_year+1)),
            weight=31.11,
            fineness=0.9999,
            precious_metal_weight=weights.Weight(1,weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="United States",
            face_value=50,
            denomination="Dollar",
        )
    ),
    "american_platinum_eagle_dollar_10": Node(
        CoinData(
            nickname="Platinum Eagle",
            years=list(range(1997,2009)),
            weight=3.11,
            fineness=0.9995,
            precious_metal_weight=weights.Weight(0.1,weights.Units.TROY_OUNCES),
            metal=Metals.PLATINUM,
            country="United States",
            face_value=10,
            denomination="Dollar",
        )
    ),
    "american_platinum_eagle_dollar_25": Node(
        CoinData(
            nickname="Platinum Eagle",
            years=list(range(1997,2009)),
            weight=7.778,
            fineness=0.9995,
            precious_metal_weight=weights.Weight(0.25,weights.Units.TROY_OUNCES),
            metal=Metals.PLATINUM,
            country="United States",
            face_value=25,
            denomination="Dollar",
        )
    ),
    "american_platinum_eagle_dollar_50": Node(
        CoinData(
            nickname="Platinum Eagle",
            years=list(range(1997,2009)),
            weight=15.56,
            fineness=0.9995,
            precious_metal_weight=weights.Weight(0.5,weights.Units.TROY_OUNCES),
            metal=Metals.PLATINUM,
            country="United States",
            face_value=50,
            denomination="Dollar",
        )
    ),
    "american_platinum_eagle_dollar_100": Node(
        CoinData(
            nickname="Platinum Eagle",
            years=list(range(1997,current_year+1)),
            weight=31.12,
            fineness=0.9995,
            precious_metal_weight=weights.Weight(1,weights.Units.TROY_OUNCES),
            metal=Metals.PLATINUM,
            country="United States",
            face_value=100,
            denomination="Dollar",
        )
    ),
    "american_palladium_eagle_dollar_25": Node(
        CoinData(
            nickname="Palladium Eagle",
            years=list(range(2017,current_year+1)),
            weight=31.12,
            fineness=0.9995,
            precious_metal_weight=weights.Weight(1,weights.Units.TROY_OUNCES),
            metal=Metals.PALLADIUM,
            country="United States",
            face_value=25,
            denomination="Dollar",
        )
    ),
}

values = {
    # United States
    "dime": NamedList(AN("Dime",["Dimes","10"]), ["barber_dime", "mercury_dime", "roosevelt_dime"],"10"),
    "quarter": NamedList(
        AN("Quarter",["Quarters","25"]),
        ["barber_quarter", "standing_liberty_quarter", "washington_quarter"],
        "25",
    ),
    "half": NamedList(
        AN("Half",["Halves","50"]),
        [
            "walking_liberty_half",
            "benjamin_half",
            "kennedy_half_1",
            "kennedy_half_2",
        ],
        "50",
    ),
    "dollar": NamedList(AN("Dollar",["Dollars","1"]), ["morgan_dollar", "peace_dollar"],"1"),
    "american_bullion_fractional_1_10": NamedList(AN("1/10 Oz Bullion",["1/10","0.1"]),["american_gold_eagle_dollar_5","american_gold_buffalo_dollar_5","american_platinum_eagle_dollar_10"],"0"),
    "american_bullion_fractional_1_4": NamedList(AN("1/4 Oz Bullion",["1/4","0.25"]),["american_gold_eagle_dollar_10","american_gold_buffalo_dollar_10","american_platinum_eagle_dollar_25"],"1"),
    "american_bullion_fractional_1_2": NamedList(AN("1/2 Oz Bullion",["1/2","0.5"]),["american_gold_eagle_dollar_25","american_gold_buffalo_dollar_25","american_platinum_eagle_dollar_50"],"2"),
    "american_bullion_1": NamedList(AN("1 Oz Bullion",["1"]),["american_gold_eagle_dollar_50","american_gold_buffalo_dollar_50","american_platinum_eagle_dollar_100","american_palladium_eagle_dollar_25"],"3"),
}

denominations = {
    # United States
    "cents": NamedList(AN("Cent","Cents"), ["dime", "quarter", "half"]),
    "dollar": NamedList(AN("Dollar","Dollars"), ["dollar"]),
    "american_bullion": TaggedList(AN("Bullion","Eagles"),["american_bullion_fractional_1_10","american_bullion_fractional_1_4","american_bullion_fractional_1_2","american_bullion_1"],tags=Tags.BULLION),
}

# Used to build the tree from just a coin object
coins_reverse_build = {
    "barber_dime": ("dime","cents","united_states"),
    "mercury_dime": ("dime","cents","united_states"),
    "roosevelt_dime": ("dime","cents","united_states"),
    "barber_quarter": ("quarter","cents","united_states"),
    "standing_liberty_quarter": ("quarter","cents","united_states"),
    "washington_quarter": ("quarter","cents","united_states"),
    "walking_liberty_half": ("half","cents","united_states"),
    "benjamin_half": ("half","cents","united_states"),
    "kennedy_half_1": ("half","cents","united_states"),
    "kennedy_half_2": ("half","cents","united_states"),
    "morgan_dollar": ("dollar","dollar","united_states"),
    "peace_dollar": ("dollar","dollar","united_states"),
    "american_gold_eagle_dollar_5": ("american_bullion_fractional_1_10","american_bullion","united_states"),
    "american_gold_buffalo_dollar_5": ("american_bullion_fractional_1_10","american_bullion","united_states"),
    "american_platinum_eagle_dollar_10": ("american_bullion_fractional_1_10","american_bullion","united_states"),
    "american_gold_eagle_dollar_10": ("american_bullion_fractional_1_4","american_bullion","united_states"),
    "american_gold_buffalo_dollar_10": ("american_bullion_fractional_1_4","american_bullion","united_states"),
    "american_platinum_eagle_dollar_25": ("american_bullion_fractional_1_4","american_bullion","united_states"),
    "american_gold_eagle_dollar_25": ("american_bullion_fractional_1_2","american_bullion","united_states"),
    "american_gold_buffalo_dollar_25": ("american_bullion_fractional_1_2","american_bullion","united_states"),
    "american_platinum_eagle_dollar_50": ("american_bullion_fractional_1_2","american_bullion","united_states"),
    "american_gold_eagle_dollar_50": ("american_bullion_1","american_bullion","united_states"),
    "american_gold_buffalo_dollar_50": ("american_bullion_1","american_bullion","united_states"),
    "american_platinum_eagle_dollar_100": ("american_bullion_1","american_bullion","united_states"),
    "american_palladium_eagle_dollar_25": ("american_bullion_1","american_bullion","united_states"),
}

# Indicates which coins are made of silver.
silver_coins = [
    "barber_dime",
    "mercury_dime",
    "roosevelt_dime",
    "barber_quarter",
    "standing_liberty_quarter",
    "washington_quarter",
    "walking_liberty_half",
    "benjamin_half",
    "kennedy_half_1",
    "kennedy_half_2",
    "morgan_dollar",
    "peace_dollar",
]

# Indicates which coins are made of gold.
gold_coins = [
    "american_gold_eagle_dollar_5",
    "american_gold_buffalo_dollar_5",
    "american_gold_eagle_dollar_10",
    "american_gold_buffalo_dollar_10",
    "american_gold_eagle_dollar_25",
    "american_gold_buffalo_dollar_25",
    "american_gold_eagle_dollar_50",
    "american_gold_buffalo_dollar_50",
]

# Indicates which coins are made of platinum.
platinum_coins = [
    "american_platinum_eagle_dollar_10",
    "american_platinum_eagle_dollar_25",
    "american_platinum_eagle_dollar_50",
    "american_platinum_eagle_dollar_100",
]

# Indicates which coins are made of palladium.
palladium_coins = [
    "american_palladium_eagle_dollar_25",
]
