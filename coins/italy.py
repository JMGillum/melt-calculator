from coinData import CoinData
from tree.node import Node
from metals import Metals
from config import current_year
import weights
from coins.namedList import NamedList
from alternativeNames import AlternativeNames as AN

coins = {
    # Italy
    "centesimi_20": Node(
        CoinData(
            years=list(range(1863, 1918)),
            weight=1,
            fineness=0.835,
            metal=Metals.SILVER,
            country="Italy",
            face_value=20,
            denomination="Centesimi",
        )
    ),
    "centesimi_50": Node(
        CoinData(
            years=list(range(1863, 1918)),
            weight=2.5,
            fineness=0.835,
            metal=Metals.SILVER,
            country="Italy",
            face_value=50,
            denomination="Centesimi",
        )
    ),
    "lira_1": Node(
        CoinData(
            years=list(range(1863, 1918)),
            weight=5,
            fineness=0.835,
            metal=Metals.SILVER,
            country="Italy",
            face_value=1,
            denomination="Lire",
        )
    ),
    "lira_2": Node(
        CoinData(
            years=list(range(1863, 1918)),
            weight=10,
            fineness=0.835,
            metal=Metals.SILVER,
            country="Italy",
            face_value=2,
            denomination="Lire",
        )
    ),
    "lira_5_1": Node(
        CoinData(
            years=list(range(1863, 1918)),
            weight=25,
            fineness=0.9,
            metal=Metals.SILVER,
            country="Italy",
            face_value=5,
            denomination="Lire",
        )
    ),
    "lira_5_2": Node(
        CoinData(
            years=list(range(1926, 1942)),
            weight=5,
            fineness=0.835,
            metal=Metals.SILVER,
            country="Italy",
            face_value=5,
            denomination="Lire",
        )
    ),
    "lira_5_3": Node(
        CoinData(
            years=list(range(1861, 1928)),
            weight=1.6129,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Italy",
            face_value=5,
            denomination="Lire",
        )
    ),
    "lira_10_1": Node(
        CoinData(
            years=list(range(1926, 1942)),
            weight=10,
            fineness=0.835,
            metal=Metals.SILVER,
            country="Italy",
            face_value=10,
            denomination="Lire",
        )
    ),
    "lira_10_2": Node(
        CoinData(
            years=list(range(1861, 1928)),
            weight=3.2258,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Italy",
            face_value=10,
            denomination="Lire",
        )
    ),
    "lira_20_1": Node(
        CoinData(
            years=list(range(1927, 1935)),
            weight=15,
            fineness=0.800,
            metal=Metals.SILVER,
            country="Italy",
            face_value=20,
            denomination="Lire",
        )
    ),
    "lira_20_2": Node(
        CoinData(
            years=list(range(1936, 1942)),
            weight=20,
            fineness=0.800,
            metal=Metals.SILVER,
            country="Italy",
            face_value=20,
            denomination="Lire",
        )
    ),
    "lira_20_3": Node(
        CoinData(
            years=list(range(1861, 1928)),
            weight=6.4516,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Italy",
            face_value=20,
            denomination="Lire",
        )
    ),
    "lira_50_1": Node(
        CoinData(
            years=list(range(1861, 1928)),
            weight=16.129,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Italy",
            face_value=0,
            denomination="Lire",
        )
    ),
    "lira_50_2": Node(
        CoinData(
            years=list(range(1931,1937)),
            weight=4.3995,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Italy",
            face_value=50,
            denomination="Lire",
        )
    ),
    "lira_100_1": Node(
        CoinData(
            years=list(range(1861, 1928)),
            weight=32.2581,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Italy",
            face_value=100,
            denomination="Lire",
        )
    ),
    "lira_100_2": Node(
        CoinData(
            years=list(range(1931,1937)),
            weight=8.799,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Italy",
            face_value=100,
            denomination="Lire",
        )
    ),
    "lira_100_3": Node(
        CoinData(
            years=[1937],
            weight=5.1966,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Italy",
            face_value=100,
            denomination="Lire",
        )
    ),
    "lira_500": Node(
        CoinData(
            years=list(range(1958, 2002)),
            weight=11,
            fineness=0.835,
            metal=Metals.SILVER,
            country="Italy",
            face_value=500,
            denomination="Lire",
        )
    ),
}

values = {
    # Italy
    "centesimi_20": NamedList("20", ["centesimi_20"]),
    "centesimi_50": NamedList("50", ["centesimi_50"]),
    "lira_1": NamedList("1", ["lira_1"]),
    "lira_2": NamedList("2", ["lira_2"]),
    "lira_5": NamedList("5", ["lira_5_1","lira_5_2","lira_5_3"]),
    "lira_10": NamedList("10", ["lira_10_1","lira_10_2"]),
    "lira_20": NamedList("20", ["lira_20_1","lira_20_2","lira_20_3"]),
    "lira_50": NamedList("50", ["lira_50_1","lira_50_2"]),
    "lira_100": NamedList("100", ["lira_100_1","lira_100_2","lira_100_3"]),
    "lira_500": NamedList("500", ["lira_500"]),
}

denominations = {
    # Italy
    "centesimi": NamedList(AN("Centesimo",["Centesimi","Centesimis"]), ["centesimi_20","centesimi_50"]),
    "lira": NamedList(AN("Lira",["Lire","Liras"]),["lira_1","lira_2","lira_5","lira_10","lira_20","lira_50","lira_100","lira_500"]),
}

coins_reverse_build = {
    "centesimi_20": ("centesimi_20","centesimi","italy"),
    "centesimi_50": ("centesimi_50","centesimi","italy"),
    "lira_1": ("lira_1","lira","italy"),
    "lira_2": ("lira_2","lira","italy"),
    "lira_5_1": ("lira_5","lira","italy"),
    "lira_5_2": ("lira_5","lira","italy"),
    "lira_5_3": ("lira_5","lira","italy"),
    "lira_10_1": ("lira_10","lira","italy"),
    "lira_10_2": ("lira_10","lira","italy"),
    "lira_20_1": ("lira_20","lira","italy"),
    "lira_20_2": ("lira_20","lira","italy"),
    "lira_20_3": ("lira_20","lira","italy"),
    "lira_50_1": ("lira_50","lira","italy"),
    "lira_50_2": ("lira_50","lira","italy"),
    "lira_100_1": ("lira_100","lira","italy"),
    "lira_100_2": ("lira_100","lira","italy"),
    "lira_100_3": ("lira_100","lira","italy"),
    "lira_500": ("lira_500","lira","italy"),
}

# Indicates which coins are made of silver.
silver_coins = [
    "centesimi_20",
    "centesimi_50",
    "lira_1",
    "lira_2",
    "lira_5_1",
    "lira_5_2",
    "lira_10_1",
    "lira_20_1",
    "lira_20_2",
    "lira_500",
]

# Indicates which coins are made of gold.
gold_coins = [
    "lira_5_3",
    "lira_10_2",
    "lira_20_3",
    "lira_50_1",
    "lira_50_2",
    "lira_100_1",
    "lira_100_2",
    "lira_100_3",
]

# Indicates which coins are made of platinum.
platinum_coins = [
]

# Indicates which coins are made of palladium.
palladium_coins = [
]
