"""
   Author: Josh Gillum              .
   Date: 25 July 2025              ":"         __ __
   Code: Line 37                  __|___       \ V /
                                .'      '.      | |
                                |  O       \____/  |
^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

 |->Switzerland
     |->Franc
         |->1/2
         |  |->swiss_franc_1_2_1
         |  |->swiss_franc_1_2_2
         |  |->swiss_franc_1_2_3
         |->1
         |  |->swiss_franc_1_1
         |  |->swiss_franc_1_2
         |  |->swiss_franc_1_3
         |->2
         |  |->swiss_franc_2_1
         |  |->swiss_franc_2_2
         |->5
         |  |->swiss_franc_5_1
         |  |->swiss_franc_5_2
         |->10
         |  |->swiss_franc_10
         |->20
         |  |->swiss_franc_20
         |->100
             |->swiss_franc_100_1
             |->swiss_franc_100_2
             |->swiss_franc_100_3

^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
"""

from coinData import CoinData
from tree.node import Node
from metals import Metals
from config import current_year
import weights
from alternativeNames import AlternativeNames as AN
from coins.namedList import NamedList
from coins.taggedList import TaggedList
from coins.tags import Tags

coins = {
    "swiss_franc_1_2_1": Node(
        CoinData(
            years=list(range(1850, 1858)),
            weight=2.5,
            fineness=0.9,
            metal=Metals.SILVER,
            country="Switzerland",
            face_value=0.5,
            denomination="Franc",
        )
    ),
    "swiss_franc_1_2_2": Node(
        CoinData(
            years=list(range(1860, 1862)),
            weight=5.00,
            fineness=0.8,
            metal=Metals.SILVER,
            country="Switzerland",
            face_value=0.5,
            denomination="Franc",
        )
    ),
    "swiss_franc_1_2_3": Node(
        CoinData(
            years=list(range(1874, 1968)),
            weight=2.5,
            fineness=0.835,
            metal=Metals.SILVER,
            country="Switzerland",
            face_value=0.5,
            denomination="Franc",
        )
    ),
    "swiss_franc_1_1": Node(
        CoinData(
            years=list(range(1850, 1858)),
            weight=5.0,
            fineness=0.9,
            metal=Metals.SILVER,
            country="Switzerland",
            face_value=1,
            denomination="Franc",
        )
    ),
    "swiss_franc_1_2": Node(
        CoinData(
            years=list(range(1860, 1862)),
            weight=10.0,
            fineness=0.8,
            metal=Metals.SILVER,
            country="Switzerland",
            face_value=1,
            denomination="Franc",
        )
    ),
    "swiss_franc_1_3": Node(
        CoinData(
            years=list(range(1874, 1968)),
            weight=5.0,
            fineness=0.835,
            metal=Metals.SILVER,
            country="Switzerland",
            face_value=1,
            denomination="Franc",
        )
    ),
    "swiss_franc_2_1": Node(
        CoinData(
            years=list(range(1850, 1858)),
            weight=10.0,
            fineness=0.9,
            metal=Metals.SILVER,
            country="Switzerland",
            face_value=2,
            denomination="Franc",
        )
    ),
    "swiss_franc_2_2": Node(
        CoinData(
            years=list(range(1874, 1968)),
            weight=10.0,
            fineness=0.835,
            metal=Metals.SILVER,
            country="Switzerland",
            face_value=2,
            denomination="Franc",
        )
    ),
    "swiss_franc_5_1": Node(
        CoinData(
            years=list(range(1850, 1929)),
            weight=25,
            fineness=0.9,
            metal=Metals.SILVER,
            country="Switzerland",
            face_value=5,
            denomination="Franc",
        )
    ),
    "swiss_franc_5_2": Node(
        CoinData(
            years=list(range(1931, 1970)),
            weight=15,
            fineness=0.835,
            metal=Metals.SILVER,
            country="Switzerland",
            face_value=5,
            denomination="Franc",
        )
    ),
    "swiss_franc_10": Node(
        CoinData(
            years=list(range(1883,1950)),
            weight=3.2258,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Switzerland",
            face_value=10,
            denomination="Franc",
        )
    ),
    "swiss_franc_20": Node(
        CoinData(
            years=list(range(1883,1950)),
            weight=6.4516,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Switzerland",
            face_value=20,
            denomination="Franc",
        )
    ),
    "swiss_franc_100_1": Node(
        CoinData(
            years=list(range(1883,1950)),
            weight=32.2581,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Switzerland",
            face_value=100,
            denomination="Franc",
        )
    ),
    "swiss_franc_100_2": Node(
        CoinData(
            years=[1934],
            weight=25.9,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Switzerland",
            face_value=100,
            denomination="Franc",
        )
    ),
    "swiss_franc_100_3": Node(
        CoinData(
            years=[1939],
            weight=17.5,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Switzerland",
            face_value=100,
            denomination="Franc",
        )
    ),
}

