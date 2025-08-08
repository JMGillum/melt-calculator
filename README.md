# WEEKLY RELEASES EVERY FRIDAY


# Roadmap
See roadmap.md for the order that countries will be added. Lower tier countries are higher priority than higher tier countries.
## Melt Calculator

The melt calculator is a valuable resources for investing in or collecting coins made of precious metals. It provides an easy to use interface for searching for coins. Each coin has an associated melt/intrinsic value equal to:
    
    weight of coin * fineness of precious metal * spot price of precious metal

This script allows the user to store a personal collection of the defined coins. This is useful for price tracking and determining gain and loss on the coins.

There is a provided script for printing out statistics on the personal collection

# Installation

Clone the repository or download the source code.
Clone the tree repository (sub package)
    See https://git-scm.com/book/en/v2/Git-Tools-Submodules for information on submodules
Or download the tree repository source code and extract to tree directory

Install python
* Linux: `sudo apt install python3`
* Windows: `python`

    Note that you must install the mariadb and colorama packages. Colorama requires version >= 0.4.6, which requires python >= 3.11, so you might have to update python if your version is older
    Also note that linux users can use python 3.10 if they remove the line that imports colorama and the line that calls `just_fix_windows_console()`. Windows users can do the same, but this will remove color support for them.

Install mariadb
1. Install mariadb: https://mariadb.com/get-started-with-mariadb/
2. Create a user account (or use root)
3. Modify db_config in config.py
4. Run your flavor of db/merge (sh or bat)
5. Log into database and execute db/setup.sql (`\. ABSOLUTE_PATH_TO/db/setup.sql`)
Windows:
* Run `Commnd Prompt (MariaDB ...)` from start menu
* Run `mariadb -u root -p from this command prompt`

# Usage

Invoke the script by callling it from the command line. Either:
`python3 main.py` or `python main.py`

pass `--help` as a command line argument to get a list of supported arguments.

## Output

The basic output of the script is a four-level tree. The outer level has a branch for each country. Each of these has a branch for each currency type / denomination (ex: cents / dollars),
 each of those has a branch for each face value they came in, and finally each of those has a branch for each grouping of the coin.  
There is an optional fifth layer that represents a personal collection. Coins in the personal collection will appear as a child branch of the specific coin in the tree.

Running the script on its own is a bit overwhelming, as it reports every single coin in the database. That is where the output customization comes into play.

## Customization

The main script provides a number of command line flags and arguments for customizing the output and/or filtering results. Do note that all flags and arguments are case sensitive. The most basic arguments to know are:
* `-h` or `--help` - Prints out all of the supported arguments/flags
* `-S` or `--search_string` - Performs a search on the next argument (Enclose in quotes)
* `-C` or `--hide_collection` - Disables printing of the personal collection
* `-H` or `--hide_price` - Disables printing of the values of coins

The file `config.py` contains several variables that can be changed to further customize the output of the script. See the header comment in this file for more information.

## Prices

One of the main features of the output is the coin pricing (based on precious metal contents). In order to see accurate pricing, the value of the various precious metals must be kept up to date. There 
are two ways of doing this.
1. Use the various pricing flags (-s,-g,-p,-P,-r) along with the -u flag. The pricing flags on their own do not stick, and are only for that one execution of the script. The -u flag pushes these prices to the database
 in order to update it for the future.
2. Run updateMetalPrices.py, which will prompt you for the various metal prices. Any that you do not wish to update can be skipped. This method is a bit more out of the way, but it is more flexible as it lets you set the price as of date, which is used to determine if a price is stale. (Useful if you are using slightly old data)

Every coin has two values: 
1. Melt value - the value of the precious metal in the coin if it were melted down.
2. Sell value - the value that a buyer would generally pay for the coin. Default value is 97% of the melt value, but some coins are higher or lower.

The coins in the personal collection will be summarized on a per coin group basis, with gain/loss being reported using both the melt and sell values. In general, the melt value appears on the left and the sell value on the right.

## Tips

### Searching

* Most denominations have a defined singular and plural form. Thus, a search for "cent" and "cents" should yield the same results. In the case that the coin is not found, try using the plural if you used singular, or singular if you used plural.
* Searches can be very broad or very specific. There are four categories for a search:
  * country (ex: canada,germany)
  * denomination (ex: cent,franc)
  * face value (ex: 20, 100)
  * year (ex: 1866, 1903)
* SQL wild cards '%' and '_' represent 0 or more characters and 0 or 1 characters respectively. They can be used in searches for countries and denominations when used with the specific flags (--country and --denomination. Does not currently work for search strings)

At least one of these must be provided for a search to actually filter anything. Some example searches:

    "France" (Returns all coins minted by France)
    "Cents" (Returns all coins of the 'cent' denomination (regardless of country))
    "Germany 2" (All German coins of face value 2)
    "1898 German 10 Mark" (All 10 mark German coins from 1898)

# Troubleshooting
## Weird output

* Try setting `show_color` to `False` in config.py
* If that doesn't work, also try setting `tree_fancy_characters` to `False` in config.py

## Mariadb Errors
* An error occurred: Unknown database 'coin_data'
* * The database has not been created. Try running the db/setup.sql script in mariadb
* If mariadb is not running: Try `sudo systemctl status mariadb` (should say 'active (running)')


