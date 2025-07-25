from coinData import CoinData
from tree.node import Node
from metals import Metals
from config import current_year
import weights
from coins.namedList import NamedList

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
}

values = {
    # Italy
    "centesimi_20": NamedList("20", ["centesimi_20"]),
}

denominations = {
    # Italy
    "centesimi": NamedList("Centesimi", ["centesimi_20"]),
}

coins_reverse_build = {
    "centesimi_20": ("centesimi_20","centesimi","italy"),
}

silver_coins = [
    "centesimi_20",
]

gold_coins = []

platinum_coins = []

palladium_coins = []
