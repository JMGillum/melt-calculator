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


def BasicBackup(db:DB_Interface,dir:Path,columns:list[str],table:str,file_name:str,append:bool=False,order_by:str=None,filter_by_series:bool=True,series:list[str]=None,table_for_checking_series:str=None,joined_tables:list[tuple]=None):

    """ Performs a backup of a table. Allows for specifying which series of information to filter.

    Args:
        db: The db interface to connect to
        dir: Directory to save the output file(s) in.
        columns: Which columns of the table to save.
        table: Which table to save
        file_name: Base portion of file name (Will be prepended with {series}_ for each series)
        append: Write mode for opening the file. True to append, False or None to truncate
        order_by: Appends 'ORDER BY {order_by}' to the query. Changes which column to sort results by
        filter_by_series: Enables or disables filtering by series.
        series: Which series to backup. None will backup all series.
        table_for_checking_series: Will determine which series are present based on values found in this table.
        joined_tables: list of tuples to be passed to Queries.FilterBySeries()
    """
    results = []
    if filter_by_series:

        # Backup all series separately if not explicitly specified
        if series is None:
            if table_for_checking_series is None:
                table_for_checking_series = table
            series = list(db.Fetch(Queries.SeriesPresentInTable(table_for_checking_series)))

        # Recursively backup each series
        if isinstance(series,list) or isinstance(series,tuple):
            #print(series)
            for item in series:
                if (isinstance(item,tuple) or isinstance(item,list)) and len(item) == 1:
                    item = item[0]
                #print(item)
                #print(len(item))
                BasicBackup(db,dir,columns,table,f"{item}_{file_name}",append,order_by,filter_by_series=True,series=item,joined_tables=joined_tables)
            return
        else:
            query, args = Queries.FilterBySeries(columns,table,series,joined_tables)
            #print(query)
            if order_by:
                query.replace(";",f" ORDER BY {order_by};")
            results = db.Fetch(query,args)

    # Do no filtering by series, just put all series in this file
    else:
        # Build query
        query = f"SELECT {','.join(columns)} FROM {table}"
        if order_by:
            query += f" ORDER BY {order_by}"
        query += ";"
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
        dir = Path.cwd()
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
        BasicBackup(db,dir,["id","coin_id","year","mintmark"],"specific_coins","setup_purchases.sql",table_for_checking_series="coins",joined_tables=[("coins","coin_id")])
        BasicBackup(db,dir,["purchase_id","coin_id","purchase_date","unit_price","purchase_quantity","specific_coin"],"purchases","setup_purchases.sql",table_for_checking_series="coins",joined_tables=[("coins","coin_id")],append=True)
        print("Backup of purchases complete.")

    if args["backup_countries"] or args["backup_all"]:
        BasicBackup(db,dir,["country_id","display_name","tags","series"],"countries","setup_countries.sql")
        BasicBackup(db,dir,["country_id","name"],"country_names","setup_countries.sql",append=True,table_for_checking_series="countries",joined_tables=[("countries","country_id")])
        print("Backup of countries complete.")

    if args["backup_denominations"] or args["backup_all"]:
        BasicBackup(db,dir,["denomination_id","country_id","display_name","tags","series"],"denominations","setup_denominations.sql")
        BasicBackup(db,dir,["denomination_id","name"],"denomination_names","setup_denominations.sql",append=True,table_for_checking_series="denominations",joined_tables=[("denominations","denomination_id")])
        print("Backup of denominations complete.")

    if args["backup_face_values"] or args["backup_all"]:
        BasicBackup(db,dir,["value_id","denomination_id","value","display_name","tags","series"],"face_values","setup_values.sql")
        BasicBackup(db,dir,["value_id","name"],"face_values_names","setup_values.sql",append=True,order_by="value_id",table_for_checking_series="face_values",joined_tables=[("face_values","value_id")])
        print("Backup of face values complete.")

    if args["backup_coins"] or args["backup_all"]:
        BasicBackup(db,dir,["coin_id","face_value_id","gross_weight","fineness","precious_metal_weight","tags","metal","name","series"],"coins","setup_coins.sql")
        BasicBackup(db,dir,["coin_id","year","tags"],"years","setup_coins_years.sql",table_for_checking_series="coins",joined_tables=[("coins","coin_id")])
        print("Backup of coins complete.")

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
