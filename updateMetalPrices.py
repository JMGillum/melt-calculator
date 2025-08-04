from db_interface import DB_Interface
import config
from datetime import datetime

def updateMetalPrices(db:DB_Interface,*prices):
    results = []
    for price in prices:
        results.append(db.updateMetalPrice(price))
    return results


if __name__ == "__main__":
    try:
        db = DB_Interface()
        db.connect(config.db_config)
        metals = db.fetchMetals()
        metals = [x for x in metals if not x[0] == "other"]
        updates = []
        for metal in metals:
            while True:
                metal_id,name,price,price_date = metal
                price = input(f"Enter Price for [{metal_id}]({name}) (currently:{config.currency_symbol}{price}) (enter empty string to skip): ")
                if price:
                    current_date = datetime.today().strftime('%Y-%m-%d')
                    price_date = current_date
                    response = input(f"Enter date (YYYY-MM-DD) for price or enter empty string to use {current_date}: ") 
                    if response:
                        price_date = response
                    if input(f"Press enter to update [{metal_id}]({name}) to {config.currency_symbol}{price} as of {price_date} (enter any other key to modify): "):
                        continue
                    else:
                        updates.append((metal_id,price,price_date))
                break
        if updates:
            confirmation = input("Push updates to database? (y/n): ").lower()
            if confirmation == 'y' or confirmation == "yes":
                print("Updates: ")
                results = updateMetalPrices(db,*updates)
                for i in range(len(updates)):
                    item = updates[i]
                    result = results[i]
                    print(f"{item} was updated {'successfully' if result else 'unsuccessfully'}")
            else:
                print("Aborting...")
            
        else:
            print("No updates")

    finally:
        db.closeConnection()
