#   Author: Josh Gillum              .
#   Date: 7 February 2026           ":"         __ __
#                                  __|___       \ V /
#                                .'      '.      | |
#                                |  O       \____/  |
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
#
#    This script is used to backup information stored in the database
#
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
from db.interface import DB_Interface
import config
from db.queries import Queries
from datetime import datetime
from pathlib import Path

def ConvertSQL(query,values):
    for item in values:
        query = query.replace("?",f'"{item}"',1)
    return query

def BackupPurchases(db,dir):
    specific_coins = {}
    purchases = db.FetchPurchases()
    current_specific_coin_id = 1
    purchases = sorted(purchases,key= lambda purchase: purchase[3])
    purchase_queries = []
    specific_coin_queries = []
    for purchase in purchases:
        purchase_args = {"coin_id": purchase[0],"purchase_date":purchase[3],"unit_price":purchase[1],"quantity":purchase[2]}
        if purchase[4] is not None:
            try:
                specific_coins[purchase[4]]
            except KeyError:
                specific_coins[purchase[4]] = (current_specific_coin_id,purchase[0],purchase[5],purchase[6])
                current_specific_coin_id += 1
            purchase_args["specific_coin_id"] = specific_coins[purchase[4]][0]
        purchase_queries.append(Queries.AddPurchase(**purchase_args))
    for key in specific_coins.keys():
        _,coin_id,year,mintmark = specific_coins[key]
        specific_coin_queries.append(Queries.AddSpecificCoin(coin_id,year,mintmark))
    output_file = dir / Path("purchases.sql")
    with open(output_file,"w") as f:
        f.write("--Specific coins\n")
        for item in specific_coin_queries:
            f.write(ConvertSQL(*item))
            f.write("\n")
        f.write("\n")
        f.write("--Purchases\n")
        for item in purchase_queries:
            f.write(ConvertSQL(*item))
            f.write("\n")

def BackupCountries(db,dir):
    countries = db.Fetch("SELECT country_id,display_name,tags FROM countries;")
    country_names = db.Fetch("SELECT country_id,name FROM country_names;")

    output_file = dir / Path("setup_countries.sql")
    with open(output_file,"w") as f:
        for line in countries:
            f.write(f"INSERT INTO countries(country_id, display_name, tags) VALUES{line};\n")
        for line in country_names:
            f.write(f"INSERT INTO country_names(country_id, name) VALUES{line};\n")


def BackupDenominations(db,dir):
    denominations = db.Fetch("SELECT denomination_id,country_id,display_name,tags FROM denominations;") 
    denomination_names = db.Fetch("SELECT denomination_id,name FROM denomination_names;")

    output_file = dir / Path("setup_denominations.sql")
    with open(output_file,"w") as f:
        for line in denominations:
            f.write(f"INSERT INTO denominations(denomination_id, country_id, display_name, tags) VALUES{line};\n")
        for line in denomination_names:
            f.write(f"INSERT INTO denomination_names(denomination_id, name) VALUES{line};\n")


def BackupValues(db,dir):
    values = db.Fetch("SELECT value_id,denomination_id,value,display_name,tags FROM face_values;")
    value_names = db.Fetch("SELECT value_id,name FROM face_values_names ORDER BY value_id;")

    output_file = dir / Path("setup_values.sql")
    with open(output_file,"w") as f:
        for line in values:
            f.write(f"INSERT INTO face_values(value_id, denomination_id, value, display_name, tags) VALUES(\"{line[0]}\", \"{line[1]}\", {str(line[2])}, {'NULL' if line[3] is None or line[3].upper() == 'NULL' else f'\"{line[3]}\"'}, '{line[4]}');\n")
        for line in value_names:
            f.write(f"INSERT INTO face_values_names(value_id, name) VALUES{line};\n")


def BackupConfig(dir):
    output_file = dir / Path("config.py")
    with open("config.py","r") as i:
        with open(output_file,"w") as f:
            for line in i:
                f.write(line)


def Backup(args,db: DB_Interface):
    """Performs backups of the database. """
    # If no specific file is specified, all will undergo backup
    if not (args["backup_purchases"] or 
        args["backup_countries"] or 
        args["backup_denominations"] or 
        args["backup_face_values"] or 
        args["backup_coins"] or 
        args["backup_config"]
            ):
        args["backup_all"] = True


    dir = Path.cwd() / Path("db") / Path("backups") # default location is ./db/backups
    if args["output_destination"]: # Backup location was specified in command line
        dir = Path(args["output_destination"])
    try:
        # Attempts to create directory that will store all backups
        if args["verbose"]:
            print(f"Attempting to create directory: {dir}")
        dir.mkdir(parents=True,exist_ok=True)
    except PermissionError:
        print(f"Permission denied. Unable to create the directory: {dir}")
        return 1
    try:
        # Backups are stored in a timestamped directory within the backups directory
        # Attempts to create that directory
        dir = dir / Path(datetime.now().strftime('%Y%m%d_%H%M%S'))
        if args["verbose"]:
            print(f"Attempting to create directory: {dir}")
        dir.mkdir(parents=True,exist_ok=True)
    except PermissionError:
        print(f"Permission denied. Unable to create the directory: {dir}")
        return 1

    # Performs each specific backup if specified
    if args["backup_purchases"] or args["backup_all"]:
        BackupPurchases(db,dir)
        print("Backup of purchases complete.")

    if args["backup_countries"] or args["backup_all"]:
        BackupCountries(db,dir)
        print("Backup of countries complete.")

    if args["backup_denominations"] or args["backup_all"]:
        BackupDenominations(db,dir)
        print("Backup of denominations complete.")

    if args["backup_face_values"] or args["backup_all"]:
        BackupValues(db,dir)
        print("Backup of face values complete.")

    if args["backup_coins"] or args["backup_all"]:
        print("No backup for coins is available yet")
        print("Backup of coins complete.")
        pass

    if args["backup_config"] or args["backup_all"]:
        BackupConfig(dir)
        print("Backup of config complete.")
    return 0

if __name__ == "__main__":
    print("This script is not meant to be called on its own. Please use the main script.")
