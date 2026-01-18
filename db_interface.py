#   Author: Josh Gillum              .
#   Date: 18 January 2026           ":"         __ __
#                                  __|___       \ V /
#                                .'      '.      | |
#                                |  O       \____/  |
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
#
#    This class is an abstraction for connecting to the database. It should be
#    updated if the database ever changes, so that calling code does not need
#    to change.
#
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

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

    def update(self,*args):
        try:
            self.cursor.execute(*args)
            self.conn.commit()  # Commit the transaction for DML
            if self.debug:
                print(f"Inserted {self.cursor.rowcount} rows.")
                print(f"Last inserted ID: {self.cursor.lastrowid}")
            return True
        except mariadb.IntegrityError as e:
            print(f"Error updating data: {e}")
            self.conn.rollback()
            return False
        except mariadb.Error as e:
            print(f"Error inserting data: {e}")
            self.conn.rollback()
            return False

    def fetchPurchases(self):
        """Gets all of the defined searches"""
        return self.fetch(Queries.purchases())

    def fetchPurchasesByCoinId(self,coin_id,purchase_id=False,specific_coin_id=False):
        return self.fetch(*Queries.purchasesByCoinId(coin_id,purchase_id,specific_coin_id))

    def fetchCountryNames(self):
        """Gets all of the names of every country"""
        return self.fetch(Queries.countryNames())

    def fetchCountryId(self,country_name):
        """Returns the country id associated with the given country_name"""
        results = Queries.countryId(country_name)
        return self.fetch(results[0],results[1])

    def fetchCountryDisplayName(self,country_id):
        """Returns the display name associated with the given country_id"""
        results = Queries.countryDisplayName(country_id)
        return self.fetch(results[0],results[1])

    def fetchDenominationId(self,denomination_name):
        """Returns the denomination id associated with the given denomination_name"""
        results = Queries.denominationId(denomination_name)
        return self.fetch(results[0],results[1])

    def fetchDenominationDisplayName(self,denomination_id):
        """Returns the display name associated with the given denomination_id"""
        results = Queries.denominationDisplayName(denomination_id)
        return self.fetch(results[0],results[1])

    def fetchMetals(self):
        return self.fetch(Queries.metals())

    def fetchCoins(self,search_arguments):
        """search_arguments should be a dictionary for **kwargs of Queries.search()"""
        results = Queries.search(**search_arguments)
        return self.fetch(results[0],results[1])

    def updateMetalPrice(self,args):
        results = Queries.updateMetalPrice(*args)
        return self.update(*results)

    def fetchSpecificCoin(self,coin_id,year,mintmark):
        results = Queries.specificCoin(coin_id,year,mintmark)
        return self.fetch(results[0],results[1])

    def addSpecificCoin(self,coin_id,year,mintmark):
        results = Queries.addSpecificCoin(coin_id,year,mintmark)
        return self.update(*results)

    def addPurchase(self,kwargs):
        results = Queries.addPurchase(**kwargs)
        return self.update(*results)

    def fetchCoinById(self,coin_id):
        results = Queries.coinById(coin_id)
        return self.fetch(results[0],results[1])

    def fetchPurchasesWithSpecificCoinId(self,specific_coin_id):
       return self.fetch(*Queries.purchasesWithSpecificCoinId(specific_coin_id)) 

    def deleteById(self,kwargs):
        return self.update(*Queries.deleteById(**kwargs))

    def fetchById(self,kwargs):
        return self.fetch(*Queries.selectById(**kwargs))
