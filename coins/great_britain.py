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
    # Great Britain
    "britannia_silver_2_pound": Node(
        CoinData(
            nickname="Silver",
            years=list(range(1997,current_year+1)),
            weight=34.05,
            fineness=0.9167,
            precious_metal_weight=weights.Weight(1, weights.Units.TROY_OUNCES),
            metal=Metals.SILVER,
            country="Great Britain",
            face_value=2,
            denomination="Pounds",
        )
    ),
    "britannia_silver_1_pound": Node(
        CoinData(
            nickname="Silver",
            years=list(range(1997,current_year+1)),
            weight=17.025,
            fineness=0.9167,
            precious_metal_weight=weights.Weight(0.5, weights.Units.TROY_OUNCES),
            metal=Metals.SILVER,
            country="Great Britain",
            face_value=1,
            denomination="Pounds",
        )
    ),
    "britannia_silver_1_2_pound": Node(
        CoinData(
            nickname="Silver",
            years=list(range(1997,current_year+1)),
            weight=8.5125,
            fineness=0.9167,
            precious_metal_weight=weights.Weight(0.25, weights.Units.TROY_OUNCES),
            metal=Metals.SILVER,
            country="Great Britain",
            face_value=50,
            denomination="Pence",
        )
    ),
    "britannia_silver_1_5_pound": Node(
        CoinData(
            nickname="Silver",
            years=list(range(1997,current_year+1)),
            weight=3.405,
            fineness=0.9167,
            precious_metal_weight=weights.Weight(0.1, weights.Units.TROY_OUNCES),
            metal=Metals.SILVER,
            country="Great Britain",
            face_value=20,
            denomination="Pence",
        )
    ),
    "britannia_gold_100_pound_old": Node(
        CoinData(
            nickname="Gold (old design)",
            years=list(range(1987,2014)),
            weight=34.05,
            fineness=0.9167,
            precious_metal_weight=weights.Weight(1, weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="Great Britain",
            face_value=100,
            denomination="Pounds",
        )
    ),
    "britannia_gold_50_pound_old": Node(
        CoinData(
            nickname="Gold (old design)",
            years=list(range(1987,2014)),
            weight=17.025,
            fineness=0.9167,
            precious_metal_weight=weights.Weight(0.5, weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="Great Britain",
            face_value=50,
            denomination="Pounds",
        )
    ),
    "britannia_gold_25_pound_old": Node(
        CoinData(
            nickname="Gold (old design)",
            years=list(range(1987,2014)),
            weight=8.5125,
            fineness=0.9167,
            precious_metal_weight=weights.Weight(0.25, weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="Great Britain",
            face_value=25,
            denomination="Pounds",
        )
    ),
    "britannia_gold_10_pound_old": Node(
        CoinData(
            nickname="Gold (old design)",
            years=list(range(1987,2014)),
            weight=3.405,
            fineness=0.9167,
            precious_metal_weight=weights.Weight(0.1, weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="Great Britain",
            face_value=10,
            denomination="Pounds",
        )
    ),
    "britannia_gold_100_pound": Node(
        CoinData(
            nickname="Gold",
            years=list(range(2013,current_year+1)),
            weight=31.11,
            fineness=0.9999,
            precious_metal_weight=weights.Weight(1, weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="Great Britain",
            face_value=100,
            denomination="Pounds",
        )
    ),
    "britannia_gold_50_pound": Node(
        CoinData(
            nickname="Gold",
            years=list(range(2013,current_year+1)),
            weight=15.552,
            fineness=0.9999,
            precious_metal_weight=weights.Weight(0.5, weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="Great Britain",
            face_value=50,
            denomination="Pounds",
        )
    ),
    "britannia_gold_25_pound": Node(
        CoinData(
            nickname="Gold",
            years=list(range(2013,current_year+1)),
            weight=7.776,
            fineness=0.9999,
            precious_metal_weight=weights.Weight(0.25, weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="Great Britain",
            face_value=25,
            denomination="Pounds",
        )
    ),
    "britannia_gold_10_pound": Node(
        CoinData(
            nickname="Gold",
            years=list(range(2013,current_year+1)),
            weight=3.11,
            fineness=0.9999,
            precious_metal_weight=weights.Weight(0.1, weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="Great Britain",
            face_value=10,
            denomination="Pounds",
        )
    ),
    "britannia_platinum_100_pound": Node(
        CoinData(
            nickname="Platinum",
            years=list(range(2018,current_year+1)),
            weight=31.11,
            fineness=0.9995,
            precious_metal_weight=weights.Weight(1, weights.Units.TROY_OUNCES),
            metal=Metals.PLATINUM,
            country="Great Britain",
            face_value=100,
            denomination="Pounds",
        )
    ),
    "britannia_platinum_50_pound": Node(
        CoinData(
            nickname="Platinum",
            years=list(range(2018,current_year+1)),
            weight=15.552,
            fineness=0.9995,
            precious_metal_weight=weights.Weight(0.5, weights.Units.TROY_OUNCES),
            metal=Metals.PLATINUM,
            country="Great Britain",
            face_value=50,
            denomination="Pounds",
        )
    ),
    "britannia_platinum_25_pound": Node(
        CoinData(
            nickname="Platinum",
            years=list(range(2018,current_year+1)),
            weight=7.776,
            fineness=0.9995,
            precious_metal_weight=weights.Weight(0.25, weights.Units.TROY_OUNCES),
            metal=Metals.PLATINUM,
            country="Great Britain",
            face_value=25,
            denomination="Pounds",
        )
    ),
    "britannia_platinum_10_pound": Node(
        CoinData(
            nickname="Platinum",
            years=list(range(2018,current_year+1)),
            weight=3.11,
            fineness=0.9995,
            precious_metal_weight=weights.Weight(0.1, weights.Units.TROY_OUNCES),
            metal=Metals.PLATINUM,
            country="Great Britain",
            face_value=10,
            denomination="Pounds",
        )
    ),
}

values = {
    # Great Britain
    # Great Britain - Britannia
    "britannia_1_10": NamedList("1/10 Oz Britannia",["britannia_silver_1_5_pound","britannia_gold_10_pound_old","britannia_gold_10_pound","britannia_platinum_10_pound"],"1"),
    "britannia_1_4": NamedList("1/4 Oz Britannia",["britannia_silver_1_2_pound","britannia_gold_25_pound_old","britannia_gold_25_pound","britannia_platinum_25_pound"],"2"),
    "britannia_1_2": NamedList("1/2 Oz Britannia",["britannia_silver_1_pound","britannia_gold_50_pound_old","britannia_gold_50_pound","britannia_platinum_50_pound"],"3"),
    "britannia_1": NamedList("1 Oz Britannia",["britannia_silver_2_pound","britannia_gold_100_pound_old","britannia_gold_100_pound","britannia_platinum_100_pound"],"4"),
}

denominations = {
    # Great Britain
    "britannia": TaggedList(AN("Britannia","Britannias"),["britannia_1_10","britannia_1_4","britannia_1_2","britannia_1"],tags=Tags.BULLION),
}

coins_reverse_build = {
    "britannia_silver_1_5_pound": ("britannia_1_10","britannia","great_britain"),
    "britannia_gold_10_pound_old": ("britannia_1_10","britannia","great_britain"),
    "britannia_gold_10_pound": ("britannia_1_10","britannia","great_britain"),
    "britannia_platinum_10_pound": ("britannia_1_10","britannia","great_britain"),
    "britannia_silver_1_2_pound": ("britannia_1_4","britannia","great_britain"),
    "britannia_gold_25_pound_old": ("britannia_1_4","britannia","great_britain"),
    "britannia_gold_25_pound": ("britannia_1_4","britannia","great_britain"),
    "britannia_platinum_25_pound": ("britannia_1_4","britannia","great_britain"),
    "britannia_silver_1_pound": ("britannia_1_2","britannia","great_britain"),
    "britannia_gold_50_pound_old": ("britannia_1_2","britannia","great_britain"),
    "britannia_gold_50_pound": ("britannia_1_2","britannia","great_britain"),
    "britannia_platinum_50_pound": ("britannia_1_2","britannia","great_britain"),
    "britannia_silver_2_pound": ("britannia_1","britannia","great_britain"),
    "britannia_gold_100_pound_old": ("britannia_1","britannia","great_britain"),
    "britannia_gold_100_pound": ("britannia_1","britannia","great_britain"),
    "britannia_platinum_100_pound": ("britannia_1","britannia","great_britain"),
}

silver_coins = [
    "britannia_silver_1_5_pound",
    "britannia_silver_1_2_pound",
    "britannia_silver_1_pound",
    "britannia_silver_2_pound",
]

gold_coins = [
    "britannia_gold_10_pound_old",
    "britannia_gold_10_pound",
    "britannia_gold_25_pound_old",
    "britannia_gold_25_pound",
    "britannia_gold_50_pound_old",
    "britannia_gold_50_pound",
    "britannia_gold_100_pound_old",
    "britannia_gold_100_pound",
]


# Indicates which coins are made of platinum.
platinum_coins = [
    "britannia_platinum_10_pound",
    "britannia_platinum_25_pound",
    "britannia_platinum_50_pound",
    "britannia_platinum_100_pound",
]

palladium_coins = []
