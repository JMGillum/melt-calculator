#!/usr/bin/env python3
#   Author: Josh Gillum              .
#   Date: 19 January 2026           ":"         __ __
#                                  __|___       \ V /
#                                .'      '.      | |
#                                |  O       \____/  |
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
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
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~


# Scripts for various operation modes
from check_config import validateConfig

    
if __name__ == "__main__":
    if validateConfig():
        print("Config error. Aborting...")
        exit(1)

    # Only import modules if config file is setup correctly
    import config # Various config information

    from setup import initialSetup,setupMetals # Sets up argument parser and metals
    from db_interface import DB_Interface # Manages connecting to the database

    import managePurchases
    import updateMetalPrices
    import backup
    import report
    import search
    # Sets up argument parser and then parses them
    args = initialSetup()

    if args["command"] in ["collection","manage","search"]:
        try:  
            # Perform setup for whichever operation mode
            # Connects to database
            db = DB_Interface(debug=args["verbose"])
            db.connect(config.db_config)
            
            # Fetches all of the purchases and sets up and fetches metal prices
            purchases,prices = setupMetals(db,args)


            # Determines which operation mode to enter, and what to do
            # The operation mode is collection, which manages or views purchases
            if args["command"] == "collection":
                # Collection report
                if args["collection_command"] == "report":
                    report.collectionReport(args,db,purchases,prices)

                # Manage purchases for collection
                if args["collection_command"] == "manage":
                    managePurchases.start(args,db)
            
            # The operation mode is manage, which is managing various database components
            elif args["command"] == "manage":

                # Backs up database entries for the various tables
                if args["manage_command"] == "backup":
                    backup.backup(args,db)

                # Updates metal prices
                elif args["manage_command"] == "prices":
                    updateMetalPrices.getMetalPricesFromUser(db,prices)

            # The operation mode is search, which will search the database for coins.
            elif args["command"] == "search":
                search.search(args,db,purchases,prices)

            # Other / undefined operation mode
            else:
                print(f"Error: Unknown command type: {args['command']}")
        finally:
            # Close Cursor and Connection
            db.closeConnection()
