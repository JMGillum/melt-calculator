#   Author: Josh Gillum              .
#   Date: 7 February 2026           ":"         __ __
#                                  __|___       \ V /
#                                .'      '.      | |
#                                |  O       \____/  |
# ~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
#
#    This script is used to backup information stored in the database
#
# ~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
from db.interface import DB_Interface
from db.queries import Queries
from datetime import datetime
from pathlib import Path
import treasure.config
import treasure.text


def ConvertSQL(query, values):
    for item in values:
        query = query.replace("?", f'"{item}"', 1)
    return query


def BackupPurchases(db:DB_Interface, dir:Path):
    specific_coins = {}
    purchases = db.FetchPurchases()
    current_specific_coin_id = 1
    purchases = sorted(purchases, key=lambda purchase: purchase[3])
    purchase_queries = []
    specific_coin_queries = []
    for purchase in purchases:
        purchase_args = {
            "coin_id": purchase[0],
            "purchase_date": purchase[3],
            "unit_price": purchase[1],
            "quantity": purchase[2],
        }
        if purchase[4] is not None:
            try:
                specific_coins[purchase[4]]
            except KeyError:
                specific_coins[purchase[4]] = (
                    current_specific_coin_id,
                    purchase[0],
                    purchase[5],
                    purchase[6],
                )
                current_specific_coin_id += 1
            purchase_args["specific_coin_id"] = specific_coins[purchase[4]][0]
        purchase_queries.append(Queries.AddPurchase(**purchase_args))
    for key in specific_coins.keys():
        _, coin_id, year, mintmark = specific_coins[key]
        specific_coin_queries.append(Queries.AddSpecificCoin(coin_id, year, mintmark))
    output_file = dir / Path("purchases.sql")
    with open(output_file, "w") as f:
        f.write("--Specific coins\n")
        for item in specific_coin_queries:
            f.write(ConvertSQL(*item))
            f.write("\n")
        f.write("\n")
        f.write("--Purchases\n")
        for item in purchase_queries:
            f.write(ConvertSQL(*item))
            f.write("\n")


def BackupResults(results, table, columns, dir, file_name, append):
    if not results:
        return

    output_file = dir / Path(file_name)
    write_mode = "w"
    if append:
        write_mode = "a"
    with open(output_file, write_mode) as f:

        # Print out every result as an insert statement.
        for line in results:
            f.write(f"INSERT INTO {table}({', '.join(columns)}) VALUES(")
            for i in range(len(line)):
                if line[i] is not None:

                    # Has to print out quotes around text if a string, as well escape quotes
                    if isinstance(line[i],str):
                        f.write(f"'{treasure.text.EscapeQuotes(line[i])}'")
                    else:
                        f.write(str(line[i]))

                # None type needs to be NULL in SQL
                else:
                    f.write("NULL")

                # Writes comma for all except last line
                if i < len(line)-1:
                    f.write(", ")
            
            f.write(");\n")


def BasicBackup(db:DB_Interface,dir:Path,columns:list[str],table:str,file_name:str,append:bool=False,order_by:str=None,filter_by_series=True,series=None):
    """ Performs a standardized, basic backup of the specified columns of the spcified table.

    Args:
        append: True to append to file instead of truncating 
        order_by: Pass a str to append "ORDER BY {order_by}" to the end of the query. None will abstain from order by 
        db: db_interface object for interacting with database
        dir: Path to directory that will store file
        columns: List of columns to backup
        table: Name of table to backup
        file_name: Name of file to store backup in
    """

    # Build query
    query = f"SELECT {','.join(columns)} FROM {table}"
    if order_by:
        query += f" ORDER BY {order_by}"
    query += ";"

    results = []
    if filter_by_series:

        # Backup all series separately if not explicitly specified
        if series is None:
            series = db.Fetch(f"SELECT DISTINCT series FROM {table}")
            series = list(series)

        # Recursively backup each series
        if isinstance(series,list) or isinstance(series,tuple):
            print(series)
            for item in series:
                if (isinstance(item,tuple) or isinstance(item,list)) and len(item) == 1:
                    item = item[0]
                print(item)
                print(len(item))
                BasicBackup(db,dir,columns,table,f"{item}_{file_name}",append,order_by,filter_by_series=True,series=item)
            return
        else:
            query = query[:-1]
            query += " WHERE series=?;"
            results = db.Fetch(query,(f"{series}",))

    # Do no filtering by series, just put all series in this file
    else:
        results = db.Fetch(query)

    BackupResults(results, table, columns, dir, file_name, append)



