from db_interface import DB_Interface
import config
from datetime import datetime
from coins import Coins
from coinData import CoinData
import data


def getDate():
    date_prompt = "Enter date as either: 'D.M.Y', 'M/D/Y', or 'Y-M-D': "
    tries = 0
    found_date = None
    response = input(date_prompt)
    while tries == 0 or response:
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
                month = int(month)
                day = int(day)
            except ValueError:
                print("Day, month, and year values must be whole numbers")
                response = None
            # Ensures date is within the range that can be sent to the database
            if response:
                if year < 100:
                    year += 2000
                if year < 1000 or year > 9999:
                    print("Acceptable dates are between: '1000-01-01' and '9999-12-31'.")
                    response = None
                if day <= 0 or day > 31:
                    print("Day must be between 1 and 31")
                    response = None
                if month <= 0 or month > 12:
                    print("Month must be betwen 1 and 12")
                    response = None
            if response:
                found_date = datetime(year,month,day)
                response = input(f'Press enter to accept {found_date.strftime("%d %B %Y")} or {date_prompt}')
            else:
                response = input(date_prompt)
    return found_date.strftime("%Y-%m-%d")

def setMetals(db):
    prices = {}
    entries = db.fetchMetals()
    for entry in entries:
        key,name,price,date = entry 
        if not key == "other":
            prices[key] = (name,float(price),date)
    data.metals = prices

if __name__ == "__main__":
    try:
        db = DB_Interface()
        db.connect(config.db_config)
        setMetals(db) # Sets value of data.metals for translation when making CoinData objects
        entries = None
        # Prompts user for information to search for a coin
        while True:
            coin_find_by_id = True
            response = input("Find coin by search string instead of id? (y/n): ").lower()
            if response == 'y' or response == "yes":
                coin_find_by_id = False
            if coin_find_by_id:
                coin_id = input("Coin id: ")
                entries = db.fetchCoinById(coin_id)
            else:
                search_string = input("Search string: ")
                arguments = Coins.parseSearchString(search_string, db.fetchCountryNames())
                entries = db.fetchCoins({"country":arguments[0],"denomination":arguments[1],"year":arguments[2],"face_value":arguments[3]})
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
            entries[i] = (entry[0],temp_output)
            if len(entries) > 1:
                print(f"{i+1}: {entries[i][1]}")
        if len(entries) > 1: # Multiple results from search
            while True:
                try:
                    entry_id = int(input("Enter number for entry to select it: "))
                except ValueError:
                    print("Must be numeric.")
                else:
                    if entry <= 0 or entry > len(entries[i]):
                        print("Value out of range")
                        continue
                entry_id -= 1
                break
        else: # Only one result from search
            entry_index = 0

        coin = entries[entry_index]
        print(f"Selected: {coin[1]}")
            
        # Gets purchase date,quantity, and price from user
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
            response = input("Enter price per coin? (No will have you enter price of entire purchase then calculate price per coin) (y/n):").lower()
            if not (response == 'y' or response == 'yes'):
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

        # Gets specific coin information from user
        specific_coin = {"year":None,"mintmark":None}
        response = input("Enter specific coin details (year and/or mintmark)? (y/n): ").lower()
        if response == 'y' or response == 'yes':
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
                confirm = input(f"Is the year ({specific_coin['year']}) and mintmark ({specific_coin['mintmark']}) correct? (y/n):").lower()
                if confirm =='y' or confirm == "yes":
                    break
                specific_coin["year"] = specific_coin["mintmark"] = None
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

        # Some error occured while trying to push to purchases table
        if not db.addPurchase({"coin_id":coin[0],"purchase_date":purchase["date"],"unit_price":purchase["unit_price"],"quantity":purchase["quantity"],"specific_coin_id":specific_coin_id}):
            print("FAILED to add purchase")
            exit(1)
        else: # Successful
            print("Added purchase successfully.")
    finally:
        db.closeConnection()
