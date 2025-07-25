"""
   Author: Josh Gillum              .
   Date: 25 July 2025              ":"         __ __
   Code: Line 87                  __|___       \ V /
                                .'      '.      | |
                                |  O       \____/  |
^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

    This file is a template for one that stores information about the coins of
    a country. It contains all of the necessary imports (some may be unused by
    this country), as well as the necessary variables.

    The coins, values, denominations, and coins_reverse_build variables must be
    updated. silver_coins, gold_coins, platinum_coins, and palladium_coins must
    be updated as necessary.

    The text in this header comment should be replaced with a simple tree
    diagram showing the contents of the data stored inside. If this was Canada
    for example:

     Canada
     |->Cent
     |  |->Nickel
     |  |  |->canada_nickel_1
     |  |  |->canada_nickel_2
     |  |  |->canada_nickel_3
     |  |->Dime
     |  |  |->canada_dime_1
     |  |  |->canada_dime_2
     |  |  |->canada_dime_3
     |  |->20
     |  |  |->canada_cents_20
     |  |->Quarter
     |  |  |->canada_quarter_1
     |  |  |->canada_quarter_2
     |  |  |->canada_quarter_3
     |  |->Half
     |      |->canada_half_1
     |      |->canada_half_2
     |      |->canada_half_3
     |->Dollar
     |  |->1
     |  |  |->canada_dollar_1
     |  |->5
     |  |  |->canada_dollar_5_1
     |  |->10
     |      |->canada_dollar_10
     |->Maple
     |  |->1 Gram Maple
     |  |  |->maple_gold_1_2_dollar
     |  |->1/20 Oz Maple
     |  |  |->maple_gold_1_dollar
     |  |  |->maple_platinum_1_dollar
     |  |->1/10 Oz Maple
     |  |  |->maple_gold_5_dollar
     |  |  |->maple_platinum_5_dollar
     |  |->1/4 Oz Maple
     |  |  |->maple_gold_10_dollar
     |  |  |->maple_platinum_10_dollar
     |  |->1/2 Oz Maple
     |  |  |->maple_gold_20_dollar
     |  |  |->maple_platinum_20_dollar
     |  |->1 Oz Maple
     |      |->maple_gold_50_dollar
     |      |->maple_silver_5_dollar
     |      |->maple_platinum_50_dollar_old
     |      |->maple_palladium_50_dollar
     |      |->maple_platinum_50_dollar
     |->Sovereign
         |->1
             |->canada_sovereign_1

    This can easily be done after all of the data is defined by setting 
    tree_fancy_characters to False (in config.py), then running main.py with 
    the either (-n or --no_coins) or (-i or --only_coin_ids) flag (depends on 
    desired level of output), as well as -c <country_name> (this will limit the 
    results to only this country.)

    Coins that are still in production should use the current_year variable,
    so that their years can be updated by updating current_year in config. Once
    a coin goes out of production, the upper cap of its lifespan can be 
    hardcoded in.

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
}

# Stores NamedLists of keys from coins
values = {
}

# Stores NamedLists of keys from values
denominations = {
}

# Stores every key inside of coins, with values of 
# tuples of (<value_id>,<denomination_id>,<country_id>)
coins_reverse_build = {
}

# Indicates which coins are made of silver.
silver_coins = [
]

# Indicates which coins are made of gold.
gold_coins = [
]

# Indicates which coins are made of platinum.
platinum_coins = [
]

# Indicates which coins are made of palladium.
palladium_coins = [
]
