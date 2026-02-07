#   Author: Josh Gillum              .
#   Date: 19 January 2026           ":"         __ __
#                                  __|___       \ V /
#                                .'      '.      | |
#                                |  O       \____/  |
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
#
#    This script provides a function for managing the purchases stored within 
#    the database. It is still WIP and currently can add or remove purchases.
#
#    Future goal is to be able to modify existing purchases to change quantities
#    or prices (to fix an error or to "sell off" part of the purchase)
#
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

import config
from coins import Coins
from coinData import CoinData, Purchase
import data

from general import getConfirmation, getDate, selectEntry
from treasure.text import CenterText


def getPurchaseInformation():
    """Gets purchase date,quantity, and price from user"""
    print(CenterText("Purchase",filler_character='-',width=80))

    # Gets the date from the user, in the form yyyy-mm-dd
    date_string = getDate()

    # Stores a purchase
    purchase = {
            "date": date_string,
            "quantity": None,
            "unit_price": None
            }
    while True: # Gets the quantity of the issue purchased.
        quantity = input("Enter number of coins purchased: ")
        if quantity:
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    print("Quantity must be greater than 0")
                    continue
            except ValueError:
                print("Quantity must be an integer value")
            purchase["quantity"] = quantity
            break
    price_by_unit = True # True if price is per coin, False for price by lot.
    if purchase["quantity"] > 1:
        # If multiple coins purchased, checks if user wants to enter price per coin or for the entire lot
        if not getConfirmation("Enter price per coin? (No will have you enter price of entire purchase then calculate price per coin)"):
            price_by_unit = False
    while True: # Gets price from the user
        try:
            if price_by_unit:
                price = input("Enter price (per coin if multiple purchased): ")
                float(price)
            else:
                price = input("Enter price of total purchase: ")
                price = round(float(price)/quantity,2)
        except ValueError:
            print("Price must be numeric.")
            continue
        purchase["unit_price"] = price
        break
    print(f"({date_string}) {config.currency_symbol}{purchase['unit_price']} x {purchase['quantity']}")
    return purchase


def getSpecificCoinInformation():
    """Gets information for a specific coin entry from the user (mint year and mint mark)"""
    print(CenterText("Specific Coin",filler_character='-',width=80))
    specific_coin = {"year":None,"mintmark":None}
    if getConfirmation("Enter specific coin details (year and/or mintmark)?"):
        while True:
            while True:
                year = input("Enter year or enter empty string to skip: ")
                if not year:
                    break
                else:
                    try:
                        year = int(year)
                        if year <= 1000:
                            print("Year must be greater than 1000.")
                            continue
                        specific_coin["year"] = year
                        break
                    except ValueError:
                        print("Year must be numeric")
                        continue
            mintmark = input("Enter mintmark or empty string to skip: ")
            if mintmark:
                specific_coin["mintmark"] = mintmark
            if getConfirmation(f"Is the year ({specific_coin['year']}) and mintmark ({specific_coin['mintmark']}) correct?"):
                break
            specific_coin["year"] = specific_coin["mintmark"] = None
    return specific_coin


def pushSpecificCoin(db,specific_coin,coin):
    specific_coin_id = None
    
    # Pushes the specific coin to the specific_coins table
    if specific_coin["year"] or specific_coin["mintmark"]:
        entries = db.fetchSpecificCoin(coin[0],year=specific_coin["year"],mintmark=specific_coin["mintmark"])
        if entries:
            specific_coin_id = entries[0][0]
        else:
            results = db.addSpecificCoin(coin[0],specific_coin["year"],specific_coin["mintmark"])
            if not results:
                exit(1)
            entries = db.fetchSpecificCoin(coin[0],year=specific_coin["year"],mintmark=specific_coin["mintmark"])
            if not entries:
                exit(1)
            print("Added specific coin successfully")
            specific_coin_id = entries[0][0]
    else: # User did not specify a specific coin
        specific_coin_id = None
    return specific_coin_id

def pushPurchase(db,coin,purchase,specific_coin_id):
    # Some error occured while trying to push to purchases table
    if not db.addPurchase({"coin_id":coin[0],"purchase_date":purchase["date"],"unit_price":purchase["unit_price"],"quantity":purchase["quantity"],"specific_coin_id":specific_coin_id}):
        print("FAILED to add purchase")
        exit(1)
    else: # Successful
        print("Added purchase successfully.")


