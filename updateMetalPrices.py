#   Author: Josh Gillum              .
#   Date: 19 January 2026           ":"         __ __
#                                  __|___       \ V /
#                                .'      '.      | |
#                                |  O       \____/  |
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
#
#    This script provides a function that prompts the user to enter the current
#    prices for the metals defined in the database. 
#
#    This script is still rough and further refinement is necessary. The prompts
#    and output needs to be improved, as well as the directions.
#
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

import config

from db_interface import DB_Interface
from datetime import datetime

def updateMetalPrices(db:DB_Interface,*prices):
    """Pushes a metal price to the database"""
    results = [] # Stores the status messages returned by the database
    for price in prices:
        results.append((price,db.updateMetalPrice(price)))
    return results

def getMetalPricesFromUser(db,metals):
    """Prompts the user to input metal prices and the dates they were valid on."""
    # Fetches the defined metals and preps it.
    print(metals)
    updates = []

    # Loops through each metal
    for metal_id,metal in metals.items():
        while True:
            name,price,price_date = metal

            # Gets price from user
            price = input(f"Enter Price for [{metal_id}]({name}) (currently:{config.currency_symbol}{price}) (enter empty string to skip): ")
            if price: # The user entered a valid price
                
                # Gets the date from the user, or defaults to current date
                current_date = datetime.today().strftime('%Y-%m-%d')
                price_date = current_date
                response = input(f"Enter date (YYYY-MM-DD) for price or enter empty string to use {current_date}: ") 
                if response: # User entered a date and did not use default
                    price_date = response

                # Gets confirmation that the information is correct
                if input(f"Press enter to update [{metal_id}]({name}) to {config.currency_symbol}{price} as of {price_date} (enter any other key to modify): "):
                    # User wants to re-enter information for this metal
                    continue
                else:
                    # Adds the metal to updates where it will be checked later
                    updates.append((metal_id,price,price_date))

            # Either the metal was skipped or updated. The updates list will indicate whether
            # the metal was updated
            break

    # Some metals were updated
    if updates:
        # Gets confirmation that the user wants to update the database
        confirmation = input("Push updates to database? (y/n): ").lower()
        if confirmation == 'y' or confirmation == "yes":
            print("Updates: ")
            results = updateMetalPrices(db,*updates) # Pushes to database
            for item,result in results: # Status as to whether the metal was updated successfully.
                print(f"{item} was updated {'successfully' if result else 'unsuccessfully'}")
        else: # User did not want to push to database
            print("Aborting...")
        
    else: # Nothing in updates list, so all metals were skipped.
        print("No updates")

if __name__ == "__main__":
    print("This script is not meant to be called on its own. Please use the main script.")
