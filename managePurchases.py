#   Author: Josh Gillum              .
#   Date: 10 February 2026          ":"         __ __
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


def GetPurchaseInformation(config):
    """Gets purchase date,quantity, and price from user"""
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
    price_by_unit = True  # True if price is per coin, False for price by lot.
    if purchase["quantity"] > 1:
        # If multiple coins purchased, checks if user wants to enter price per coin or for the entire lot
        if not GetConfirmation(
            "Enter price per coin? (No will have you enter price of entire purchase then calculate price per coin)"
        ):
            price_by_unit = False
    while True:  # Gets price from the user
        try:
            if price_by_unit:
                price = input("Enter price (per coin if multiple purchased): ")
                float(price)
            else:
                price = input("Enter price of total purchase: ")
                price = round(float(price) / quantity, 2)
        except ValueError:
            print("Price must be numeric.")
            continue
        purchase["unit_price"] = price
        break
    print(
        f"({date_string}) {config['currency_symbol']}{purchase['unit_price']} x {purchase['quantity']}"
    )
    return purchase


def GetSpecificCoinInformation():
    """Gets information for a specific coin entry from the user (mint year and mint mark)"""
    print(CenterText("Specific Coin", filler_character="-", width=80))
    specific_coin = {"year": None, "mintmark": None}
    if GetConfirmation("Enter specific coin details (year and/or mintmark)?"):
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
            if GetConfirmation(
                f"Is the year ({specific_coin['year']}) and mintmark ({specific_coin['mintmark']}) correct?"
            ):
                break
            specific_coin["year"] = specific_coin["mintmark"] = None
    return specific_coin


def PushSpecificCoin(db, specific_coin, coin):
    specific_coin_id = None

    # Pushes the specific coin to the specific_coins table
    if specific_coin["year"] or specific_coin["mintmark"]:
        entries = db.FetchSpecificCoin(
            coin[0], year=specific_coin["year"], mintmark=specific_coin["mintmark"]
        )
        if entries:
            specific_coin_id = entries[0][0]
        else:
            results = db.AddSpecificCoin(
                coin[0], specific_coin["year"], specific_coin["mintmark"]
            )
            if not results:
                exit(1)
            entries = db.FetchSpecificCoin(
                coin[0], year=specific_coin["year"], mintmark=specific_coin["mintmark"]
            )
            if not entries:
                exit(1)
            print("Added specific coin successfully")
            specific_coin_id = entries[0][0]
    else:  # User did not specify a specific coin
        specific_coin_id = None
    return specific_coin_id


def PushPurchase(db, coin, purchase, specific_coin_id):
    # Some error occured while trying to push to purchases table
    if not db.AddPurchase(
        {
            "coin_id": coin[0],
            "purchase_date": purchase["date"],
            "unit_price": purchase["unit_price"],
            "quantity": purchase["quantity"],
            "specific_coin_id": specific_coin_id,
        }
    ):
        print("FAILED to add purchase")
        exit(1)
    else:  # Successful
        print("Added purchase successfully.")


def GetCoinInformation(db, additional_search_args: dict = None, config={}):
    print(CenterText("Find Coin", filler_character="-", width=80))
    # Prompts user for information to search for a coin
    while True:
        coin_find_by_id = True
        if GetConfirmation("Use search string instead of coin id?"):
            coin_find_by_id = False
        if coin_find_by_id:
            coin_id = input("Coin id: ")
            entries = db.FetchCoinById(coin_id)
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
            break
        else:
            print("No results found. Try again...")

    entry_id = 0
    if len(entries) > 1:
        print("Multiple results found...")
    for i in range(len(entries)):
        entry = entries[i]
        temp_coin = CoinData(
            weight=entry[mapping["gross_weight"]],
            fineness=entry[mapping["fineness"]],
            precious_metal_weight=entry[mapping["precious_metal_weight"]],
            years=entry[mapping["years"]],
            metal=entry[mapping["metal"]],
            nickname=entry[mapping["coin_display_name"]],
            face_value=entry[mapping["value"]],
            denomination=entry[mapping["denomination_display_name"]],
            country=entry[mapping["country_display_name"]],
            config=config,
        )
        temp_coin.TogglePrice(False)
        temp_output = temp_coin.Print("%c %F %d " + temp_coin.GetCoinString())
        entries[i] = (entry[0], temp_output)  # Tuple of (coin_id, coin string)
    entry_id = SelectEntry(
        [x[1] for x in entries]
    )  # Gets entry from list of coin strings

    coin = entries[entry_id]
    print(f"Selected: {coin[1]}")
    return coin


def SetMetals(db):
    prices = {}
    entries = db.FetchMetals()
    print(entries)
    for entry in entries:
        key, name, price, date = entry
        prices[key] = (name, float(price), date)
    data.metals = prices


def SelectPurchase(db, coin, config):
    purchases = db.FetchPurchasesByCoinId(coin[0], True, True)
    if not purchases:
        print("No purchases found.")
        exit(1)
    # Creates a list of tuples of (purchase_id,specific_coin_id,Purchase object).
    # They are then sorted by purchase date
    purchases = sorted(
        [
            (
                x[7],
                x[8],
                Purchase(*(x[1:4] + x[5:7])),
                config["date_format"],
                config["currency_symbol"],
                config["show_color"],
                config["colors_8_bit"],
                config["types_colors"]["purchase"],
            )
            for x in purchases
        ],
        key=lambda x: x[2].purchase_date,
    )
    purchase_id = SelectEntry([x[2] for x in purchases])
    purchase = purchases[purchase_id]
    print(f"Selected: {purchase[2]}")
    if purchase[0] is None:
        print("Error with purchase")
        exit(1)
    return purchase


def PrintResult(result, item, exit_on_fail=True):
    if result:
        print(f"Successfully deleted {item}")
    else:
        print(f"Failed to delete {item}")
        if exit_on_fail:
            exit(1)


def AlterDatabaseConfirmation():
    print(CenterText("Warning", filler_character="-", width=80))
    return GetConfirmation(
        "Continuing will alter the database. Continue?"
    )  # Ensures user wants to continue


def Start(args, db, config):
    while True:
        if args["delete"]:  # Delete mode
            coin = GetCoinInformation(db, {"show_only_owned": True}, config=config)
            purchase = SelectPurchase(db, coin, config)
            if AlterDatabaseConfirmation():
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
                    else:
                        print("Keeping specific coin information")
            else:  # User didn't want to alter database
                print("Aborting...")
                exit(0)
        else:  # Default add mode
            coin = GetCoinInformation(db, config=config)
            purchase = GetPurchaseInformation(config)
            specific_coin = GetSpecificCoinInformation()
            if AlterDatabaseConfirmation():
                specific_coin_id = PushSpecificCoin(db, specific_coin, coin)
                PushPurchase(db, coin, purchase, specific_coin_id)
            else:
                print("Aborting...")
                exit(0)
        if not GetConfirmation(
            f"{'Delete' if args['delete'] else 'Add'} another purchase?"
        ):
            break


if __name__ == "__main__":
    print(
        "This script is not meant to be called on its own. Please use the main script."
    )
