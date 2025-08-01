"""
   Author: Josh Gillum              .
   Date: 24 July 2025              ":"         __ __
                                  __|___       \ V /
                                .'      '.      | |
                                |  O       \____/  |
^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

    This script is designed to be used to make adding or updating CoinData
    objects within the Coins class. See CoinInfo.py for information on the
    class. The script will print out the entire coins_reverse_build dictionary,
    as well as the silver_coins and gold_coins lists. They will simply have to
    be copied and pasted into Coins class in coins/coins.py. Make sure to delete
    the old versions of these variables as well.

    In order to work, the CoinData objects must contain the metal type (either
    Metals.SILVER or Metals.GOLD). The entries within Coins.values,
    Coins.denominations, and Coins.countries must also be correct. There needs
    to be a way for the script to go from a country all the way down to the coin
    object.

^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
"""

from metals import Metals
from tree.node import Node
from coins.coins import Coins
from alternativeNames import AlternativeNames


import coins.canada as canada
import coins.france as france
import coins.germany as germany
import coins.great_britain as great_britain
import coins.italy as italy
import coins.mexico as mexico
import coins.russia as russia
import coins.south_africa as south_africa
import coins.switzerland as switzerland
import coins.united_states as united_states

tab = "    "

def convertCountry(name):
    names = {
            "canada":"can",
            "france":"fra",
            "germany":"deu",
            "great_britain":"gbr",
            "italy":"ita",
            "mexico":"mex",
            "russia":"rus",
            "south_africa":"zaf",
            "switzerland":"che",
            "united_states":"usa",
            }
    try:
        return names[name]
    except KeyError:
        return "UNKNOWN"

def metalToString(metal):
    if metal == Metals.SILVER:
        return "ag"
    elif metal == Metals.GOLD:
        return "au"
    elif metal == Metals.PALLADIUM:
        return "pd"
    elif metal == Metals.PLATINUM:
        return "pt"
    else:
        return "other"



if __name__ == "__main__": 
    country = south_africa
    iso_name = "zaf"

    insert_values = []
    insert_coins = []
    for denomination in country.denominations:
        item = country.denominations[denomination]
        for value in item:
            alternative_names = ""
            name = ""
            value_item = country.values[value]
            placeholder = ""
            if isinstance(value_item.name,AlternativeNames):
                placeholder += ",name"
                for i in range(min(len(value_item.name.other_names),6)):
                    if i == 0:
                        name = f',"{value_item.name.other_names[i].lower()}"'
                    else:
                        placeholder += f",alternative_name_{i}"
                        alternative_names += f",\"{value_item.name.other_names[i].lower()}\""

            denomination_id = f"{iso_name}_{item.name.lower()}"
            value_id = f"{denomination_id}_{value_item}"
            d_temp = ""
            
            d_temp += f"INSERT INTO face_values(value_id,denomination_id,value{placeholder}) VALUES("
            d_temp += f'"{value_id}","{iso_name}_{item.name.lower()}"'
            d_temp += f',{value_item.name.lower()}'
            if isinstance(value_item.name,AlternativeNames):
                d_temp += f'{name}{alternative_names}'
            d_temp += ");"
            insert_values.append(d_temp)
            i = 0
            for coin in value_item:
                i += 1
                coin_item = country.coins[coin]
             
                if isinstance(coin_item,Node):
                    coin_item = coin_item.data

                pmw = str(coin_item.precious_metal_weight.as_troy_ounces()) if coin_item.precious_metal_weight else "NULL"

                c_temp = ""
                if coin_item.nickname:
                    c_temp += "INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal,name) VALUES("
                else:
                    c_temp += "INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("
                c_temp += f"\"{value_id}_{i}\",\"{value_id}\","
                c_temp += f"{coin_item.weight.as_grams()},{coin_item.fineness},{pmw},"
                c_temp += f'"{str(coin_item.years)[1:-1]}","'
                c_temp +=f"{metalToString(coin_item.metal)}\""
                if coin_item.nickname:
                    c_temp += f',"{coin_item.nickname.lower()}"'
                c_temp += ");"
                insert_coins.append(c_temp)

    print("---------------------Values--------------------------")
    for line in insert_values:
        print(line)
    print("---------------------Coins--------------------------")
    for line in insert_coins:
        print(line)