def getCoinInformation(db,additional_search_args:dict=None):
    print(CenterText("Find Coin",filler_character='-',width=80))
    # Prompts user for information to search for a coin
    while True:
        coin_find_by_id = True
        if getConfirmation("Use search string instead of coin id?"):
            coin_find_by_id = False
        if coin_find_by_id:
            coin_id = input("Coin id: ")
            entries = db.fetchCoinById(coin_id)
        else:
            search_string = input("Search string: ")
            arguments = Coins.parseSearchString(db, search_string)
            search_args = {"country":arguments[0],"denomination":arguments[1],"year":arguments[2],"face_value":arguments[3]}
            if additional_search_args:
                search_args |= additional_search_args
            entries = db.fetchCoins(search_args)
        if entries:
            break
        else:
            print("No results found. Try again...")

    entry_id = 0
    if len(entries) > 1:
        print("Multiple results found...")
    for i in range(len(entries)):
        entry = entries[i]
        temp_coin = CoinData(weight=entry[1],fineness=entry[2],precious_metal_weight=entry[3],years=entry[4],metal=entry[5],nickname=entry[6],face_value=entry[8],denomination=entry[11],country=entry[13])
        temp_coin.togglePrice(False)
        temp_output = temp_coin.print("%c %F %d " + temp_coin.getCoinString())
        entries[i] = (entry[0],temp_output) # Tuple of (coin_id, coin string)
    entry_id = selectEntry([x[1] for x in entries]) # Gets entry from list of coin strings

    coin = entries[entry_id]
    print(f"Selected: {coin[1]}")
    return coin


def setMetals(db):
    prices = {}
    entries = db.fetchMetals()
    for entry in entries:
        key,name,price,date = entry 
        if not key == "other":
            prices[key] = (name,float(price),date)
    data.metals = prices

def selectPurchase(db,coin):
    purchases = db.fetchPurchasesByCoinId(coin[0],True,True)
    if not purchases:
        print("No purchases found.")
        exit(1)
    # Creates a list of tuples of (purchase_id,specific_coin_id,Purchase object). 
    # They are then sorted by purchase date
    purchases = sorted([(x[7],x[8],Purchase(*(x[1:4]+x[5:7]))) for x in purchases],key=lambda x: x[2].purchase_date)
    purchase_id = selectEntry([x[2] for x in purchases])
    purchase = purchases[purchase_id]
    print(f"Selected: {purchase[2]}")
    if purchase[0] is None:
        print("Error with purchase")
        exit(1)
    return purchase

def printResult(result,item,exit_on_fail=True):
    if result:
        print(f"Successfully deleted {item}")
    else:
        print(f"Failed to delete {item}")
        if exit_on_fail:
            exit(1)


def alterDatabaseConfirmation():
    print(CenterText("Warning",filler_character='-',width=80))
    return getConfirmation("Continuing will alter the database. Continue?") # Ensures user wants to continue

def start(args,db):
    while True:
        if args["delete"]: # Delete mode
            coin = getCoinInformation(db,{"show_only_owned":True})
            purchase = selectPurchase(db,coin)
            if alterDatabaseConfirmation():
                result = db.deleteById({"purchases":purchase[0]})
                printResult(result,purchase[2])
                # Check if specific_coin is used by other purchases
                if purchase[1] is not None and not db.fetchPurchasesWithSpecificCoinId(purchase[1]):
                    # It is not used, see if user wants to delete it
                    if getConfirmation("No remaining coins use the specific_coin information of the deleted coin. Delete entry from specific_coins table?"):
                        result = db.deleteById({"specific_coins":purchase[1]})
                        printResult(result,purchase[1])
                    else:
                        print("Keeping specific coin information")
            else: # User didn't want to alter database
                print("Aborting...")
                exit(0)
        else: # Default add mode
            coin = getCoinInformation(db)
            purchase = getPurchaseInformation()
            specific_coin = getSpecificCoinInformation()
            if alterDatabaseConfirmation():
                specific_coin_id = pushSpecificCoin(db,specific_coin,coin)
                pushPurchase(db,coin,purchase,specific_coin_id)
            else:
                print("Aborting...")
                exit(0)
        if not getConfirmation(f"{'Delete' if args['delete'] else 'Add'} another purchase?"):
            break

if __name__ == "__main__":
    print("This script is not meant to be called on its own. Please use the main script.")
