#!/usr/bin/env python3
#   Author: Josh Gillum              .
#   Date: 5 March 2026              ":"         __ __
#                                  __|___       \ V /
#                                .'      '.      | |
#                                |  O       \____/  |
# ~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
#
#    This script is a useful tool for figuring out the intrinsic or "melt"
#    value of various different world coins. It prints them out in a tree
#    structure.
#
#    Supported features accessible through this script:
#    * Core search functionality
#    * Report of owned coins and a profit report
#    * Management of purchases
#    * Database backups
#    * Metal price updates
#
#    Run the script with the '--help' flag to see a list of a supported command
#    line arguments. In general, the arguments will be:
#       main.py <mode> <optional submode> [flags]
#
#    The '--help' flag can be appended after any mode and viable optional submode
#    combination to list the valid command line options for it.
#
#    Setup of a database is required before this script will be operational.
#    By default, the database is mariadb. This can be changed by updating the
#    db_config dictionary in config.py, the various functions in the
#    DB_Interface class in db_interface.py, and potentially the SQL queries in
#    queries.py (Only if the new database uses a different form of SQL than
#    mariadb).
#
#    Make sure to read README.md or README.txt for more information
#    about the program, how to set it up, and how to use it to its fullest
#    potential.
#
#    Thank you.
#
# ~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~


# Scripts for various operation modes
from check_config import ValidateConfig

if __name__ == "__main__":
    config, errors = ValidateConfig()
    for error in errors:
        print(error, flush=True)
    if config is None:
        print("Config error. Aborting...")
        exit(1)

    # Only import modules if config file is setup correctly
    # import config # Various config information
    from setup import InitialSetup, SetupMetals, InitColoredText  # Sets up argument parser and metals
    from db.interface import DB_Interface  # Manages connecting to the database

    import managePurchases
    import updateMetalPrices
    import addCoins
    import backup
    import report
    import search
    import setup_db
    import update_db


    # Sets up argument parser and then parses them
    args = InitialSetup(config)

    # Sets up colored text
    if not InitColoredText(config,args["verbose"]):
        print("Unable to initialize colored text", flush=True)
        exit(1)

    if args["command"] in ["manage-purchases", "report", "admin", "search"]:
        try:
            # Perform setup for whichever operation mode
            # Connects to database
            db = DB_Interface(debug=args["verbose"])
            db.Connect(config["db_config"])

            skip_setup_metals = False
            # These do not need access to purchases or pricing, so execute them
            if args["command"] == "admin":
                # Backs up database entries for the various tables
                if args["admin_command"] == "backup":
                    backup.Backup(args, db, dir=config["backup_path"])
                    skip_setup_metals = True

                # Adds new coins
                elif args["admin_command"] == "new-items":
                    addCoins.AddCoins(db, args["prefix"], config)
                    skip_setup_metals = True

                # Setup database
                elif args["admin_command"] == "setup-db":
                    status, errors = setup_db.Start(db,args,config)
                    if status > 0:
                        for error in errors:
                            print(error)
                        print("",end="",flush=True)
                        exit(1)
                    skip_setup_metals = True

                # Update database
                elif args["admin_command"] == "update-db":
                    status, errors = update_db.Start(db,args,config)
                    if status > 0:
                        for error in errors:
                            print(error)
                        print("",end="",flush=True)
                        exit(1)
                    skip_setup_metals = True

            if not skip_setup_metals:
                # Fetches all of the purchases and sets up and fetches metal prices
                purchases, prices = SetupMetals(db, args, config)

            # Collection report
            if args["command"] == "report":
                report.CollectionReport(args, db, purchases, prices, config)

            # Manage purchases for collection
            elif args["command"] == "manage-purchases":
                managePurchases.Start(args, db, purchases, config)

            # The operation mode is manage, which is managing various database components
            elif args["command"] == "admin":

                # Updates metal prices
                if args["admin_command"] == "prices":
                    updateMetalPrices.GetMetalPricesFromUser(db, prices, config)


            # The operation mode is search, which will search the database for coins.
            elif args["command"] == "search":
                search.Search(args, db, purchases, prices, config)

            # Other / undefined operation mode
            else:
                print(f"Error: Unknown command type: {args['command']}")
        finally:
            # Close Cursor and Connection
            db.CloseConnection()
