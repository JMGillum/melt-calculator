#   Author: Josh Gillum              .
#   Date: 23 February 2026          ":"         __ __
#                                  __|___       \ V /
#                                .'      '.      | |
#                                |  O       \____/  |
# ~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
#
#    This script provides a function for managing the purchases stored within
#    the database. It is still WIP and currently can add or remove purchases.
#
#    Future goal is to be able to modify existing purchases to change quantities
#    or prices (to fix an error or to "sell off" part of the purchase)
#
# ~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

from coins import Coins
from coinData import CoinData, Purchase
import data

from treasure.text import CenterText
from treasure.prompt import GetConfirmation, GetDate, SelectEntry


def GetPurchaseInformation(config:dict)->dict:
    """ Gets purchase date, quantity, and price from user

    Args:
        config: Needs to have "currency_symbol" defined.

    Returns: Dictionary storing "date", "quantity", and "unit_price"
        
    """

    # Prints header
    print(CenterText("Purchase", filler_character="-", width=80))

    # Gets the date from the user, in the form yyyy-mm-dd
    date_string = GetDate()

    # Stores a purchase
    purchase = {"date": date_string, "quantity": None, "unit_price": None}
    while True:  # Gets the quantity of the issue purchased.
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

    # True if price is per coin, False for price by lot.
    price_by_unit = True  
    if purchase["quantity"] > 1:

        # If multiple coins purchased, checks if user wants to enter price per coin or for the entire lot
        if not GetConfirmation(
            "Enter price per coin? (No will have you enter price of entire purchase then calculate price per coin)"
        ):
            price_by_unit = False

    # Get price from user
    while True:
        try:
            if price_by_unit:
                price = input("Enter price (per coin if multiple purchased): ")
                float(price)
            else:
                price = input("Enter price of total purchase: ")
                price = round(float(price) / quantity, 2)

        # Input could nut be converted to float
        except ValueError:
            print("Price must be numeric.")
            continue
        purchase["unit_price"] = price
        break

    print(
        f"({date_string}) {config['currency_symbol']}{purchase['unit_price']} x {purchase['quantity']}"
    )
    return purchase


def GetSpecificCoinInformation()->dict:
    """ Gets information for a specific coin entry from the user (mint year and mint mark)

    Returns: dict with "year" and "mintmark" defined
        
    """

    # Prints header
    print(CenterText("Specific Coin", filler_character="-", width=80))
    specific_coin = {"year": None, "mintmark": None}

    # Determines if user wants to enter specific coin information
    if GetConfirmation("Enter specific coin details (year and/or mintmark)?"):
        while True:

            # Gets year from user
            while True:
                year = input("Enter year or enter empty string to skip: ")
                if not year:
                    break
                else:

                    # Validates input for year
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
            if GetConfirmation(
                f"Is the year ({specific_coin['year']}) and mintmark ({specific_coin['mintmark']}) correct?"
            ):
                break
            specific_coin["year"] = specific_coin["mintmark"] = None
    return specific_coin


def PushSpecificCoin(db, specific_coin:dict, coin_id:str)->str:
    """ Fetches the specific coin id that matches what is defined in specific_coin. Adds a new entry to the database if needed.

    Args:
        db (DB_Interface): object for interacting with the database
        specific_coin: Must have "year" and "mintmark" defined
        coin: coin_id that specific_coin belongs to

    Returns: The specific_coin_id of the database entry.
        
    """
    specific_coin_id = None

    # Checks to see if the specific coin information is already stored in a database entry
    if specific_coin["year"] or specific_coin["mintmark"]:
        entries = db.FetchSpecificCoin(
            coin_id, year=specific_coin["year"], mintmark=specific_coin["mintmark"]
        )

        # Information is stores, so extract the specific_coin_id
        if entries:
            specific_coin_id = entries[0][0]

        # No results in dataabse
        else:

            # Push new entry to database
            results = db.AddSpecificCoin(
                coin_id, specific_coin["year"], specific_coin["mintmark"]
            )
            if not results:
                exit(1)

            # Fetch entry that was just added to confirm that it was added successfully.
            entries = db.FetchSpecificCoin(
                coin_id, year=specific_coin["year"], mintmark=specific_coin["mintmark"]
            )
            if not entries:
                exit(1)
            print("Added specific coin successfully")

            # Extract specific_coin_id from results
            specific_coin_id = entries[0][0]

    # specific_coin argument did not have the defined variables
    else:
        specific_coin_id = None

    return specific_coin_id


def PushPurchase(db, coin_id:str, purchase:dict, specific_coin_id:str|None):
    """ Adds a new purchase to the database

    Args:
        db (DB_Interface): object for interacting with the database 
        coin_id: Coin id of the coin that the specific_coin belongs to
        purchase: Must have "date", "unit_price", and "quantity" defined.
        specific_coin_id: Id for specific coin for this purchase, or None
    """
    # Some error occured while trying to push to purchases table
    if not db.AddPurchase(
        {
            "coin_id": coin_id,
            "purchase_date": purchase["date"],
            "unit_price": purchase["unit_price"],
            "quantity": purchase["quantity"],
            "specific_coin_id": specific_coin_id,
        }
    ):
        print("FAILED to add purchase")
        exit(1)

    # Successful
    else:
        print("Added purchase successfully.")


