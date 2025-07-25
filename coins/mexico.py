from coinData import CoinData
from tree.node import Node
from metals import Metals
from config import current_year
import weights
from coins.namedList import NamedList

coins = {
    # Mexico
    "peso_1": Node(
        CoinData(
            years=[
                x
                for x in list(range(1920, 1946))
                if x not in list(range(1928, 1932)) + [1936, 1937, 1939, 1941, 1942]
            ],
            weight=16.66,
            fineness=0.72,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=1,
            denomination="Peso",
        )
    ),
}

values = {
    # Mexico
    "peso_1": NamedList("1", ["peso_1"]),
}

denominations = {
    # Mexico
    "peso": NamedList("Peso", ["peso_1"]),
}

coins_reverse_build = {
    "peso_1": ("peso_1","peso","mexico"),
}

silver_coins = [
    "peso_1",
]

gold_coins = []

platinum_coins = []

palladium_coins = []
