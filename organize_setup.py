
#   Author: Josh Gillum              .
#   Date: 8 September 2025          ":"         __ __
#                                  __|___       \ V /
#                                .'      '.      | |
#                                |  O       \____/  |
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
#
#    This script is a useful tool for figuring out the intrinsic or "melt"
#    value of various different world coins. It prints them out in a tree
#    structure.
#
#    Searching for specific coins or groups of coins is also supported. Searches
#    can be as specific as '1898 German 10 Mark', or simply '1866'. The first
#    would show the single coin (along with its associated country and
#    denomination). The second search would simply return all coins that were
#    minted in 1866.
#
#    Run the script with the '--help' flag to see a list of a supported command
#    line arguments. The most useful of which are probably:
#        -S <search_string> this allows you to provide a string representing
#            your search query
#        -s <silver_price> this allows you to supply the silver price to be
#            used when calculating value
#        -g <gold_price> same as with silver price, but for gold.
#        -p <platinum_price> same as above, but for platinum.
#        -P <palladium_price> same as above, but for palladium.
#
#    * Checkout data.py to change the default precious metal prices used
#    when one isn't supplied
#
#    * Purchases are supported, but no script is yet available for adding them.
#
#    Finally, make sure to read README.md or README.txt for more information
#    about the program and how to use it to its fullest potential.
#
#    Thank you.
#
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

import data as d
from coins import Coins
import config
import general

from datetime import datetime
import sys  # Used to check if stdin is not from a terminal (piping input)
from setup import setupParser
from db_interface import DB_Interface
from updateMetalPrices import updateMetalPrices
from colorama import just_fix_windows_console

if __name__ == "__main__":
    just_fix_windows_console() # Enables ANSI code support on windows or strips them if necessary
    # Command line arguments
    parser = setupParser()
    args = vars(parser.parse_args())
    if args["verbose"]:
        print(f"arguments: {args}")

    # The database was specified in the command line
    if args["database"]:
        config.db_config["database"] = args["database"]

    try:  # Connects to database
        db = DB_Interface(debug=args["verbose"])
        db.connect(config.db_config)

        countries = db.fetch("SELECT country_id,display_name,tags FROM countries;")
        country_names = db.fetch("SELECT country_id,name FROM country_names;")

        with open("./db/setup_countries.sql.organized","w") as f:
            for line in countries:
                f.write(f"INSERT INTO countries(country_id, display_name, tags) VALUES{line};\n")
            for line in country_names:
                f.write(f"INSERT INTO country_names(country_id, name) VALUES{line};\n")

        denominations = db.fetch("SELECT denomination_id,country_id,display_name,tags FROM denominations;") 
        denomination_names = db.fetch("SELECT denomination_id,name FROM denomination_names;")

        with open("./db/setup_denominations.sql.organized","w") as f:
            for line in denominations:
                f.write(f"INSERT INTO denominations(denomination_id, country_id, display_name, tags) VALUES{line};\n")
            for line in denomination_names:
                f.write(f"INSERT INTO denomination_names(denomination_id, name) VALUES{line};\n")

        values = db.fetch("SELECT value_id,denomination_id,value,display_name,tags FROM face_values;")
        value_names = db.fetch("SELECT value_id,name FROM face_values_names ORDER BY value_id;")

        with open("./db/setup_values.sql.organized","w") as f:
            for line in values:
                f.write(f"INSERT INTO face_values(value_id, denomination_id, value, display_name, tags) VALUES(\"{line[0]}\", \"{line[1]}\", {str(line[2])}, {'NULL' if line[3] is None or line[3].upper() == 'NULL' else f'\"{line[3]}\"'}, '{line[4]}');\n")
            for line in value_names:
                f.write(f"INSERT INTO face_values_names(value_id, name) VALUES{line};\n")

    finally:
        # 4. Close Cursor and Connection
        db.closeConnection()
