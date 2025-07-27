# WEEKLY RELEASES EVERY FRIDAY

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

# Usage

Invoke the script by callling it from the command line. Either:
`python3 main.py` or `python main.py`

pass `--help` as a command line argument to get a list of supported arguments.

If you would like to add your own coin data, see README.md in the coins directory

See purchases.py if you would like to add your own personal collection data
    collectionReport.py can be run to provide a report on your collection.

## Customization

The main script provides a number of command line flags and arguments for customizing the output and/or filtering results. Do note that all flags and arguments are case sensitive. The most basic arguments to know are:
* `-h` or `--help` - Prints out all of the supported arguments/flags
* `-S` or `--search_string` - Performs a search on the next argument (Enclose in quotes)
* `-C` or `--hide_collection` - Disables printing of the personal collection
* `-H` or `--hide_price` - Disables printing of the values of coins

The file `config.py` contains several variables that can be changed to further customize the output of the script. See the header comment in this file for more information.

## Tips

### Searching

* Most denominations have a defined singular and plural form. Thus, a search for "cent" and "cents" should yield the same results. In the case that the coin is not found, try using the plural if you used singular, or singular if you used plural.
* Searches can be very broad or very specific. There are four categories for a search:
* * country (ex: canada,germany)
* * denomination (ex: cent,franc)
* * face value (ex: 20, 100)
* * year (ex: 1866, 1903)

At least one of these must be provided for a search to actually filter anything. Some example searches:

    "France" (Returns all coins minted by France)
    "Cents" (Returns all coins of the 'cent' denomination (regardless of country))
    "Germany 2" (All German coins of face value 2)
    "1898 German 10 Mark" (All 10 mark German coins from 1898)

# Troubleshooting
## Weird output

* Try setting `show_color` to `False` in config.py
* If that doesn't work, also try setting `tree_fancy_characters` to `False` in config.py
