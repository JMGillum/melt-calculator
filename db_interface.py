"""
   Author: Josh Gillum              .
   Date: 2 August 2025             ":"         __ __
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
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self,db_config):
        try:
            password = db_config["password"]
        except KeyError:
            password = db_config["password"] = None
        if password is None:
            if not sys.stdin.isatty():
                print(
                    "The program must be run from a terminal or password must be supplied in db_config"
                )
                sys.exit(1)
            else:
                db_config["password"] = getpass.getpass("Password for mariadb: ")

        try:
            print("Connecting to MariaDB...")
            conn = mariadb.connect(**db_config)
            print("Connection successful!")

            # 3. Create a Cursor Object
        except mariadb.Error as e:
            print(f"An error occurred: {e}")
            sys.exit(1)
        self.conn = conn
        self.cursor = conn.cursor()

    def closeConnection(self):
        if self.cursor:
            self.cursor.close()
            print("Cursor closed.")
        if self.conn:
            self.conn.close()
            print("Connection closed.")

    def fetchPurchases(self):
        if self.cursor:
            try:
                self.cursor.execute(Queries.purchases())
                return list(self.cursor)
            except mariadb.Error as e:
                print(f"An error occurred: {e}")
                sys.exit(1)

    def fetchCountryNames(self):
        if self.cursor:
            try:
                self.cursor.execute(Queries.countryNames())
                return list(self.cursor)
            except mariadb.Error as e:
                print(f"An error occurred: {e}")
                sys.exit(1)

    def fetchCoins(
        self,
        country=None,
        denomination=None,
        face_value=None,
        face_value_name=None,
        year=None,
        debug=False,
        show_only_owned=False,
        show_only_not_owned=False,
        ):
        if self.cursor:
            try:
                results = Queries.search(country=country,denomination=denomination,face_value=face_value,face_value_name=face_value_name,year=year,debug=debug,show_only_owned=show_only_owned,show_only_not_owned=show_only_not_owned)
                self.cursor.execute(results[0],results[1])
                return list(self.cursor)
            except mariadb.Error as e:
                print(f"An error occurred: {e}")
                sys.exit(1)
