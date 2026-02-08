#   Author: Josh Gillum              .
#   Date: 7 February 2026           ":"         __ __
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

from .queries import Queries

class DB_Interface:
    def __init__(self,debug=False):
        self.conn = None
        self.cursor = None
        self.debug = debug

    def Connect(self,db_config,debug=None):
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

    def CloseConnection(self,debug=None):
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

    def Fetch(self,*args):
        """Submits a query to the database"""
        if self.cursor:
            try:
                self.cursor.execute(*args)
            except mariadb.Error as e:
                print(f"An error occured: {e}")
                sys.exit(1)
            return list(self.cursor)

    def Update(self,*args):
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

    def FetchPurchases(self):
        """Gets all of the defined searches"""
        return self.Fetch(Queries.Purchases())

    def FetchPurchasesByCoinId(self,coin_id,purchase_id=False,specific_coin_id=False):
        return self.Fetch(*Queries.PurchasesByCoinId(coin_id,purchase_id,specific_coin_id))

    def FetchCountryNames(self):
        """Gets all of the names of every country"""
        return self.Fetch(Queries.CountryNames())

    def FetchCountryId(self,country_name):
        """Returns the country id associated with the given country_name"""
        results = Queries.CountryId(country_name)
        return self.Fetch(results[0],results[1])

    def FetchCountryDisplayName(self,country_id):
        """Returns the display name associated with the given country_id"""
        results = Queries.CountryDisplayName(country_id)
        return self.Fetch(results[0],results[1])

    def FetchDenominationId(self,denomination_name):
        """Returns the denomination id associated with the given denomination_name"""
        results = Queries.DenominationId(denomination_name)
        return self.Fetch(results[0],results[1])

    def FetchDenominationDisplayName(self,denomination_id):
        """Returns the display name associated with the given denomination_id"""
        results = Queries.DenominationDisplayName(denomination_id)
        return self.Fetch(results[0],results[1])

    def FetchMetals(self):
        return self.Fetch(Queries.Metals())

    def FetchCoins(self,search_arguments):
        """search_arguments should be a dictionary for **kwargs of Queries.search()"""
        results = Queries.Search(**search_arguments)
        return self.Fetch(results[0],results[1])

    def UpdateMetalPrice(self,args):
        results = Queries.UpdateMetalPrice(*args)
        return self.Update(*results)

    def FetchSpecificCoin(self,coin_id,year,mintmark):
        results = Queries.SpecificCoin(coin_id,year,mintmark)
        return self.Fetch(results[0],results[1])

    def AddSpecificCoin(self,coin_id,year,mintmark):
        results = Queries.AddSpecificCoin(coin_id,year,mintmark)
        return self.Update(*results)

    def AddPurchase(self,kwargs):
        results = Queries.AddPurchase(**kwargs)
        return self.Update(*results)

    def FetchCoinById(self,coin_id):
        results = Queries.CoinById(coin_id)
        return self.Fetch(results[0],results[1])

    def FetchPurchasesWithSpecificCoinId(self,specific_coin_id):
       return self.Fetch(*Queries.PurchasesWithSpecificCoinId(specific_coin_id)) 

    def DeleteById(self,kwargs):
        return self.Update(*Queries.DeleteById(**kwargs))

    def FetchById(self,kwargs):
        return self.Fetch(*Queries.SelectById(**kwargs))
