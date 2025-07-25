from coinData import CoinData
from tree.node import Node
from metals import Metals
from config import current_year
import weights
from coins.namedList import NamedList

coins = {
    # South Africa
    # South Africa - Krugerrand
    "krugerrand_silver": Node(
        CoinData(
            nickname="Silver",
            years=list(range(2017, current_year+1)),
            weight=31.11,
            fineness=0.9999,
            precious_metal_weight=weights.Weight(1, weights.Units.TROY_OUNCES),
            metal=Metals.SILVER,
            country="South Africa",
            face_value=1,
            denomination="Ounce",
        )
    ),
    "krugerrand_gold_1": Node(
        CoinData(
            nickname="Gold",
            years=list(range(1967, current_year+1)),
            weight=33.93,
            fineness=0.9167,
            precious_metal_weight=weights.Weight(1, weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="South Africa",
            face_value=1,
            denomination="Ounce",
        )
    ),
    "krugerrand_gold_1_2": Node(
        CoinData(
            nickname="Gold",
            years=list(range(1980, current_year+1)),
            weight=16.965,
            fineness=0.9167,
            precious_metal_weight=weights.Weight(0.5, weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="South Africa",
            face_value=0.5,
            denomination="Ounce",
        )
    ),
    "krugerrand_gold_1_4": Node(
        CoinData(
            nickname="Gold",
            years=list(range(1970, current_year+1)),
            weight=8.4825,
            fineness=0.9167,
            precious_metal_weight=weights.Weight(0.25, weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="South Africa",
            face_value=0.25,
            denomination="Ounce",
        )
    ),
    "krugerrand_gold_1_10": Node(
        CoinData(
            nickname="Gold",
            years=list(range(1980, current_year+1)),
            weight=3.393,
            fineness=0.9167,
            precious_metal_weight=weights.Weight(0.1, weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="South Africa",
            face_value=0.1,
            denomination="Ounce",
        )
    ),
}

values = {
    # South Africa
    # South Africa - Krugerrand
    "krugerrand_1_10": NamedList("1/10 oz Krugerrand",["krugerrand_gold_1_10"],"1"),
    "krugerrand_1_4": NamedList("1/4 oz Krugerrand",["krugerrand_gold_1_4"],"2"),
    "krugerrand_1_2": NamedList("1/2 oz Krugerrand",["krugerrand_gold_1_2"],"3"),
    "krugerrand_1": NamedList("1 oz Krugerrand",["krugerrand_silver","krugerrand_gold_1"],"4"),
}

denominations = {
    # South Africa
    "krugerrand": NamedList("Krugerrand",["krugerrand_1","krugerrand_1_2","krugerrand_1_4","krugerrand_1_10"]),
}

coins_reverse_build = {
    "krugerrand_silver": ("krugerrand_1","krugerrand","south_africa"),
    "krugerrand_gold_1": ("krugerrand_1","krugerrand","south_africa"),
    "krugerrand_gold_1_2": ("krugerrand_1_2","krugerrand","south_africa"),
    "krugerrand_gold_1_4": ("krugerrand_1_4","krugerrand","south_africa"),
    "krugerrand_gold_1_10": ("krugerrand_1_10","krugerrand","south_africa"),
}

silver_coins = [
    "krugerrand_silver",
]

# Indicates which coins are made of gold.
gold_coins = [
    "krugerrand_gold_1",
    "krugerrand_gold_1_2",
    "krugerrand_gold_1_4",
    "krugerrand_gold_1_10",
]

platinum_coins = []

palladium_coins = []
