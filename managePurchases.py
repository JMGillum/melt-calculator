from db_interface import DB_Interface
import config
from datetime import datetime
from coins import Coins
from coinData import CoinData,Purchase
import data
import argparse

def getConfirmation(prompt):
    while True:
        response = input(f"{prompt} (y/n): ").lower()
        if response == 'y' or response == "yes":
            return True
        elif response == 'n' or response == "no":
            return False
        else:
            print("You must enter either 'y' or 'n'.")

def getDate():
    date_prompt = "Enter date as either: 'D.M.Y', 'M/D/Y', or 'Y-M-D': "
    tries = 0
    found_date = None
    response = None
    while tries == 0 or response or response is None:
        if tries == 0 or response is None:
            response = input(date_prompt)
        else:
            response = input(f'Press enter to accept {found_date.strftime("%d %B %Y")} or {date_prompt}')
        if tries <= 0 or response:
            tries += 1
            if response:
                values_dot = response.split(".")
                values_slash = response.split("/")
                values_dash = response.split("-")
                day = -1
                month = -1
                year = -1

                if len(values_dot) == 3:
                    day,month,year = values_dot
                elif len(values_slash) == 3:
                    month,day,year = values_slash
                elif len(values_dash) == 3:
                    year,month,day = values_dash

                try:
                    year = int(year)
                    if year < 100:
                        year += 2000
                    found_date = datetime(year,int(month),int(day))
                except TypeError:
                    print("All values must be numeric.")
                    response = None
                except ValueError as e:
                    print(f"Values are outside of the acceptable range. {e}")
                    response = None
                # Ensures date is within the range that can be sent to the database
    return found_date.strftime("%Y-%m-%d")

def getPurchaseInformation():
    # Gets purchase date,quantity, and price from user
    print("---------------------------------Purchase----------------------------------------")
    date_string = getDate()
    purchase = {
            "date": date_string,
            "quantity": None,
            "unit_price": None
            }
    while True:
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
    price_by_unit = True
    if purchase["quantity"] > 1:
        if not getConfirmation("Enter price per coin? (No will have you enter price of entire purchase then calculate price per coin)"):
            price_by_unit = False
    while True:
        try:
            if price_by_unit:
                price = input("Enter price (per coin if multiple purchased): ")
                temp = float(price)
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
    # Gets specific coin information from user
    print("-------------------------------Specific Coin-------------------------------------")
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


def selectEntry(entries):
    for i in range(len(entries)):
        if len(entries) > 1:
            print(f"{i+1}: {entries[i]}")
        else:
            print(f"{entries[i]}")
    entry_id = 0
    if len(entries) > 1: # Multiple results from search
        while True:
            try:
                entry_id = int(input("Enter number for entry to select it: "))
            except ValueError:
                print("Must be numeric.")
                continue
            if entry_id <= 0 or entry_id > len(entries):
                print("Value out of range")
                continue
            else:
                entry_id -= 1
                break
    return entry_id


def getCoinInformation(db,additional_search_args:dict=None):
    print("--------------------------------Find Coin----------------------------------------")
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
    print("------------------------------------Warning-------------------------------------")
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
