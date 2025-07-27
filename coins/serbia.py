
"""
   Author: Josh Gillum              .
   Date: 26 July 2025              ":"         __ __
   Code: Line 29                  __|___       \ V /
                                .'      '.      | |
                                |  O       \____/  |
^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

 |->Serbia
     |->Dinar
     |  |->1
     |  |  |->serbia_dinar_1_1
     |  |->2
     |  |  |->serbia_dinar_2_1
     |  |->5
     |  |  |->serbia_dinar_5_1
     |  |->10
     |  |  |->serbia_dinar_10_1
     |  |->20
     |      |->serbia_dinar_20_1
     |->Para
         |->50
             |->serbia_para_50_1

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
    "serbia_para_50_1": Node(
        CoinData(
            years=[1875,1879] + list(range(1904,1916)),
            weight=0.835,
            fineness=2.5,
            metal=Metals.SILVER,
            country="Serbia",
            face_value=50,
            denomination="Para",
        )
    ),
    "serbia_dinar_1_1": Node(
        CoinData(
            years=[1875,1879,1897] + list(range(1904,1916)),
            weight=0.835,
            fineness=5,
            metal=Metals.SILVER,
            country="Serbia",
            face_value=1,
            denomination="Dinara",
        )
    ),
    "serbia_dinar_2_1": Node(
        CoinData(
            years=[1875,1879,1897] + list(range(1904,1916)),
            weight=0.835,
            fineness=10,
            metal=Metals.SILVER,
            country="Serbia",
            face_value=2,
            denomination="Dinara",
        )
    ),
    "serbia_dinar_5_1": Node(
        CoinData(
            years=[1879],
            weight=0.9,
            fineness=25,
            metal=Metals.SILVER,
            country="Serbia",
            face_value=5,
            denomination="Dinara",
        )
    ),
    "serbia_dinar_10_1": Node(
        CoinData(
            years=[1882],
            weight=3.2258,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Serbia",
            face_value=10,
            denomination="Dinara",
        )
    ),
    "serbia_dinar_20_1": Node(
        CoinData(
            years=[1879,1882],
            weight=6.4516,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Serbia",
            face_value=20,
            denomination="Dinara",
        )
    ),
}

# Stores NamedLists of keys from coins
values = {
        "serbia_para_50": NamedList("50",["serbia_para_50_1"]),
        "serbia_dinar_1": NamedList("1",["serbia_dinar_1_1"]),
        "serbia_dinar_2": NamedList("2",["serbia_dinar_2_1"]),
        "serbia_dinar_5": NamedList("5",["serbia_dinar_5_1"]),
        "serbia_dinar_10": NamedList("10",["serbia_dinar_10_1"]),
        "serbia_dinar_20": NamedList("20",["serbia_dinar_20_1"]),
}

# Stores NamedLists of keys from values
denominations = {
        "serbia_para": NamedList(AN("Para",["Pare"]),["serbia_para_50"]),
        "serbia_dinar": NamedList(AN("Dinar",["Dinara"]),["serbia_dinar_1","serbia_dinar_2","serbia_dinar_5","serbia_dinar_10","serbia_dinar_20"]),
}

# Stores every key inside of coins, with values of 
# tuples of (<value_id>,<denomination_id>,<country_id>)
coins_reverse_build = {
    "serbia_para_50_1": ("serbia_para_50","serbia_para","serbia"),
    "serbia_dinar_1_1": ("serbia_dinar_1","serbia_dinar","serbia"),
    "serbia_dinar_2_1": ("serbia_dinar_2","serbia_dinar","serbia"),
    "serbia_dinar_5_1": ("serbia_dinar_5","serbia_dinar","serbia"),
    "serbia_dinar_10_1": ("serbia_dinar_10","serbia_dinar","serbia"),
    "serbia_dinar_20_1": ("serbia_dinar_20","serbia_dinar","serbia"),
}

# Indicates which coins are made of silver.
silver_coins = [
    "serbia_para_50_1",
    "serbia_dinar_1_1",
    "serbia_dinar_2_1",
    "serbia_dinar_5_1",
]

# Indicates which coins are made of gold.
gold_coins = [
    "serbia_dinar_10_1",
    "serbia_dinar_20_1",
]

# Indicates which coins are made of platinum.
platinum_coins = [
]

# Indicates which coins are made of palladium.
palladium_coins = [
]
