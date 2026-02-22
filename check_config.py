from datetime import datetime
import treasure.config
from db.interface import DB_Interface

default_config_contents = """
# Config file for metals program
backup_path="/absolute/path/to/store/backups" # Where to store database backups

default_retention = 0.97 # Value of coin that a shop will pay. Is percentage of melt.

use_permille = false # Uses parts per thousand instead of parts per hundred (percent)

tree_fancy_characters = true

currency_symbol = "$" # displayed before prices

current_year = 2026
minimum_year = 1800 # Smallest value that will be interpreted as a year and not a face value.

date_format = "%m/%d/%y"

bullion_hint = " (Bullion)" # Displayed after bullion denominations

enforce_prices_set = false

# ----- Color related config -----
show_color = true # Toggles all color output
colors_8_bit = true # Toggles 8 bit colors on instead of 3 bit colors
show_metal_colors = true # Toggles colored names of metals

# Colors for names of metals. Does nothing if show_metal_colors is false.
# Each value on left is key used in database.
# Each value on right is a color defined in colors.py
[metals_colors]
ag="silver"
au="bright_yellow"
pd="bronze"
pt="rose"
rh="lime"
other="red"

[types_colors]
country="blue"
denomination="purple"
value="yellow"
purchase="teal"

[tags_colors]
bullion="magenta"

[misc_colors]
gain="green"
loss="red"

[db_config]
host="localhost"
port=3306
user="root"
database="coin_data"
# Uncomment password line below if you want to connect to database without
# having to enter your password each time. Be aware that it will be freely visible
# to other users of the system
#password="your_password"
"""

config_name = "config.toml"
config_dir = "metals"


def CheckFloat(item) -> bool:
    """ Returns whether the item is a float or an int

    Args:
        item (): The item to check

    Returns: True if item is int or float, False otherwise
        
    """
    
    return not isinstance(item, bool) and (
        isinstance(item, float) or isinstance(item, int)
    )


def CheckInt(item) -> bool:
    """ Returns whether the item is an int

    Args:
        item (): The item to check

    Returns: True if item is int, False otherwise.
        
    """
    
    return isinstance(item, int)


def CheckStr(item) -> bool:
    """ Returns whether the item is str

    Args:
        item (): The item to check

    Returns: True if item is str, False otherwise.
        
    """
    
    return isinstance(item, str)


def CheckBool(item) -> bool:
    """ Returns whether the item is bool

    Args:
        item (): The item to check

    Returns: True if item is bool, False otherwise.
        
    """

    return isinstance(item, bool)


def CheckValue(datatype:str, item) -> bool:
    """ Returns whether the item is of the specified datatype

    Args:
        datatype: A string of either "float", "int", "str", or "bool". What datatype the item is being compared to.
        item (): The item to check the datatype of

    Returns: True if item matches provided datatpye, False otherwise
        
    """

    datatype = datatype.lower()
    if datatype == "float":
        return CheckFloat(item)
    if datatype == "int":
        return CheckInt(item)
    if datatype == "str":
        return CheckStr(item)
    if datatype == "bool":
        return CheckBool(item)
    return False


def ValidateConfig() -> (dict,list[str]):
    """ Loads the config from the file, checks if the datatypes of the variables match what they are supposed to be.

    Returns: (dict object of config, list of strings describing errors)
        
    """
    errors = []  # A list of error strings. Allows this to function in non-terminal environments

    # Gets the config from the default location
    config = treasure.config.FetchConfig(config_name, config_dir)

    # Config was not found, create at default location
    if config is None:
        errors.append(
            f"Config file not found. Creating {config_name}: {treasure.config.DefaultConfigPath(config_dir)}"
        )

        # Creates config file with default contents.
        treasure.config.CreateConfig(default_config_contents, config_name, config_dir)
        return (None, errors)

    # Validate basic config options are of the correct datatypes
    # Each item is a tuple of (key,default value)

    # All variables that should be of float type
    float_keys = (("default_retention", 0.97),)

    # All variables that should be of int type
    int_keys = (("current_year", datetime.now().year), ("minimum_year", 1800))

    # All variables that should be of str type
    str_keys = (
        ("currency_symbol", "$"),
        ("date_format", "%m/%d/%y"),
        ("bullion_hint", " (Bullion)"),
        ("backup_path","~/backups/metals"),
    )

    # All variables that should be of bool type
    bool_keys = (
        ("use_permille", False),
        ("tree_fancy_characters", True),
        ("enforce_prices_set", True),
        ("show_color", True),
        ("colors_8_bit", True),
        ("show_metal_colors", True),
    )

    keys = {"float": float_keys, "int": int_keys, "str": str_keys, "bool": bool_keys}

    # Loops through each key, setting default value if not present in config file.
    for datatype, type_keys in keys.items():
        for key in type_keys:
            key, default = key

            # Fetches specific config item, or uses default if it is not found
            if treasure.config.ExtractConfigItem(config, key, default):

                # Config item is of the wrong datatype
                if not CheckValue(datatype, config[key]):
                    errors.append(f"Error: {key}")

    # Validate each of the color dictionaries
    dict_keys = (
        ("metals_colors", ("ag", "au", "pd", "pt", "rh", "other")),
        ("types_colors", ("country", "denomination", "value", "purchase")),
        ("tags_colors", ("bullion",)),
        ("misc_colors", ("gain", "loss")),
    )

    for key, sub_keys in dict_keys:

        # If config item is missing, use empty dictionary. This allows the user
        # to disable color output for specific items.
        if treasure.config.ExtractConfigItem(config, key, {}):

            # Checks each dict object
            if not isinstance(config[key], dict):
                errors.append(f"Error: {key}")
            else:

                # Loops through each sub key in the dictionary
                for sub_key in sub_keys:
                    if treasure.config.ExtractConfigItem(config[key], sub_key, ""):
                        if not isinstance(config[key][sub_key], str):
                            errors.append(f"Error: {key} {sub_key}")

    # Let db_interface class handle validating the db config
    treasure.config.ExtractConfigItem(config, "db_config", None)
    errors += DB_Interface.ValidateConfig(config["db_config"])

    return (config, errors)


if __name__ == "__main__":

    # Simply validates the config and prints out any errors
    print(f"Config location: {treasure.config.DefaultConfigPath('metals')}")
    _, errors = ValidateConfig()
    for error in errors:
        print(error)
