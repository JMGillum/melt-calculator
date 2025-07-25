from coinData import CoinData
from tree.node import Node
from metals import Metals
from config import current_year
import weights
from coins.namedList import NamedList
from alternativeNames import AlternativeNames as AN

coins = {
    # Germany
    "pfennig_20": Node(
        CoinData(
            years=list(range(1873, 1920)),
            weight=1.1111,
            fineness=0.900,
            metal=Metals.SILVER,
            country="Germany",
            face_value=20,
            denomination="Pfennig",
        )
    ),
    "pfennig_50": Node(
        CoinData(
            years=list(range(1873, 1920)),
            weight=2.7777,
            fineness=0.900,
            metal=Metals.SILVER,
            country="Germany",
            face_value=50,
            denomination="Pfennig",
        )
    ),
    "mark_1_1": Node(
        CoinData(
            years=list(range(1873, 1920)),
            weight=5.5555,
            fineness=0.900,
            metal=Metals.SILVER,
            country="Germany",
            face_value=1,
            denomination="Mark",
        )
    ),
    "mark_1_2": Node(
        CoinData(
            years=list(range(1924,1934)),
            weight=5.0000,
            fineness=0.500,
            metal=Metals.SILVER,
            country="Germany",
            face_value=1,
            denomination="Mark",
        )
    ),
    "mark_2_1": Node(
        CoinData(
            years=list(range(1874, 1919)),
            weight=11.1111,
            fineness=0.900,
            metal=Metals.SILVER,
            country="Germany",
            face_value=2,
            denomination="Mark",
        )
    ),
    "mark_2_2": Node(
        CoinData(
            years=list(range(1924,1934)),
            weight=10,
            fineness=0.500,
            metal=Metals.SILVER,
            country="Germany",
            face_value=2,
            denomination="Mark",
        )
    ),
    "mark_2_3": Node(
        CoinData(
            years=list(range(1933,1940)),
            weight=8.0000,
            fineness=0.625,
            metal=Metals.SILVER,
            country="Germany",
            face_value=2,
            denomination="Mark",
        )
    ),
    "mark_3_1": Node(
        CoinData(
            years=list(range(1874, 1919)),
            weight=16.6666,
            fineness=0.900,
            metal=Metals.SILVER,
            country="Germany",
            face_value=3,
            denomination="Mark",
        )
    ),
    "mark_3_2": Node(
        CoinData(
            years=list(range(1924,1934)),
            weight=15.0,
            fineness=0.500,
            metal=Metals.SILVER,
            country="Germany",
            face_value=3,
            denomination="Mark",
        )
    ),
    "mark_5_1": Node(
        CoinData(
            years=list(range(1874, 1919)),
            weight=27.7777,
            fineness=0.900,
            metal=Metals.SILVER,
            country="Germany",
            face_value=5,
            denomination="Mark",
        )
    ),
    "mark_5_2": Node(
        CoinData(
            years=list(range(1871, 1916)),
            weight=1.9913,
            fineness=0.900,
            retention=0.97,
            metal=Metals.GOLD,
            country="Germany",
            face_value=5,
            denomination="Mark",
        )
    ),
    "mark_5_3": Node(
        CoinData(
            years=list(range(1924,1934)),
            weight=25.0000,
            fineness=0.500,
            metal=Metals.SILVER,
            country="Germany",
            face_value=5,
            denomination="Mark",
        )
    ),
    "mark_5_4": Node(
        CoinData(
            years=list(range(1933,1940)),
            weight=13.8888,
            fineness=0.900,
            metal=Metals.SILVER,
            country="Germany",
            face_value=5,
            denomination="Mark",
        )
    ),
    "mark_10": Node(
        CoinData(
            years=list(range(1871, 1916)),
            weight=3.9825,
            fineness=0.900,
            retention=0.97,
            metal=Metals.GOLD,
            country="Germany",
            face_value=10,
            denomination="Mark",
        )
    ),
    "mark_20": Node(
        CoinData(
            years=list(range(1871, 1916)),
            weight=7.965,
            fineness=0.900,
            retention=0.97,
            metal=Metals.GOLD,
            country="Germany",
            face_value=20,
            denomination="Mark",
        )
    ),
}

values = {
    # Germany
    "pfennig_20": NamedList("20",["pfennig_20"]),
    "pfennig_50": NamedList("50",["pfennig_50"]),
    "mark_1": NamedList("1",["mark_1_1","mark_1_2"]),
    "mark_2": NamedList("2",["mark_2_1","mark_2_2","mark_2_3"]),
    "mark_3": NamedList("3",["mark_3_1","mark_3_2"]),
    "mark_5": NamedList("5",["mark_5_1","mark_5_2","mark_5_3","mark_5_4"]),
    "mark_10": NamedList("10", ["mark_10"]),
    "mark_20": NamedList("20", ["mark_20"]),
}

denominations = {
    # Germany
    "pfennig": NamedList(AN("Pfennig","Pfennigs"),["pfennig_20","pfennig_50"]),
    "mark": NamedList(AN("Mark","Marks"), ["mark_1","mark_2","mark_3","mark_5","mark_10","mark_20"]),
}

coins_reverse_build = {
    "pfennig_20": ("pfennig_20","pfennig","germany"),
    "pfennig_50": ("pfennig_50","pfennig","germany"),
    "mark_1_1": ("mark_1","mark","germany"),
    "mark_1_2": ("mark_1","mark","germany"),
    "mark_2_1": ("mark_2","mark","germany"),
    "mark_2_2": ("mark_2","mark","germany"),
    "mark_2_3": ("mark_2","mark","germany"),
    "mark_3_1": ("mark_3","mark","germany"),
    "mark_3_2": ("mark_3","mark","germany"),
    "mark_5_1": ("mark_5","mark","germany"),
    "mark_5_2": ("mark_5","mark","germany"),
    "mark_5_3": ("mark_5","mark","germany"),
    "mark_5_4": ("mark_5","mark","germany"),
    "mark_10": ("mark_10","mark","germany"),
    "mark_20": ("mark_20","mark","germany"),
}

silver_coins = [
    "pfennig_20",
    "pfennig_50",
    "mark_1_1",
    "mark_1_2",
    "mark_2_1",
    "mark_2_2",
    "mark_2_3",
    "mark_3_1",
    "mark_3_2",
    "mark_5_1",
    "mark_5_3",
    "mark_5_4",
]

gold_coins = [
    "mark_5_2",
    "mark_10",
    "mark_20",
]

platinum_coins = []

palladium_coins = []