def BackupConfig(dir:Path):
    """ Performs a backup of the config file

    Args:
        dir: Path to directory that will store backup

    Returns: True if config exists, False if it doesnt
        
    """

    config_path = treasure.config.DefaultConfigPath("metals")
    if config_path is not None:

        # Simply read every line and write it at same time
        input = config_path / "config.toml"
        output = Path(dir) / "config.toml"
        with input.open(mode="r") as i:
            with output.open(mode="w") as f:
                for line in i:
                    f.write(line)
        return True
    return False


def Backup(args, db: DB_Interface, dir=None):
    """Performs backups of the database."""
    # If no specific file is specified, all will undergo backup
    if not (
        args["backup_purchases"]
        or args["backup_countries"]
        or args["backup_denominations"]
        or args["backup_face_values"]
        or args["backup_coins"]
        or args["backup_config"]
    ):
        args["backup_all"] = True

    if dir is None:
        dir = (
            Path.cwd() / Path("database") / Path("backups")
        )  # default location is ./database/backups
    else:
        dir = Path(dir)
    if args["output_destination"]:  # Backup location was specified in command line
        dir = Path(args["output_destination"])
    try:
        # Attempts to create directory that will store all backups
        if args["verbose"]:
            print(f"Attempting to create directory: {dir}")
        dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print(f"Permission denied. Unable to create the directory: {dir}")
        return 1
    try:
        # Backups are stored in a timestamped directory within the backups directory
        # Attempts to create that directory
        dir = dir / Path(datetime.now().strftime("%Y%m%d_%H%M%S"))
        if args["verbose"]:
            print(f"Attempting to create directory: {dir}")
        dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print(f"Permission denied. Unable to create the directory: {dir}")
        return 1

    # Performs each specific backup if specified
    if args["backup_purchases"] or args["backup_all"]:
        BackupPurchases(db, dir)
        print("Backup of purchases complete.")

    if args["backup_countries"] or args["backup_all"]:
        #BackupCountries(db, dir)
        BasicBackup(db,dir,["country_id","display_name","tags","series"],"countries","setup_countries.sql")
        BasicBackup(db,dir,["country_id","name"],"country_names","setup_countries.sql",append=True,filter_by_series=False)
        print("Backup of countries complete.")

    if args["backup_denominations"] or args["backup_all"]:
        #BackupDenominations(db, dir)
        BasicBackup(db,dir,["denomination_id","country_id","display_name","tags","series"],"denominations","setup_denominations.sql")
        BasicBackup(db,dir,["denomination_id","name"],"denomination_names","setup_denominations.sql",append=True,filter_by_series=False)
        print("Backup of denominations complete.")

    if args["backup_face_values"] or args["backup_all"]:
        #BackupValues(db, dir)
        BasicBackup(db,dir,["value_id","denomination_id","value","display_name","tags","series"],"face_values","setup_values.sql")
        BasicBackup(db,dir,["value_id","name"],"face_values_names","setup_values.sql",append=True,order_by="value_id",filter_by_series=False)
        print("Backup of face values complete.")

    if args["backup_coins"] or args["backup_all"]:
        print("No backup for coins is available yet")
        print("Backup of coins complete.")
        pass

    if args["backup_config"] or args["backup_all"]:
        if BackupConfig(dir):
            print("Backup of config complete.")
        else:
            print("Backup of config failed.")
    return 0


if __name__ == "__main__":
    print(
        "This script is not meant to be called on its own. Please use the main script."
    )
