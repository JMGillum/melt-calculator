from coinData import CoinData
from tree.node import Node
from metals import Metals
from config import current_year
import weights
from coins.coins import NamedList
coins = {
    # Canada
    "canada_nickel_1": Node(
        CoinData(
            years=list(range(1858,1911)),
            weight=1.1620,
            fineness=0.925,
            metal = Metals.SILVER,
            country="Canada",
            face_value=5,
            denomination="Cents",
        )
    ),
    "canada_nickel_2": Node(
        CoinData(
            years=list(range(1910,1920)),
            weight=1.1664,
            fineness=0.925,
            metal = Metals.SILVER,
            country="Canada",
            face_value=5,
            denomination="Cents",
        )
    ),
    "canada_nickel_3": Node(
        CoinData(
            years=list(range(1920,1968)),
            weight=1.1664,
            fineness=0.80,
            metal = Metals.SILVER,
            country="Canada",
            face_value=5,
            denomination="Cents",
        )
    ),
    "canada_dime_1": Node(
        CoinData(
            years=list(range(1858,1911)),
            weight=2.3240,
            fineness=0.925,
            metal = Metals.SILVER,
            country="Canada",
            face_value=10,
            denomination="Cents",
        )
    ),
    "canada_dime_2": Node(
        CoinData(
            years=list(range(1910,1920)),
            weight=2.3328,
            fineness=0.925,
            metal = Metals.SILVER,
            country="Canada",
            face_value=10,
            denomination="Cents",
        )
    ),
    "canada_dime_3": Node(
        CoinData(
            years=list(range(1920,1968)),
            weight=2.3328,
            fineness=0.8,
            metal = Metals.SILVER,
            country="Canada",
            face_value=10,
            denomination="Cents",
        )
    ),
    "canada_cents_20": Node(
        CoinData(
            years=list(range(1858,1911)),
            weight=4.648,
            fineness=0.925,
            metal = Metals.SILVER,
            country="Canada",
            face_value=20,
            denomination="Cents",
        )
    ),
    "canada_quarter_1": Node(
        CoinData(
            years=list(range(1858,1911)),
            weight=5.81,
            fineness=0.925,
            metal = Metals.SILVER,
            country="Canada",
            face_value=25,
            denomination="Cents",
        )
    ),
    "canada_quarter_2": Node(
        CoinData(
            years=list(range(1910,1920)),
            weight=5.8319,
            fineness=0.925,
            metal = Metals.SILVER,
            country="Canada",
            face_value=25,
            denomination="Cents",
        )
    ),
    "canada_quarter_3": Node(
        CoinData(
            years=list(range(1920,1968)),
            weight=5.8319,
            fineness=0.8,
            metal = Metals.SILVER,
            country="Canada",
            face_value=25,
            denomination="Cents",
        )
    ),
    "canada_half_1": Node(
        CoinData(
            years=list(range(1858,1911)),
            weight=11.62,
            fineness=0.925,
            metal = Metals.SILVER,
            country="Canada",
            face_value=50,
            denomination="Cents",
        )
    ),
    "canada_half_2": Node(
        CoinData(
            years=list(range(1910,1920)),
            weight=11.6638,
            fineness=0.925,
            metal = Metals.SILVER,
            country="Canada",
            face_value=50,
            denomination="Cents",
        )
    ),
    "canada_half_3": Node(
        CoinData(
            years=list(range(1920,1968)),
            weight=11.6638,
            fineness=0.80,
            metal = Metals.SILVER,
            country="Canada",
            face_value=50,
            denomination="Cents",
        )
    ),
    "canada_dollar_1": Node(
        CoinData(
            years=list(range(1920,1968)),
            weight=23.3276,
            fineness=0.8,
            metal = Metals.SILVER,
            country="Canada",
            face_value=1,
            denomination="Dollars",
        )
    ),
    "canada_sovereign_1": Node(
        CoinData(
            years=list(range(1908,1920)),
            weight=7.9881,
            fineness=0.917,
            precious_metal_weight=weights.Weight(0.2354,weights.Units.TROY_OUNCES),
            metal = Metals.GOLD,
            country="Canada",
            face_value=1,
            denomination="Sovereign",
        )
    ),
    "canada_dollar_5_1": Node(
        CoinData(
            years=list(range(1912,1915)),
            weight=8.3591,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Canada",
            face_value=5,
            denomination="Dollars",
        )
    ),
    "canada_dollar_10": Node(
        CoinData(
            years=list(range(1912,1915)),
            weight=16.7181,
            fineness=0.9,
            metal=Metals.GOLD,
            country="Canada",
            face_value=10,
            denomination="Dollars",
        )
    ),
    # Canada - Maple
    "maple_silver_5_dollar": Node(
        CoinData(
            nickname="Silver",
            years=list(range(1988, current_year+1)),
            weight=31.11,
            fineness=0.9999,
            precious_metal_weight=weights.Weight(1, weights.Units.TROY_OUNCES),
            metal=Metals.SILVER,
            country="Canada",
            face_value=5,
            denomination="Dollars",
        )
    ),
    "maple_gold_50_dollar": Node(
        CoinData(
            nickname="Gold",
            years=list(range(1979, current_year+1)),
            weight=31.11,
            fineness=0.9999,
            precious_metal_weight=weights.Weight(1, weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="Canada",
            face_value=50,
            denomination="Dollars",
        )
    ),
    "maple_gold_20_dollar": Node(
        CoinData(
            nickname="Gold",
            years=list(range(1986, current_year+1)),
            weight=15.555,
            fineness=0.9999,
            precious_metal_weight=weights.Weight(0.5, weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="Canada",
            face_value=20,
            denomination="Dollars",
        )
    ),
    "maple_gold_10_dollar": Node(
        CoinData(
            nickname="Gold",
            years=list(range(1982, current_year+1)),
            weight=7.7775,
            fineness=0.9999,
            precious_metal_weight=weights.Weight(0.25, weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="Canada",
            face_value=10,
            denomination="Dollars",
        )
    ),
    "maple_gold_5_dollar": Node(
        CoinData(
            nickname="Gold",
            years=list(range(1982, current_year+1)),
            weight=3.111,
            fineness=0.9999,
            precious_metal_weight=weights.Weight(0.1, weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="Canada",
            face_value=5,
            denomination="Dollars",
        )
    ),
    "maple_gold_1_dollar": Node(
        CoinData(
            nickname="Gold",
            years=list(range(1993, current_year+1)),
            weight=1.5555,
            fineness=0.9999,
            precious_metal_weight=weights.Weight(0.05, weights.Units.TROY_OUNCES),
            metal=Metals.GOLD,
            country="Canada",
            face_value=1,
            denomination="Dollars",
        )
    ),
    "maple_gold_1_2_dollar": Node(
        CoinData(
            nickname="Gold",
            years=list(range(2024, current_year+1)),
            weight=1.00,
            fineness=0.9999,
            precious_metal_weight=weights.Weight(1, weights.Units.GRAMS),
            metal=Metals.GOLD,
            country="Canada",
            face_value=50,
            denomination="Cents",
        )
    ), 
    "maple_platinum_50_dollar": Node(
        CoinData(
            nickname="Platinum",
            years=list(range(2009,current_year+1)),
            weight=31.11,
            fineness=0.9999,
            precious_metal_weight=weights.Weight(1, weights.Units.TROY_OUNCES),
            metal=Metals.PLATINUM,
            country="Canada",
            face_value=50,
            denomination="Dollars",
        )
    ),
    "maple_platinum_50_dollar_old": Node(
        CoinData(
            nickname="Platinum (old purity)",
            years=list(range(1988,2003)),
            weight=31.11,
            fineness=0.9995,
            precious_metal_weight=weights.Weight(1, weights.Units.TROY_OUNCES),
            metal=Metals.PLATINUM,
            country="Canada",
            face_value=50,
            denomination="Dollars",
        )
    ),
    "maple_platinum_20_dollar": Node(
        CoinData(
            nickname="Platinum",
            years=list(range(1988,2003)),
            weight=15.555,
            fineness=0.9995,
            precious_metal_weight=weights.Weight(0.5, weights.Units.TROY_OUNCES),
            metal=Metals.PLATINUM,
            country="Canada",
            face_value=20,
            denomination="Dollars",
        )
    ),
    "maple_platinum_10_dollar": Node(
        CoinData(
            nickname="Platinum",
            years=list(range(1988,2003)),
            weight=7.7775,
            fineness=0.9995,
            precious_metal_weight=weights.Weight(0.25, weights.Units.TROY_OUNCES),
            metal=Metals.PLATINUM,
            country="Canada",
            face_value=10,
            denomination="Dollars",
        )
    ),
    "maple_platinum_5_dollar": Node(
        CoinData(
            nickname="Platinum",
            years=list(range(1988,2003)),
            weight=3.111,
            fineness=0.9995,
            precious_metal_weight=weights.Weight(0.1, weights.Units.TROY_OUNCES),
            metal=Metals.PLATINUM,
            country="Canada",
            face_value=5,
            denomination="Dollars",
        )
    ),
    "maple_platinum_1_dollar": Node(
        CoinData(
            nickname="Platinum",
            years=list(range(1993,2003)),
            weight=1.5555,
            fineness=0.9995,
            precious_metal_weight=weights.Weight(0.05, weights.Units.TROY_OUNCES),
            metal=Metals.PLATINUM,
            country="Canada",
            face_value=1,
            denomination="Dollars",
        )
    ),
    "maple_palladium_50_dollar": Node(
        CoinData(
            nickname="Palladium",
            years=[2005,2006,2009]+list(range(2015,current_year+1)),
            weight=31.11,
            fineness=0.9995,
            precious_metal_weight=weights.Weight(1, weights.Units.TROY_OUNCES),
            metal=Metals.PALLADIUM,
            country="Canada",
            face_value=50,
            denomination="Dollars",
        )
    ),
}

values = {
    # Canada
    "canada_nickel": NamedList("Nickels",["canada_nickel_1","canada_nickel_2","canada_nickel_3"],"5"),
    "canada_dime": NamedList("Dimes",["canada_dime_1","canada_dime_2","canada_dime_3"],"10"),
    "canada_cents_20": NamedList("20",["canada_cents_20"]),
    "canada_quarter": NamedList("Quarters",["canada_quarter_1","canada_quarter_2","canada_quarter_3"],"25"),
    "canada_half": NamedList("Halves",["canada_half_1","canada_half_2","canada_half_3"],"50"),
    "canada_sovereign_1": NamedList("1",["canada_sovereign_1"]),
    "canada_dollar_1": NamedList("1", ["canada_dollar_1"]),
    "canada_dollar_5": NamedList("5", ["canada_dollar_5_1"]),
    "canada_dollar_10": NamedList("10", ["canada_dollar_10"]),
    # Canada - Maple
    "maple_1": NamedList("1 Oz Maple",["maple_silver_5_dollar","maple_gold_50_dollar","maple_platinum_50_dollar_old","maple_platinum_50_dollar","maple_palladium_50_dollar"],"6"),
    "maple_1_2": NamedList("1/2 Oz Maple",["maple_gold_20_dollar","maple_platinum_20_dollar"],"5"),
    "maple_1_4": NamedList("1/4 Oz Maple",["maple_gold_10_dollar","maple_platinum_10_dollar"],"4"),
    "maple_1_10": NamedList("1/10 Oz Maple",["maple_gold_5_dollar","maple_platinum_5_dollar"],"3"),
    "maple_1_20": NamedList("1/20 Oz Maple",["maple_gold_1_dollar","maple_platinum_1_dollar"],"2"),
    "maple_1_gram": NamedList("1 Gram Maple",["maple_gold_1_2_dollar"],"1"),
}

denominations = {
    # Canada
    "canada_cent": NamedList("Cents", ["canada_nickel","canada_dime","canada_cents_20","canada_quarter","canada_half"]),
    "canada_sovereign": NamedList("Sovereigns",["canada_sovereign_1"]),
    "canada_dollar": NamedList("Dollars", ["canada_dollar_1","canada_dollar_5","canada_dollar_10"]),
    "maple": NamedList("Maple",["maple_1","maple_1_2","maple_1_4","maple_1_10","maple_1_20","maple_1_gram"]),
}

coins_reverse_build = {
    "canada_nickel_1": ("canada_nickel","canada_cent","canada"),
    "canada_nickel_2": ("canada_nickel","canada_cent","canada"),
    "canada_nickel_3": ("canada_nickel","canada_cent","canada"),
    "canada_dime_1": ("canada_dime","canada_cent","canada"),
    "canada_dime_2": ("canada_dime","canada_cent","canada"),
    "canada_dime_3": ("canada_dime","canada_cent","canada"),
    "canada_cents_20": ("canada_cents_20","canada_cent","canada"),
    "canada_quarter_1": ("canada_quarter","canada_cent","canada"),
    "canada_quarter_2": ("canada_quarter","canada_cent","canada"),
    "canada_quarter_3": ("canada_quarter","canada_cent","canada"),
    "canada_half_1": ("canada_half","canada_cent","canada"),
    "canada_half_2": ("canada_half","canada_cent","canada"),
    "canada_half_3": ("canada_half","canada_cent","canada"),
    "canada_sovereign_1": ("canada_sovereign_1","canada_sovereign","canada"),
    "canada_dollar_1": ("canada_dollar_1","canada_dollar","canada"),
    "canada_dollar_5_1": ("canada_dollar_5","canada_dollar","canada"),
    "canada_dollar_10": ("canada_dollar_10","canada_dollar","canada"),
    "maple_silver_5_dollar": ("maple_1","maple","canada"),
    "maple_gold_50_dollar": ("maple_1","maple","canada"),
    "maple_platinum_50_dollar_old": ("maple_1","maple","canada"),
    "maple_platinum_50_dollar": ("maple_1","maple","canada"),
    "maple_palladium_50_dollar": ("maple_1","maple","canada"),
    "maple_gold_20_dollar": ("maple_1_2","maple","canada"),
    "maple_platinum_20_dollar": ("maple_1_2","maple","canada"),
    "maple_gold_10_dollar": ("maple_1_4","maple","canada"),
    "maple_platinum_10_dollar": ("maple_1_4","maple","canada"),
    "maple_gold_5_dollar": ("maple_1_10","maple","canada"),
    "maple_platinum_5_dollar": ("maple_1_10","maple","canada"),
    "maple_gold_1_dollar": ("maple_1_20","maple","canada"),
    "maple_platinum_1_dollar": ("maple_1_20","maple","canada"),
    "maple_gold_1_2_dollar": ("maple_1_gram","maple","canada"),
}

silver_coins = [
    "canada_nickel_1",
    "canada_nickel_2",
    "canada_nickel_3",
    "canada_dime_1",
    "canada_dime_2",
    "canada_dime_3",
    "canada_cents_20",
    "canada_quarter_1",
    "canada_quarter_2",
    "canada_quarter_3",
    "canada_half_1",
    "canada_half_2",
    "canada_half_3",
    "canada_dollar_1",
    "maple_silver_5_dollar",
]

gold_coins = [
    "canada_sovereign_1",
    "canada_dollar_5_1",
    "canada_dollar_10",
    "maple_gold_50_dollar",
    "maple_gold_20_dollar",
    "maple_gold_10_dollar",
    "maple_gold_5_dollar",
    "maple_gold_1_dollar",
    "maple_gold_1_2_dollar",
]

platinum_coins = [
    "maple_platinum_50_dollar_old",
    "maple_platinum_50_dollar",
    "maple_platinum_20_dollar",
    "maple_platinum_10_dollar",
    "maple_platinum_5_dollar",
    "maple_platinum_1_dollar",
]

# Indicates which coins are made of palladium.
palladium_coins = [
    "maple_palladium_50_dollar",
]