def GetCoinInformation(db, additional_search_args: dict = None, purchases:dict={}, config:dict={})->tuple:
    """ Gets information about the coin that the user wants to manage purchases for.

    Args:
        db (DB_Interface): object for interacting with the database 
        additional_search_args: Any additional arguments for filtering results. Passed to db.FetchCoins() along with
        the four defined in this function: "country", "denomination", "year", "face_value"
        config: Stores config options. Used to set the characters used to print the output tree

    Returns: Tuple of (coin_id, CoinData object)
        
    """

    # Prints header
    print(CenterText("Find Coin", filler_character="-", width=80))

    # Prompts user for information to search for a coin
    while True:
        coin_find_by_id = True

        # Determines which search method the user wants to use
        if GetConfirmation("Use search string instead of coin id?"):
            coin_find_by_id = False

        # Search by id
        if coin_find_by_id:
            coin_id = input("Coin id: ")
            entries,mapping = db.FetchCoins({"coin_id":coin_id})

        # Search by keywords
        else:
            search_string = input("Search string: ")
            arguments = Coins.ParseSearchString(db, search_string,config=config)
            search_args = {
                "country": arguments[0],
                "denomination": arguments[1],
                "year": arguments[2],
                "face_value": arguments[3],
            }
            if additional_search_args:
                search_args |= additional_search_args
            entries, mapping = db.FetchCoins(search_args)
        if entries:
            x = Coins.Build(entries,mapping,config=config,show_coin_ids=True,purchases=purchases,summarize_purchases=False)

            # Only one coin found, so select it
            if len(entries) == 1:
                entry = entries[0]
                coin_id = entry[mapping["coin_id"]]
                for _,country in x:
                    for _, denomination in country:
                        for _, value in denomination:
                            for _, coin in value:
                                return (coin_id,coin)

            # More than one coin found, so get user to refine search
            else:
                x.set_fancy(config["tree_fancy_characters"],cascade=True)
                for line in x.print():
                    print(line)
                print(CenterText("", filler_character="-", width=80))
                print(f"{len(entries)} results found. Please refine your search or use the coin id found within curly brackets.")

        else:
            print("No results found. Try again...")



def SelectPurchase(db, coin)->tuple:
    """ Gets the user to pick one purchase associated with the coin.

    Args:
        db (DB_Interface): Object for interacting with the database
        coin (Tree): A tree object with purchases in its nodes member 

    Returns: A tuple of (purchase_id, specific_coin_id, Purchase object)
        
    """
    coin_id, coin = coin

    # coin is a Tree object, so iterate through its nodes to get
    # all of its purchases
    purchases = [x for (_,x) in coin]

    if not purchases:
        print("No purchases found.")
        exit(1)

    # Gets the user to pick one of the purchases associated with the coin
    purchase_id = SelectEntry(purchases)

    # Some error occured when selecting a purchase
    if purchase_id is None:
        print("Error with purchase")
        exit(1)

    # Indicate which purchase was selected
    purchase = purchases[purchase_id]
    print(f"Selected: {purchase}")

    purchase = (purchase.purchase_id, purchase.specific_coin_id, purchases[purchase_id])
    return purchase


def PrintResult(result, item, exit_on_fail:bool=True):
    """ Prints whether a delete operation was successful, and optionally exits on failure

    Args:
        result (): A truthy value that indicates success or not
        item (): The item indicating what the delete failed on
        exit_on_fail: Pass False to not exit on result evaluating to False 
    """
    if result:
        print(f"Successfully deleted {item}")
    else:
        print(f"Failed to delete {item}")
        if exit_on_fail:
            exit(1)


def AlterDatabaseConfirmation()->bool:
    """ Gets confirmation that the user would like to modify the database

    Returns: True / False for continuing
        
    """
    print(CenterText("Warning", filler_character="-", width=80))
    return GetConfirmation(
        "Continuing will alter the database. Continue?"
    )  # Ensures user wants to continue


def Start(args, db, purchases, config):
    while True:

        # Delete mode
        if args["delete"]:

            # Gets the user to select a coin
            coin = GetCoinInformation(db, {"show_only_owned": True}, purchases, config=config)

            # Gets the user to select a purchase associated with the coin
            purchase = SelectPurchase(db, coin)

            # Gets confirmation to continue
            if AlterDatabaseConfirmation():

                # Deletes purchase
                result = db.DeleteById({"purchases": purchase[0]})
                PrintResult(result, purchase[2])

                # Check if specific_coin is used by other purchases
                if purchase[1] is not None and not db.FetchPurchasesWithSpecificCoinId(
                    purchase[1]
                ):
                    # It is not used, see if user wants to delete it
                    if GetConfirmation(
                        "No remaining coins use the specific_coin information of the deleted coin. Delete entry from specific_coins table?"
                    ):
                        result = db.DeleteById({"specific_coins": purchase[1]})
                        PrintResult(result, purchase[1])

                    # Specific coin is used by another purchase
                    else:
                        print("Keeping specific coin information")

            # User did not want to alter database
            else:
                print("Aborting...")
                exit(0)

        # Add purchase
        else:

            # Gets the user to select a coin
            coin = GetCoinInformation(db, config=config)

            # Gets the user to define the purchase details
            purchase = GetPurchaseInformation(config)

            # Gets the user to define the specific_coin if applicable
            specific_coin = GetSpecificCoinInformation()

            # Gets confirmation for continuing
            if AlterDatabaseConfirmation():

                # Adds the new purchase
                specific_coin_id = PushSpecificCoin(db, specific_coin, coin[0])
                PushPurchase(db, coin[0], purchase, specific_coin_id)

            # User did not want to continue
            else:
                print("Aborting...")
                exit(0)

        # Checks if the user wants to perform another operation
        if not GetConfirmation(
            f"{'Delete' if args['delete'] else 'Add'} another purchase?"
        ):
            break


if __name__ == "__main__":
    print(
        "This script is not meant to be called on its own. Please use the main script."
    )
