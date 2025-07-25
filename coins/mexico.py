"""
   Author: Josh Gillum              .
   Date: 25 July 2025              ":"         __ __
   Code: Line 84                  __|___       \ V /
                                .'      '.      | |
                                |  O       \____/  |
^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

 |->Mexico
     |->Centavo
     |  |->5
     |  |  |->mexico_centavo_5
     |  |->10
     |  |  |->mexico_centavo_10_1
     |  |  |->mexico_centavo_10_2
     |  |  |->mexico_centavo_10_3
     |  |  |->mexico_centavo_10_4
     |  |->20
     |  |  |->mexico_centavo_20_1
     |  |  |->mexico_centavo_20_2
     |  |  |->mexico_centavo_20_3
     |  |  |->mexico_centavo_20_4
     |  |->50
     |      |->mexico_centavo_50_1
     |      |->mexico_centavo_50_2
     |      |->mexico_centavo_50_3
     |      |->mexico_centavo_50_4
     |->Escudo
     |  |->1/2
     |  |  |->mexico_escudo_fractional_1_2
     |  |->1
     |  |  |->mexico_escudo_1
     |  |->2
     |  |  |->mexico_escudo_2
     |  |->4
     |  |  |->mexico_escudo_4
     |  |->8
     |      |->mexico_escudo_8
     |->Peso
     |  |->1
     |  |  |->mexico_peso_1_5
     |  |  |->mexico_peso_1_1
     |  |  |->mexico_peso_1_2
     |  |  |->mexico_peso_1_3
     |  |  |->mexico_peso_1_4
     |  |->2
     |  |  |->mexico_peso_2_2
     |  |  |->mexico_peso_2_1
     |  |->2-1/2
     |  |  |->mexico_peso_fractional_5_2_1
     |  |  |->mexico_peso_fractional_5_2_2
     |  |->5
     |  |  |->mexico_peso_5_4
     |  |  |->mexico_peso_5_5
     |  |  |->mexico_peso_5_1
     |  |  |->mexico_peso_5_2
     |  |  |->mexico_peso_5_3
     |  |->10
     |  |  |->mexico_peso_10_2
     |  |  |->mexico_peso_10_3
     |  |  |->mexico_peso_10_1
     |  |->20
     |  |  |->mexico_peso_20_1
     |  |  |->mexico_peso_20_2
     |  |->50
     |      |->mexico_peso_50
     |->Real
         |->1/4
         |  |->mexico_real_fractional_1_4
         |->1/2
         |  |->mexico_real_fractional_1_2
         |->1
         |  |->mexico_real_1
         |->2
         |  |->mexico_real_2
         |->4
         |  |->mexico_real_4
         |->8
             |->mexico_real_8

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
    "mexico_real_fractional_1_4": Node(
        CoinData(
            years=list(range(1822,1870)),
            weight=0.846,
            fineness=0.9027,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=0.25,
            denomination="Real",
        )
    ),
    "mexico_real_fractional_1_2": Node(
        CoinData(
            years=list(range(1822,1870)),
            weight=1.6921,
            fineness=0.9027,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=0.5,
            denomination="Real",
        )
    ),
    "mexico_real_1": Node(
        CoinData(
            years=list(range(1822,1870)),
            weight=3.3841,
            fineness=0.9027,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=1,
            denomination="Real",
        )
    ),
    "mexico_real_2": Node(
        CoinData(
            years=list(range(1822,1906)),
            weight=6.7683,
            fineness=0.9027,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=2,
            denomination="Reales",
        )
    ),
    "mexico_real_4": Node(
        CoinData(
            years=list(range(1822,1906)),
            weight=13.5365,
            fineness=0.9027,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=4,
            denomination="Reales",
        )
    ),
    "mexico_real_8": Node(
        CoinData(
            years=list(range(1822,1915)),
            weight=27.073,
            fineness=0.9027,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=8,
            denomination="Reales",
        )
    ),
    "mexico_escudo_fractional_1_2": Node(
        CoinData(
            years=list(range(1825,1874)),
            weight=1.6921,
            fineness=0.875,
            metal=Metals.GOLD,
            country="Mexico",
            face_value=0.5,
            denomination="Escudo",
        )
    ),
    "mexico_escudo_1": Node(
        CoinData(
            years=list(range(1825,1874)),
            weight=3.3841,
            fineness=0.875,
            metal=Metals.GOLD,
            country="Mexico",
            face_value=1,
            denomination="Escudo",
        )
    ),
    "mexico_escudo_2": Node(
        CoinData(
            years=list(range(1825,1874)),
            weight=6.7683,
            fineness=0.875,
            metal=Metals.GOLD,
            country="Mexico",
            face_value=2,
            denomination="Escudos",
        )
    ),
    "mexico_escudo_4": Node(
        CoinData(
            years=list(range(1825,1874)),
            weight=13.5365,
            fineness=0.875,
            metal=Metals.GOLD,
            country="Mexico",
            face_value=4,
            denomination="Escudos",
        )
    ),
    "mexico_escudo_8": Node(
        CoinData(
            years=list(range(1825,1874)),
            weight=27.0730,
            fineness=0.875,
            metal=Metals.GOLD,
            country="Mexico",
            face_value=8,
            denomination="Escudos",
        )
    ),
    "mexico_centavo_5": Node(
        CoinData(
            years=list(range(1863,1906)),
            weight=1.3537,
            fineness=0.9027,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=5,
            denomination="Centavos",
        )
    ),
    "mexico_centavo_10_1": Node(
        CoinData(
            years=list(range(1863,1906)),
            weight=2.7073,
            fineness=0.9027,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=10,
            denomination="Centavos",
        )
    ),
    "mexico_centavo_10_2": Node(
        CoinData(
            years=list(range(1905,1919)),
            weight=2.50,
            fineness=0.8,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=10,
            denomination="Centavos",
        )
    ),
    "mexico_centavo_10_3": Node(
        CoinData(
            years=[1918,1919],
            weight=1.8125,
            fineness=0.8,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=10,
            denomination="Centavos",
        )
    ),
    "mexico_centavo_10_4": Node(
        CoinData(
            years=list(range(1919,1946)),
            weight=1.6667,
            fineness=0.72,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=10,
            denomination="Centavos",
        )
    ),
    "mexico_centavo_20_1": Node(
        CoinData(
            years=list(range(1863,1906)),
            weight=5.4146,
            fineness=0.9027,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=20,
            denomination="Centavos",
        )
    ),
    "mexico_centavo_20_2": Node(
        CoinData(
            years=list(range(1905,1919)),
            weight=5,
            fineness=0.8,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=20,
            denomination="Centavos",
        )
    ),
    "mexico_centavo_20_3": Node(
        CoinData(
            years=[1918,1919],
            weight=3.625,
            fineness=0.8,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=20,
            denomination="Centavos",
        )
    ),
    "mexico_centavo_20_4": Node(
        CoinData(
            years=list(range(1919,1946)),
            weight=3.3333,
            fineness=0.72,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=20,
            denomination="Centavos",
        )
    ),
    "mexico_centavo_50_1": Node(
        CoinData(
            years=list(range(1905,1919)),
            weight=12.5,
            fineness=0.8,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=50,
            denomination="Centavos",
        )
    ),
    "mexico_centavo_50_2": Node(
        CoinData(
            years=[1918,1919],
            weight=9.0625,
            fineness=0.8,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=50,
            denomination="Centavos",
        )
    ),
    "mexico_centavo_50_3": Node(
        CoinData(
            years=list(range(1919,1946)),
            weight=8.3333,
            fineness=0.72,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=50,
            denomination="Centavos",
        )
    ),
    "mexico_centavo_50_4": Node(
        CoinData(
            years=[1935],
            weight=7.9733,
            fineness=0.42,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=50,
            denomination="Centavos",
        )
    ),
    "mexico_peso_1_1": Node(
        CoinData(
            years=[1918,1919],
            weight=18.125,
            fineness=0.80,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=1,
            denomination="Peso",
        )
    ),
    "mexico_peso_1_2": Node(
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
    "mexico_peso_1_3": Node(
        CoinData(
            years=[1947,1948,1949],
            weight=14,
            fineness=0.5,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=1,
            denomination="Peso",
        )
    ),
    "mexico_peso_1_4": Node(
        CoinData(
            years=list(range(1957,1968)),
            weight=16.00,
            fineness=0.10,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=1,
            denomination="Peso",
        )
    ),
    "mexico_peso_1_5": Node(
        CoinData(
            years=list(range(1870,1906)),
            weight=1.6921,
            fineness=0.875,
            metal=Metals.GOLD,
            country="Mexico",
            face_value=1,
            denomination="Peso",
        )
    ),
    "mexico_peso_2_1": Node(
        CoinData(
            years=list(range(1919,1946)),
            weight=26.6667,
            fineness=0.90,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=2,
            denomination="Peso",
        )
    ),
    "mexico_peso_2_2": Node(
        CoinData(
            years=list(range(1905,1960)),
            weight=1.6667,
            fineness=0.90,
            metal=Metals.GOLD,
            country="Mexico",
            face_value=1,
            denomination="Peso",
        )
    ),
    "mexico_peso_fractional_5_2_1": Node(
        CoinData(
            years=list(range(1870,1906)),
            weight=4.2301,
            fineness=0.875,
            metal=Metals.GOLD,
            country="Mexico",
            face_value=2.5,
            denomination="Peso",
        )
    ),
    "mexico_peso_fractional_5_2_2": Node(
        CoinData(
            years=list(range(1905,1960)),
            weight=2.0833,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Mexico",
            face_value=2.5,
            denomination="Peso",
        )
    ),
    "mexico_peso_5_1": Node(
        CoinData(
            years=list(range(1947,1950)),
            weight=30,
            fineness=0.90,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=5,
            denomination="Peso",
        )
    ),
    "mexico_peso_5_2": Node(
        CoinData(
            years=list(range(1950,1955)),
            weight=27.78,
            fineness=0.72,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=5,
            denomination="Peso",
        )
    ),
    "mexico_peso_5_3": Node(
        CoinData(
            years=list(range(1955,1960)),
            weight=18.05,
            fineness=0.72,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=5,
            denomination="Peso",
        )
    ),
    "mexico_peso_5_4": Node(
        CoinData(
            years=list(range(1870,1906)),
            weight=8.4602,
            fineness=0.875,
            metal=Metals.GOLD,
            country="Mexico",
            face_value=5,
            denomination="Peso",
        )
    ),
    "mexico_peso_5_5": Node(
        CoinData(
            years=list(range(1905,1960)),
            weight=4.1667,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Mexico",
            face_value=5,
            denomination="Peso",
        )
    ),
    "mexico_peso_10_1": Node(
        CoinData(
            years=list(range(1955,1961)),
            weight=28.88,
            fineness=0.90,
            metal=Metals.SILVER,
            country="Mexico",
            face_value=10,
            denomination="Peso",
        )
    ),
    "mexico_peso_10_2": Node(
        CoinData(
            years=list(range(1870,1906)),
            weight=16.9205,
            fineness=0.875,
            metal=Metals.GOLD,
            country="Mexico",
            face_value=10,
            denomination="Peso",
        )
    ),
    "mexico_peso_10_3": Node(
        CoinData(
            years=list(range(1905,1960)),
            weight=8.3333,
            fineness=0.90,
            metal=Metals.GOLD,
            country="Mexico",
            face_value=10,
            denomination="Peso",
        )
    ),
    "mexico_peso_20_1": Node(
        CoinData(
            years=list(range(1870,1906)),
            weight=33.8410,
            fineness=0.875,
            metal=Metals.GOLD,
            country="Mexico",
            face_value=20,
            denomination="Peso",
        )
    ),
    "mexico_peso_20_2": Node(
        CoinData(
            years=list(range(1905,1960)),
            weight=16.6667,
            fineness=0.90,
            metal=Metals.GOLD,
            country="Mexico",
            face_value=20,
            denomination="Peso",
        )
    ),
    "mexico_peso_50": Node(
        CoinData(
            years=list(range(1905,1960)),
            weight=41.6667,
            fineness=0.90,
            metal=Metals.GOLD,
            country="Mexico",
            face_value=50,
            denomination="Peso",
        )
    ),
}

values = {
    "mexico_real_fractional_1_4": NamedList(AN("1/4",["0.25"]),["mexico_real_fractional_1_4"],"-1"),
    "mexico_real_fractional_1_2": NamedList(AN("1/2",["0.5"]),["mexico_real_fractional_1_2"],"0"),
    "mexico_real_1": NamedList("1",["mexico_real_1"]),
    "mexico_real_2": NamedList("2",["mexico_real_2"]),
    "mexico_real_4": NamedList("4",["mexico_real_4"]),
    "mexico_real_8": NamedList("8",["mexico_real_8"]),
    "mexico_escudo_fractional_1_2": NamedList(AN("1/2",["0.5"]),["mexico_escudo_fractional_1_2"],"0"),
    "mexico_escudo_1": NamedList("1",["mexico_escudo_1"]),
    "mexico_escudo_2": NamedList("2",["mexico_escudo_2"]),
    "mexico_escudo_4": NamedList("4",["mexico_escudo_4"]),
    "mexico_escudo_8": NamedList("8",["mexico_escudo_8"]),
    "mexico_centavo_5": NamedList("5",["mexico_centavo_5"]),
    "mexico_centavo_10": NamedList("10",["mexico_centavo_10_1","mexico_centavo_10_2","mexico_centavo_10_3","mexico_centavo_10_4"]),
    "mexico_centavo_20": NamedList("20",["mexico_centavo_20_1","mexico_centavo_20_2","mexico_centavo_20_3","mexico_centavo_20_4"]),
    "mexico_centavo_50": NamedList("50",["mexico_centavo_50_1","mexico_centavo_50_2","mexico_centavo_50_3","mexico_centavo_50_4"]),
    "mexico_peso_1": NamedList("1", ["mexico_peso_1_1","mexico_peso_1_2","mexico_peso_1_3","mexico_peso_1_4","mexico_peso_1_5"]),
    "mexico_peso_2": NamedList("2", ["mexico_peso_2_1","mexico_peso_2_2"]),
    "mexico_peso_fractional_5_2": NamedList(AN("2-1/2",["2.5","2 1/2","5/2"]), ["mexico_peso_fractional_5_2_1","mexico_peso_fractional_5_2_2"],"3"),
    "mexico_peso_5": NamedList("5", ["mexico_peso_5_1","mexico_peso_5_2","mexico_peso_5_3","mexico_peso_5_4","mexico_peso_5_5"]),
    "mexico_peso_10": NamedList("10", ["mexico_peso_10_1","mexico_peso_10_2","mexico_peso_10_3"]),
    "mexico_peso_20": NamedList("20", ["mexico_peso_20_1","mexico_peso_20_2"]),
    "mexico_peso_50": NamedList("50", ["mexico_peso_50"]),
}

denominations = {
    "mexico_real": NamedList(AN("Real",["Reales"]),["mexico_real_fractional_1_4","mexico_real_fractional_1_2","mexico_real_1","mexico_real_2","mexico_real_4","mexico_real_8"]),
    "mexico_escudo": NamedList(AN("Escudo",["Escudos"]),["mexico_escudo_fractional_1_2","mexico_escudo_1","mexico_escudo_2","mexico_escudo_4","mexico_escudo_8"]),
    "mexico_centavo": NamedList(AN("Centavo",["Centavos"]),["mexico_centavo_5","mexico_centavo_10","mexico_centavo_20","mexico_centavo_50"]),
    "mexico_peso": NamedList(AN("Peso","Pesos"), ["mexico_peso_1","mexico_peso_2","mexico_peso_fractional_5_2","mexico_peso_5","mexico_peso_10","mexico_peso_20","mexico_peso_50"]),
}

coins_reverse_build = {
    "mexico_real_fractional_1_4": ("mexico_real_fractional_1_4","mexico_real","mexico"),
    "mexico_real_fractional_1_2": ("mexico_real_fractional_1_2","mexico_real","mexico"),
    "mexico_real_1": ("mexico_real_1","mexico_real","mexico"),
    "mexico_real_2": ("mexico_real_2","mexico_real","mexico"),
    "mexico_real_4": ("mexico_real_4","mexico_real","mexico"),
    "mexico_real_8": ("mexico_real_8","mexico_real","mexico"),
    "mexico_escudo_fractional_1_2": ("mexico_escudo_fractional_1_2","mexico_escudo","mexico"),
    "mexico_escudo_1": ("mexico_escudo_1","mexico_escudo","mexico"),
    "mexico_escudo_2": ("mexico_escudo_2","mexico_escudo","mexico"),
    "mexico_escudo_4": ("mexico_escudo_4","mexico_escudo","mexico"),
    "mexico_escudo_8": ("mexico_escudo_8","mexico_escudo","mexico"),
    "mexico_centavo_5": ("mexico_centavo_5","mexico_centavo","mexico"),
    "mexico_centavo_10_1": ("mexico_centavo_10","mexico_centavo","mexico"),
    "mexico_centavo_10_2": ("mexico_centavo_10","mexico_centavo","mexico"),
    "mexico_centavo_10_3": ("mexico_centavo_10","mexico_centavo","mexico"),
    "mexico_centavo_10_4": ("mexico_centavo_10","mexico_centavo","mexico"),
    "mexico_centavo_20_1": ("mexico_centavo_20","mexico_centavo","mexico"),
    "mexico_centavo_20_2": ("mexico_centavo_20","mexico_centavo","mexico"),
    "mexico_centavo_20_3": ("mexico_centavo_20","mexico_centavo","mexico"),
    "mexico_centavo_20_4": ("mexico_centavo_20","mexico_centavo","mexico"),
    "mexico_centavo_50_1": ("mexico_centavo_50","mexico_centavo","mexico"),
    "mexico_centavo_50_2": ("mexico_centavo_50","mexico_centavo","mexico"),
    "mexico_centavo_50_3": ("mexico_centavo_50","mexico_centavo","mexico"),
    "mexico_centavo_50_4": ("mexico_centavo_50","mexico_centavo","mexico"),
    "mexico_peso_1_1": ("mexico_peso_1","mexico_peso","mexico"),
    "mexico_peso_1_2": ("mexico_peso_1","mexico_peso","mexico"),
    "mexico_peso_1_3": ("mexico_peso_1","mexico_peso","mexico"),
    "mexico_peso_1_4": ("mexico_peso_1","mexico_peso","mexico"),
    "mexico_peso_1_5": ("mexico_peso_1","mexico_peso","mexico"),
    "mexico_peso_2_1": ("mexico_peso_2","mexico_peso","mexico"),
    "mexico_peso_2_2": ("mexico_peso_2","mexico_peso","mexico"),
    "mexico_peso_fractional_5_2_1": ("mexico_peso_fractional_5_2","mexico_peso","mexico"),
    "mexico_peso_fractional_5_2_2": ("mexico_peso_fractional_5_2","mexico_peso","mexico"),
    "mexico_peso_5_1": ("mexico_peso_5","mexico_peso","mexico"),
    "mexico_peso_5_2": ("mexico_peso_5","mexico_peso","mexico"),
    "mexico_peso_5_3": ("mexico_peso_5","mexico_peso","mexico"),
    "mexico_peso_5_4": ("mexico_peso_5","mexico_peso","mexico"),
    "mexico_peso_5_5": ("mexico_peso_5","mexico_peso","mexico"),
    "mexico_peso_10_1": ("mexico_peso_10","mexico_peso","mexico"),
    "mexico_peso_10_2": ("mexico_peso_10","mexico_peso","mexico"),
    "mexico_peso_10_3": ("mexico_peso_10","mexico_peso","mexico"),
    "mexico_peso_20_1": ("mexico_peso_20","mexico_peso","mexico"),
    "mexico_peso_20_2": ("mexico_peso_20","mexico_peso","mexico"),
    "mexico_peso_50": ("mexico_peso_50","mexico_peso","mexico"),
}

# Indicates which coins are made of silver.
silver_coins = [
    "mexico_real_fractional_1_4",
    "mexico_real_fractional_1_2",
    "mexico_real_1",
    "mexico_real_2",
    "mexico_real_4",
    "mexico_real_8",
    "mexico_centavo_5",
    "mexico_centavo_10_1",
    "mexico_centavo_10_2",
    "mexico_centavo_10_3",
    "mexico_centavo_10_4",
    "mexico_centavo_20_1",
    "mexico_centavo_20_2",
    "mexico_centavo_20_3",
    "mexico_centavo_20_4",
    "mexico_centavo_50_1",
    "mexico_centavo_50_2",
    "mexico_centavo_50_3",
    "mexico_centavo_50_4",
    "mexico_peso_1_1",
    "mexico_peso_1_2",
    "mexico_peso_1_3",
    "mexico_peso_1_4",
    "mexico_peso_2_1",
    "mexico_peso_5_1",
    "mexico_peso_5_2",
    "mexico_peso_5_3",
    "mexico_peso_10_1",
]

# Indicates which coins are made of gold.
gold_coins = [
    "mexico_escudo_fractional_1_2",
    "mexico_escudo_1",
    "mexico_escudo_2",
    "mexico_escudo_4",
    "mexico_escudo_8",
    "mexico_peso_1_5",
    "mexico_peso_2_2",
    "mexico_peso_fractional_5_2_1",
    "mexico_peso_fractional_5_2_2",
    "mexico_peso_5_4",
    "mexico_peso_5_5",
    "mexico_peso_10_2",
    "mexico_peso_10_3",
    "mexico_peso_20_1",
    "mexico_peso_20_2",
    "mexico_peso_50",
]

# Indicates which coins are made of platinum.
platinum_coins = [
]

# Indicates which coins are made of palladium.
palladium_coins = [
]
