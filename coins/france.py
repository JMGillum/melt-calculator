"""
   Author: Josh Gillum              .
   Date: 25 July 2025              ":"         __ __
   Code: Line 43                  __|___       \ V /
                                .'      '.      | |
                                |  O       \____/  |
^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

 |->France
     |->Centime
     |  |->20
     |  |  |->centimes_20
     |  |->50
     |      |->centimes_50_1
     |      |->centimes_50_2
     |->Franc
         |->1
         |  |->franc_1_1
         |  |->franc_1_2
         |->2
         |  |->franc_2
         |->5
         |  |->franc_5_1
         |  |->franc_5_3
         |  |->franc_5_2
         |->10
         |  |->franc_10_2
         |  |->franc_10_1
         |->20
         |  |->franc_20_1
         |  |->franc_20_2
         |->50
         |  |->franc_50
         |->100
             |->franc_100_2
             |->franc_100_3
             |->franc_100_1


^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
"""

from coinData import CoinData
from tree.node import Node
from metals import Metals
from config import current_year
import weights
from coins.namedList import NamedList
from alternativeNames import AlternativeNames as AN

coins = {
    # France
    "centimes_20": Node(
        data=CoinData(
            years=list(range(1848, 1921)),
            weight=1,
            fineness=0.9,
            metal=Metals.SILVER,
            country="France",
            face_value=20,
            denomination="Centimes",
        )
    ),
    "centimes_50_1": Node(
        data=CoinData(
            years=list(range(1848, 1867)),
            weight=2.5,
            fineness=0.9,
            metal=Metals.SILVER,
            country="France",
            face_value=50,
            denomination="Centimes",
        )
    ),
    "centimes_50_2": Node(
        data=CoinData(
            years=list(range(1866, 1921)),
            weight=2.5,
            fineness=0.835,
            metal=Metals.SILVER,
            country="France",
            face_value=50,
            denomination="Centimes",
        )
    ),
    "franc_1_1": Node(
        CoinData(
            years=list(range(1848, 1867)),
            weight=5,
            fineness=0.9,
            metal=Metals.SILVER,
            country="France",
            face_value=1,
            denomination="Franc",
        )
    ),
    "franc_1_2": Node(
        CoinData(
            years=list(range(1866, 1921)),
            weight=5,
            fineness=0.835,
            metal=Metals.SILVER,
            country="France",
            face_value=1,
            denomination="Franc",
        )
    ),
    "franc_2": Node(
        CoinData(
            years=list(range(1848, 1921)),
            weight=10,
            fineness=0.9,
            metal=Metals.SILVER,
            country="France",
            face_value=2,
            denomination="Franc",
        )
    ),
    "franc_5_1": Node(
        CoinData(
            years=list(range(1848, 1921)),
            weight=25,
            fineness=0.9,
            metal=Metals.SILVER,
            country="France",
            face_value=5,
            denomination="Franc",
        )
    ),
    "franc_5_2": Node(
        CoinData(
            years=list(range(1960, 1970)),
            weight=12,
            fineness=0.835,
            metal=Metals.SILVER,
            country="France",
            face_value=5,
            denomination="Franc",
        )
    ),
    "franc_5_3": Node(
        CoinData(
            years=list(range(1848, 1915)),
            weight=1.6129,
            fineness=0.9,
            metal=Metals.GOLD,
            country="France",
            face_value=5,
            denomination="Franc",
        )
    ),
    "franc_10_1": Node(
        CoinData(
            years=[x for x in list(range(1929, 1940)) if x not in [1935, 1936]],
            weight=10,
            fineness=0.68,
            metal=Metals.SILVER,
            country="France",
            face_value=10,
            denomination="Franc",
        )
    ),
    "franc_10_2": Node(
        CoinData(
            years=list(range(1848, 1915)),
            weight=3.2258,
            fineness=0.90,
            metal=Metals.GOLD,
            country="France",
            face_value=10,
            denomination="Franc",
        )
    ),
    "franc_20_1": Node(
        data=CoinData(
            years=[x for x in range(1906, 1915)],
            weight=6.4516,
            fineness=0.9,
            metal=Metals.GOLD,
            country="France",
            face_value=20,
            denomination="Franc",
        ),
        nodes=[],
    ),
    "franc_20_2": Node(
        CoinData(
            years=list(range(1929, 1940)),
            weight=20,
            fineness=0.68,
            metal=Metals.SILVER,
            country="France",
            face_value=20,
            denomination="Franc",
        )
    ),
    "franc_50": Node(
        CoinData(
            years=list(range(1848, 1915)),
            weight=16.129,
            fineness=0.9,
            metal=Metals.GOLD,
            country="France",
            face_value=20,
            denomination="Franc",
        )
    ),
    "franc_100_1": Node(
        CoinData(
            years=[x for x in range(1982, 2001)],
            weight=15,
            fineness=0.9,
            metal=Metals.SILVER,
            country="France",
            face_value=100,
            denomination="Franc",
            retention=0.70,
        )
    ),
    "franc_100_2": Node(
        CoinData(
            years=list(range(1848, 1915)),
            weight=32.2581,
            fineness=0.9,
            metal=Metals.GOLD,
            country="France",
            face_value=100,
            denomination="Franc",
        )
    ),
    "franc_100_3": Node(
        CoinData(
            years=list(range(1929, 1937)),
            weight=6.55,
            fineness=0.9,
            metal=Metals.GOLD,
            country="France",
            face_value=100,
            denomination="Franc",
        )
    ),
}