values = {
    "swiss_franc_fractional_1_2": NamedList(AN("1/2",["0.5"]), ["swiss_franc_1_2_1","swiss_franc_1_2_2","swiss_franc_1_2_3"],"0"),
    "swiss_franc_1": NamedList("1", ["swiss_franc_1_1","swiss_franc_1_2","swiss_franc_1_3"]),
    "swiss_franc_2": NamedList("2", ["swiss_franc_2_1","swiss_franc_2_2"]),
    "swiss_franc_5": NamedList("5", ["swiss_franc_5_1","swiss_franc_5_2"]),
    "swiss_franc_10": NamedList("10", ["swiss_franc_10"]),
    "swiss_franc_20": NamedList("20", ["swiss_franc_20"]),
    "swiss_franc_100": NamedList("100", ["swiss_franc_100_1","swiss_franc_100_2","swiss_franc_100_3"]),
}

denominations = {
    # Italy
    "swiss_franc": NamedList(AN("Franc",["Francs"]), ["swiss_franc_fractional_1_2","swiss_franc_1","swiss_franc_2","swiss_franc_5","swiss_franc_10","swiss_franc_20","swiss_franc_100"]),
}

coins_reverse_build = {
    "swiss_franc_1_2_1": ("swiss_franc_fractional_1_2","swiss_franc","switzerland"),
    "swiss_franc_1_2_2": ("swiss_franc_fractional_1_2","swiss_franc","switzerland"),
    "swiss_franc_1_2_3": ("swiss_franc_fractional_1_2","swiss_franc","switzerland"),
    "swiss_franc_1_1": ("swiss_franc_1","swiss_franc","switzerland"),
    "swiss_franc_1_2": ("swiss_franc_1","swiss_franc","switzerland"),
    "swiss_franc_1_3": ("swiss_franc_1","swiss_franc","switzerland"),
    "swiss_franc_2_1": ("swiss_franc_2","swiss_franc","switzerland"),
    "swiss_franc_2_2": ("swiss_franc_2","swiss_franc","switzerland"),
    "swiss_franc_5_1": ("swiss_franc_5","swiss_franc","switzerland"),
    "swiss_franc_5_2": ("swiss_franc_5","swiss_franc","switzerland"),
    "swiss_franc_10": ("swiss_franc_10","swiss_franc","switzerland"),
    "swiss_franc_20": ("swiss_franc_20","swiss_franc","switzerland"),
    "swiss_franc_100_1": ("swiss_franc_100","swiss_franc","switzerland"),
    "swiss_franc_100_2": ("swiss_franc_100","swiss_franc","switzerland"),
    "swiss_franc_100_3": ("swiss_franc_100","swiss_franc","switzerland"),
}

# Indicates which coins are made of silver.
silver_coins = [
    "swiss_franc_1_2_1",
    "swiss_franc_1_2_2",
    "swiss_franc_1_2_3",
    "swiss_franc_1_1",
    "swiss_franc_1_2",
    "swiss_franc_1_3",
    "swiss_franc_2_1",
    "swiss_franc_2_2",
    "swiss_franc_5_1",
    "swiss_franc_5_2",
]

# Indicates which coins are made of gold.
gold_coins = [
    "swiss_franc_10",
    "swiss_franc_20",
    "swiss_franc_100_1",
    "swiss_franc_100_2",
    "swiss_franc_100_3",
]

# Indicates which coins are made of platinum.
platinum_coins = [
]

# Indicates which coins are made of palladium.
palladium_coins = [
]
