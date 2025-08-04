"""
   Author: Josh Gillum              .
   Date: 3 August 2025             ":"         __ __
                                  __|___       \ V /
                                .'      '.      | |
                                |  O       \____/  |
^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

    This class is an abstraction for connecting to the database. It should be
    updated if the database ever changes, so that calling code does not need
    to change.

^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
"""

import sys
import mariadb
import getpass

from queries import Queries

class DB_Interface:
    def __init__(self,debug=False):
        self.conn = None
        self.cursor = None
        self.debug = debug

    def connect(self,db_config,debug=None):
        if self.debug and debug is None:
            debug = True
        try:
            password = db_config["password"]
        except KeyError:
            password = db_config["password"] = None
        # Gets the password from the user if it is not pre defined
        if password is None:
            # getpass function will not work if stdin is not a terminal (user couldn't enter password)
            if not sys.stdin.isatty():
                print(
                    "The program must be run from a terminal or password must be supplied in db_config"
                )
                sys.exit(1)
            else:
                db_config["password"] = getpass.getpass(f"Password for mariadb database({db_config['database']}): ")

        try:
            # Creates the connection
            if debug:
                print("Connecting to MariaDB...")
            conn = mariadb.connect(**db_config)
            if debug:
                print("Connection successful!")

            # 3. Create a Cursor Object
        except mariadb.Error as e:
            print(f"An error occurred: {e}")
            sys.exit(1)
        self.conn = conn
        self.cursor = conn.cursor()

    def closeConnection(self,debug=None):
        if self.debug and debug is None:
            debug = self.debug
        if self.cursor:
            self.cursor.close()
            if debug:
                print("Cursor closed.")
        if self.conn:
            self.conn.close()
            if debug:
                print("Connection closed.")

    def fetch(self,*args):
        """Submits a query to the database"""
        if self.cursor:
            try:
                self.cursor.execute(*args)
            except mariadb.Error as e:
                print(f"An error occured: {e}")
                sys.exit(1)
            return list(self.cursor)

    def fetchPurchases(self):
        """Gets all of the defined searches"""
        return self.fetch(Queries.purchases())

    def fetchCountryNames(self):
        """Gets all of the names of every country"""
        return self.fetch(Queries.countryNames())

    def fetchMetals(self):
        return self.fetch(Queries.metals())

    def fetchCoins(self,search_arguments):
        """search_arguments should be a dictionary for **kwargs of Queries.search()"""
        results = Queries.search(**search_arguments)
        return self.fetch(results[0],results[1])