values = {
    # France
    "centimes_20": NamedList("20", ["centimes_20"]),
    "centimes_50": NamedList("50", ["centimes_50_1", "centimes_50_2"]),
    "franc_1": NamedList("1", ["franc_1_1", "franc_1_2"]),
    "franc_2": NamedList("2", ["franc_2"]),
    "franc_5": NamedList("5", ["franc_5_1", "franc_5_2", "franc_5_3"]),
    "franc_10": NamedList("10", ["franc_10_1", "franc_10_2"]),
    "franc_20": NamedList("20", ["franc_20_1", "franc_20_2"]),
    "franc_50": NamedList("50", ["franc_50"]),
    "franc_100": NamedList("100", ["franc_100_1", "franc_100_2", "franc_100_3"]),
}

denominations = {
    # France
    "centimes": NamedList(AN("Centime","Centimes"), ["centimes_20", "centimes_50"]),
    "franc": NamedList(
        AN("Franc","Francs"),
        [
            "franc_1",
            "franc_2",
            "franc_5",
            "franc_10",
            "franc_20",
            "franc_50",
            "franc_100",
        ],
    ),
}

coins_reverse_build = {
    "centimes_20": ("centimes_20","centimes","france"),
    "centimes_50_1": ("centimes_50","centimes","france"),
    "centimes_50_2": ("centimes_50","centimes","france"),
    "franc_1_1": ("franc_1","franc","france"),
    "franc_1_2": ("franc_1","franc","france"),
    "franc_2": ("franc_2","franc","france"),
    "franc_5_1": ("franc_5","franc","france"),
    "franc_5_2": ("franc_5","franc","france"),
    "franc_5_3": ("franc_5","franc","france"),
    "franc_10_1": ("franc_10","franc","france"),
    "franc_10_2": ("franc_10","franc","france"),
    "franc_20_1": ("franc_20","franc","france"),
    "franc_20_2": ("franc_20","franc","france"),
    "franc_50": ("franc_50","franc","france"),
    "franc_100_1": ("franc_100","franc","france"),
    "franc_100_2": ("franc_100","franc","france"),
    "franc_100_3": ("franc_100","franc","france"),
}

silver_coins = [
    "centimes_20",
    "centimes_50_1",
    "centimes_50_2",
    "franc_1_1",
    "franc_1_2",
    "franc_2",
    "franc_5_1",
    "franc_5_2",
    "franc_10_1",
    "franc_20_2",
    "franc_100_1",
]

gold_coins = [
    "franc_5_3",
    "franc_10_2",
    "franc_20_1",
    "franc_50",
    "franc_100_2",
    "franc_100_3",
]

platinum_coins = []

palladium_coins = []
