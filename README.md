# Melt Calculator

The melt calculator is a valuable resources for investing in or collecting coins made of precious metals. It provides an easy to use interface for searching for coins. Each coin has an associated melt/intrinsic value equal to:

``` text
weight of coin * fineness of precious metal * spot price of precious metal
```

This script allows the user to store a personal collection of the defined coins. This is useful for price tracking and determining gain and loss on the coins.

## Requirements

* Python >= 3.11
* Code is tested on Linux, but should work for Windows. No guarantees for Mac.

## Installation

1. Obtain a copy of the software. Do one of the following:
    * Follow the instructions for using git and [clone the repository](./docs/tutorials/UsingGit.md) (Preffered)
    * Download the source code and extract. You will need to do this for this repository, the database repository, the treasure repository, and the tree repository. Each of the repositories other than this main one must be extracted into their respective folders in this repository.
2. Install python
    * Linux (Debian based): `sudo apt install python3`
    * Windows: `python`
3. Navigate to the root project directory and install the required python packages by doing one of the following:
    * System-wide install (Not recommended)

        ``` SHELL
        pip install -r requirements.txt
        ```

    * Use venv:

        ``` SHELL
        python3 -m venv venv
        source ./venv/bin/activate
        pip install -r requirements.txt
        ```

    * Use anaconda

        ``` SHELL
        conda env create -f environment.yml
        ```

        > [!Note]
        > This will create an environment named `metals`. Edit the `environment.yml` file if you would like to change the name.

4. (Optional) Create alias to run program from anywhere:
    1. Edit `start.sh` by uncommenting the lines associated with your virtual environment. You will have to update the path to the project directory. Note that this must be an absolute path.
    2. Add the following to your shell configuration file (`~/.bashrc` for BASH, `~/.zshrc` for zsh, etc.):

        ``` SHELL
        alias metals='/absolute/path/to/project/start.sh'
        ```

        * `metals` You can replace metals with whatever you want the command to be.

5. Install mariadb

    1. Install mariadb via their [tutorial](https://mariadb.com/get-started-with-mariadb/)
    2. Create a user account (or use root)
    3. Follow instructions in the [database creation tutorial](./docs/tutorials/CreateDatabase.md)

6. Create the config file:

    ``` SHELL
    python3 check_config.py
    ```

    * This will create the config file, as well as print out its location.

7. Edit the config file (at least the database section)

8. Run the program:

    ``` SHELL
    python3 main.py --help
    ```

    * If you followed step 4 and created an alias, you can use `metals` in place of `python3 main.py`. You will have to restart your shell for this to take effect however (close and reopen terminal).

## Usage

Invoke the script by callling it from the command line. Either:
`python3 main.py` or `python main.py`

Pass `--help` as a command line argument to get a list of supported arguments.

## Output

The basic output of the script is a four-level tree. The outer level has a branch for each country. Each of these has a branch for each currency type / denomination (ex: cents / dollars), each of those has a branch for each face value they came in, and finally each of those has a branch for each grouping of the coin.  

There is an optional fifth layer that represents a personal collection. Coins in the personal collection will appear as a child branch of the specific coin in the tree.

Running the script on its own is a bit overwhelming, as it reports every single coin in the database. That is where the output customization comes into play.

## Customization

The main script provides a number of command line flags and arguments for customizing the output and/or filtering results. Do note that all flags and arguments are case sensitive. The most basic arguments to know are:

* `-h` or `--help` - Prints out all of the supported arguments/flags
* `-S` or `--search_string` - Performs a search on the next argument (Enclose in quotes)
* `-C` or `--hide_collection` - Disables printing of the personal collection
* `-H` or `--hide_price` - Disables printing of the values of coins

The config file contains several variables that can be changed to further customize the output of the script.

## Prices

One of the main features of the output is the coin pricing (based on precious metal contents). In order to see accurate pricing, the value of the various precious metals must be kept up to date. There are two ways of doing this.

1. Use the various pricing flags (-s,-g,-p,-P,-r) along with the -u flag. The pricing flags on their own do not stick, and are only for that one execution of the script. The -u flag pushes these prices to the database
 in order to update it for the future.
2. Execute `python3 main.py admin prices` to run through a script that will have you update metal prices. You can skip any metal by simply pressing enter when it prompts you for the price.

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

``` text
"France" (Returns all coins minted by France)
"Cents" (Returns all coins of the 'cent' denomination (regardless of country))
"Germany 2" (All German coins of face value 2)
"1898 German 10 Mark" (All 10 mark German coins from 1898)
```

## Troubleshooting

### Weird output

* If you see strings like "\033[0;5m] or similar, your terminal does not support the colors used by the program.
  * Try setting `show_color` to `false` in the config file.
* If the lines of the output tree looks like boxes, your terminal doesn't support the characters used.
  * Try setting `tree_fancy_characters` to `false` in the config file.

### Mariadb Errors

* `An error occurred: Unknown database 'coin_data'`
  * The database has not been created. Try running the db/setup.sql script in mariadb
* If mariadb is not running
  * Try `sudo systemctl status mariadb` (should say `'active (running)'`)

## Furthur Reading

For more information, check out the `docs` folder. It contains tutorials for common tasks with the program.

### Common tutorials

* [Updating the repository](./docs/tutorials/UsingGit.md)
* [Updating the database](./docs/tutorials/UpdateDatabase.md)
* [Backing up the database](./docs/tutorials/Backups.md)
* [Managing coin collection](./docs/tutorials/ManagingPurchases.md)
* [Updating metal prices](./docs/tutorials/Pricing.md)
* [Custom items](./docs/tutorials/AddingItems.md)
