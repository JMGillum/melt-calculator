"""
   Author: Josh Gillum              .
   Date: 26 July 2025              ":"         __ __
   Code: Line 62                  __|___       \ V /
                                .'      '.      | |
                                |  O       \____/  |
^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

 |->Russia
     |->Kopek
     |  |->5
     |  |  |->russia_kopek_5_1
     |  |  |->russia_kopek_5_2
     |  |  |->russia_kopek_5_3
     |  |->10
     |  |  |->russia_kopek_10_1
     |  |  |->russia_kopek_10_2
     |  |  |->russia_kopek_10_3
     |  |->15
     |  |  |->russia_kopek_15_1
     |  |  |->russia_kopek_15_2
     |  |->20
     |  |  |->russia_kopek_20_1
     |  |  |->russia_kopek_20_2
     |  |  |->russia_kopek_20_3
     |  |->25
     |  |  |->russia_kopek_25_1
     |  |  |->russia_kopek_25_2
     |  |  |->russia_kopek_25_3
     |  |->50
     |      |->russia_kopek_50_1
     |      |->russia_kopek_50_2
     |->Ruble
         |->1/2
         |  |->russia_ruble_fractional_1_2_1
         |->1
         |  |->russia_ruble_1_1
         |  |->russia_ruble_1_2
         |  |->russia_ruble_1_3
         |->3
         |  |->russia_ruble_3_1
         |->5
         |  |->russia_ruble_5_1
         |  |->russia_ruble_5_2
         |  |->russia_ruble_5_3
         |->7-1/2
         |  |->russia_ruble_fractional_15_2_1
         |->10
         |  |->russia_ruble_10_1
         |  |->russia_ruble_10_2
         |->15
         |  |->russia_ruble_15_1
         |->25
         |  |->russia_ruble_25_1
         |  |->russia_ruble_25_2
         |->37-1/2
             |->russia_ruble_fractional_75_2_1

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

# Stores Nodes of CoinData objects
coins = {
    "russia_kopek_5_1": Node(
        CoinData(
            years=list(range(1855,1859)),
            weight=1.0366,
            fineness=0.868,
            metal=Metals.SILVER,
            country="Russia",
            face_value=5,
            denomination="Kopeks",
        )
    ),
    "russia_kopek_5_2": Node(
        CoinData(
            years=list(range(1859,1867)),
            weight=1.0366,
            fineness=0.75,
            metal=Metals.SILVER,
            country="Russia",
            face_value=5,
            denomination="Kopeks",
        )
    ),
    "russia_kopek_5_3": Node(
        CoinData(
            years=list(range(1867,1916)),
            weight=0.8998,
            fineness=0.5,
            metal=Metals.SILVER,
            country="Russia",
            face_value=5,
            denomination="Kopeks",
        )
    ),
    "russia_kopek_10_1": Node(
        CoinData(
            years=list(range(1855,1859)),
            weight=2.07,
            fineness=0.868,
            metal=Metals.SILVER,
            country="Russia",
            face_value=10,
            denomination="Kopeks",
        )
    ),
    "russia_kopek_10_2": Node(
        CoinData(
            years=list(range(1859,1867)),
            weight=2.0732,
            fineness=0.75,
            metal=Metals.SILVER,
            country="Russia",
            face_value=10,
            denomination="Kopeks",
        )
    ),
    "russia_kopek_10_3": Node(
        CoinData(
            years=list(range(1867,1918)) + list(range(1921,1932)),
            weight=1.7996,
            fineness=0.5,
            metal=Metals.SILVER,
            country="Russia",
            face_value=10,
            denomination="Kopeks",
        )
    ),
    "russia_kopek_15_1": Node(
        CoinData(
            years=list(range(1860,1867)),
            weight=3.1097,
            fineness=0.75,
            metal=Metals.SILVER,
            country="Russia",
            face_value=15,
            denomination="Kopeks",
        )
    ),
    "russia_kopek_15_2": Node(
        CoinData(
            years=list(range(1867,1918)) + list(range(1921,1932)),
            weight=2.6994,
            fineness=0.5,
            metal=Metals.SILVER,
            country="Russia",
            face_value=15,
            denomination="Kopeks",
        )
    ),
    "russia_kopek_20_1": Node(
        CoinData(
            years=list(range(1855,1859)),
            weight=4.1463,
            fineness=0.868,
            metal=Metals.SILVER,
            country="Russia",
            face_value=20,
            denomination="Kopeks",
        )
    ),
    "russia_kopek_20_2": Node(
        CoinData(
            years=list(range(1859,1867)),
            weight=4.1463,
            fineness=0.75,
            metal=Metals.SILVER,
            country="Russia",
            face_value=20,
            denomination="Kopeks",
        )
    ),
    "russia_kopek_20_3": Node(
        CoinData(
            years=list(range(1867,1918)) + list(range(1921,1932)),
            weight=3.5992,
            fineness=0.5,
            metal=Metals.SILVER,
            country="Russia",
            face_value=20,
            denomination="Kopeks",
        )
    ),
    "russia_kopek_25_1": Node(
        CoinData(
            years=list(range(1855,1859)),
            weight=5.183,
            fineness=0.868,
            metal=Metals.SILVER,
            country="Russia",
            face_value=25,
            denomination="Kopeks",
)
    ),
    "russia_kopek_25_2": Node(
        CoinData(
            years=list(range(1859,1886)),
            weight=5.1829,
            fineness=0.868,
            metal=Metals.SILVER,
            country="Russia",
            face_value=25,
            denomination="Kopeks",
        )
    ),
    "russia_kopek_25_3": Node(
        CoinData(
            years=list(range(1886,1902)),
            weight=4.9987,
            fineness=0.9,
            metal=Metals.SILVER,
            country="Russia",
            face_value=25,
            denomination="Kopeks",
        )
    ),
    "russia_kopek_50_1": Node(
        CoinData(
            years=list(range(1859,1886)),
            weight=10.3658,
            fineness=0.868,
            metal=Metals.SILVER,
            country="Russia",
            face_value=50,
            denomination="Kopeks",
        )
    ),
    "russia_kopek_50_2": Node(
        CoinData(
            years=list(range(1886,1915)) + [1921,1922] + list(range(1924,1928)),
            weight=9.9979,
            fineness=0.9,
            metal=Metals.SILVER,
            country="Russia",
            face_value=50,
            denomination="Kopeks",
        )
    ),
    "russia_ruble_fractional_1_2_1": Node(
        CoinData(
            years=list(range(1855,1859)),
            weight=10.366,
            fineness=0.868,
            metal=Metals.SILVER,
            country="Russia",
            face_value=0.5,
            denomination="Ruble",
        )
    ),
    "russia_ruble_1_1": Node(
        CoinData(
            years=list(range(1855,1859)),
            weight=20.73,
            fineness=0.868,
            metal=Metals.SILVER,
            country="Russia",
            face_value=1,
            denomination="Ruble",
        )
    ),
    "russia_ruble_1_2": Node(
        CoinData(
            years=list(range(1859,1886)),
            weight=20.7316,
            fineness=0.868,
            metal=Metals.SILVER,
            country="Russia",
            face_value=1,
            denomination="Ruble",
        )
    ),
    "russia_ruble_1_3": Node(
        CoinData(
            years=list(range(1886,1916))+[1921,1922,1924],
            weight=19.9957,
            fineness=0.9,
            metal=Metals.SILVER,
            country="Russia",
            face_value=1,
            denomination="Ruble",
        )
    ),
    "russia_ruble_3_1": Node(
        CoinData(
            years=list(range(1869,1886)),
            weight=3.9264,
            fineness=0.917,
            metal=Metals.GOLD,
            country="Russia",
            face_value=3,
            denomination="Ruble",
        )
    ),
    "russia_ruble_5_1": Node(
        CoinData(
            years=list(range(1855,1886)),
            weight=6.554,
            fineness=0.917,
            metal=Metals.GOLD,
            country="Russia",
            face_value=5,
            denomination="Ruble",
        )
    ),
    "russia_ruble_5_2": Node(
        CoinData(
            years=list(range(1886,1898)),
            weight=6.4519,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Russia",
            face_value=5,
            denomination="Ruble",
        )
    ),
    "russia_ruble_5_3": Node(
        CoinData(
            years=list(range(1897,1912)),
            weight=4.3012,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Russia",
            face_value=5,
            denomination="Ruble",
        )
    ),
    "russia_ruble_fractional_15_2_1": Node(
        CoinData(
            years=[1897],
            weight=6.4518,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Russia",
            face_value=7.5,
            denomination="Ruble",
        )
    ),
    "russia_ruble_10_1": Node(
        CoinData(
            years=list(range(1886,1898)),
            weight=12.9039,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Russia",
            face_value=10,
            denomination="Ruble",
        )
    ),
    "russia_ruble_10_2": Node(
        CoinData(
            years=list(range(1897,1912)),
            weight=8.6024,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Russia",
            face_value=10,
            denomination="Ruble",
        )
    ),
    "russia_ruble_15_1": Node(
        CoinData(
            years=[1897],
            weight=12.9036,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Russia",
            face_value=15,
            denomination="Ruble",
        )
    ),
    "russia_ruble_25_1": Node(
        CoinData(
            years=[1876],
            weight=32.72,
            fineness=0.917,
            metal=Metals.GOLD,
            country="Russia",
            face_value=25,
            denomination="Ruble",
        )
    ),
    "russia_ruble_25_2": Node(
        CoinData(
            years=[1896,1908],
            weight=32.5295,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Russia",
            face_value=25,
            denomination="Ruble",
        )
    ),
    "russia_ruble_fractional_75_2_1": Node(
        CoinData(
            years=[1902],
            weight=32.259,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Russia",
            face_value=37.5,
            denomination="Ruble",
        )
    ),
}

# Stores NamedLists of keys from coins
values = {
        "russia_kopek_5": NamedList("5",["russia_kopek_5_1","russia_kopek_5_2","russia_kopek_5_3"]),
        "russia_kopek_10": NamedList("10",["russia_kopek_10_1","russia_kopek_10_2","russia_kopek_10_3"]),
        "russia_kopek_15": NamedList("15",["russia_kopek_15_1","russia_kopek_15_2"]),
        "russia_kopek_20": NamedList("20",["russia_kopek_20_1","russia_kopek_20_2","russia_kopek_20_3"]),
        "russia_kopek_25": NamedList("25",["russia_kopek_25_1","russia_kopek_25_2","russia_kopek_25_3"]),
        "russia_kopek_50": NamedList("50",["russia_kopek_50_1","russia_kopek_50_2"]),
        "russia_ruble_fractional_1_2": NamedList(AN("1/2 (Poltina)",["Poltina","1/2","0.5"]),["russia_ruble_fractional_1_2_1"],"0"),
        "russia_ruble_1": NamedList("1",["russia_ruble_1_1","russia_ruble_1_2","russia_ruble_1_3"]),
        "russia_ruble_3": NamedList("3",["russia_ruble_3_1"]),
        "russia_ruble_5": NamedList("5",["russia_ruble_5_1","russia_ruble_5_2","russia_ruble_5_3"]),
        "russia_ruble_fractional_15_2": NamedList(AN("7-1/2",["7 1/2","7.5","15/2"]),["russia_ruble_fractional_15_2_1"],"8"),
        "russia_ruble_10": NamedList("10",["russia_ruble_10_1","russia_ruble_10_2"]),
        "russia_ruble_15": NamedList("15",["russia_ruble_15_1"]),
        "russia_ruble_25": NamedList("25",["russia_ruble_25_1","russia_ruble_25_2"]),
        "russia_ruble_fractional_75_2": NamedList(AN("37-1/2",["37 1/2","37.5","75/2"]),["russia_ruble_fractional_75_2_1"],"38"),
}

# Stores NamedLists of keys from values
denominations = {
        "russia_kopek": NamedList(AN("Kopek",["Kopeks","Kopeck","Kopecks"]),["russia_kopek_5","russia_kopek_10","russia_kopek_15","russia_kopek_20","russia_kopek_25","russia_kopek_50"]),
        "russia_ruble": NamedList(AN("Ruble","Rubles"),["russia_ruble_fractional_1_2","russia_ruble_1","russia_ruble_3","russia_ruble_5","russia_ruble_fractional_15_2","russia_ruble_10","russia_ruble_15","russia_ruble_25","russia_ruble_fractional_75_2"])
}

# Stores every key inside of coins, with values of 
# tuples of (<value_id>,<denomination_id>,<country_id>)
coins_reverse_build = {
    "russia_kopek_5_1": ("russia_kopek_5","russia_kopek","russia"),
    "russia_kopek_5_2": ("russia_kopek_5","russia_kopek","russia"),
    "russia_kopek_5_3": ("russia_kopek_5","russia_kopek","russia"),
    "russia_kopek_10_1": ("russia_kopek_10","russia_kopek","russia"),
    "russia_kopek_10_2": ("russia_kopek_10","russia_kopek","russia"),
    "russia_kopek_10_3": ("russia_kopek_10","russia_kopek","russia"),
    "russia_kopek_15_1": ("russia_kopek_15","russia_kopek","russia"),
    "russia_kopek_15_2": ("russia_kopek_15","russia_kopek","russia"),
    "russia_kopek_20_1": ("russia_kopek_20","russia_kopek","russia"),
    "russia_kopek_20_2": ("russia_kopek_20","russia_kopek","russia"),
    "russia_kopek_20_3": ("russia_kopek_20","russia_kopek","russia"),
    "russia_kopek_25_1": ("russia_kopek_25","russia_kopek","russia"),
    "russia_kopek_25_2": ("russia_kopek_25","russia_kopek","russia"),
    "russia_kopek_25_3": ("russia_kopek_25","russia_kopek","russia"),
    "russia_kopek_50_1": ("russia_kopek_50","russia_kopek","russia"),
    "russia_kopek_50_2": ("russia_kopek_50","russia_kopek","russia"),
    "russia_ruble_fractional_1_2_1": ("russia_ruble_fractional_1_2","russia_ruble","russia"),
    "russia_ruble_1_1": ("russia_ruble_1","russia_ruble","russia"),
    "russia_ruble_1_2": ("russia_ruble_1","russia_ruble","russia"),
    "russia_ruble_1_3": ("russia_ruble_1","russia_ruble","russia"),
    "russia_ruble_3_1": ("russia_ruble_3","russia_ruble","russia"),
    "russia_ruble_5_1": ("russia_ruble_5","russia_ruble","russia"),
    "russia_ruble_5_2": ("russia_ruble_5","russia_ruble","russia"),
    "russia_ruble_5_3": ("russia_ruble_5","russia_ruble","russia"),
    "russia_ruble_fractional_15_2_1": ("russia_ruble_fractional_15_2","russia_ruble","russia"),
    "russia_ruble_10_1": ("russia_ruble_10","russia_ruble","russia"),
    "russia_ruble_10_2": ("russia_ruble_10","russia_ruble","russia"),
    "russia_ruble_15_1": ("russia_ruble_15","russia_ruble","russia"),
    "russia_ruble_25_1": ("russia_ruble_25","russia_ruble","russia"),
    "russia_ruble_25_2": ("russia_ruble_25","russia_ruble","russia"),
    "russia_ruble_fractional_75_2_1": ("russia_ruble_fractional_75_2","russia_ruble","russia"),
}

# Indicates which coins are made of silver.
silver_coins = [
    "russia_kopek_5_1",
    "russia_kopek_5_2",
    "russia_kopek_5_3",
    "russia_kopek_10_1",
    "russia_kopek_10_2",
    "russia_kopek_10_3",
    "russia_kopek_15_1",
    "russia_kopek_15_2",
    "russia_kopek_20_1",
    "russia_kopek_20_2",
    "russia_kopek_20_3",
    "russia_kopek_25_1",
    "russia_kopek_25_2",
    "russia_kopek_25_3",
    "russia_kopek_50_1",
    "russia_kopek_50_2",
    "russia_ruble_fractional_1_2_1",
    "russia_ruble_1_1",
    "russia_ruble_1_2",
    "russia_ruble_1_3",
]

# Indicates which coins are made of gold.
gold_coins = [
    "russia_ruble_3_1",
    "russia_ruble_5_1",
    "russia_ruble_5_2",
    "russia_ruble_5_3",
    "russia_ruble_fractional_15_2_1",
    "russia_ruble_10_1",
    "russia_ruble_10_2",
    "russia_ruble_15_1",
    "russia_ruble_25_1",
    "russia_ruble_25_2",
    "russia_ruble_fractional_75_2_1",
]

# Indicates which coins are made of platinum.
platinum_coins = [
]

# Indicates which coins are made of palladium.
palladium_coins = [
]
