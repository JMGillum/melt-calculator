import config

from general import PrintDepth
import general

config_file_name = "config.py"

float_value_error = ("Error. Value for",f"in {config_file_name} must be a float value (number with optional decimal portion).")
bool_value_error = ("Error. Value for",f"in {config_file_name} must be a boolean value (True/False).")
int_value_error = ("Error. Value for",f"in {config_file_name} must be an integer value (whole number).")
str_value_error = ("Error. Value for",f"in {config_file_name} must be a string value (surrounded in quotes).")
dict_value_error = ("Error. Value for",f"in {config_file_name} must be a dictionary value (surrounded in curly brackets).")

missing_variable_error = ("Config file is missing",f"value. Add the following to {config_file_name} and modify the value if needed:\n")

config_options = {
    "default_retention":("float",0.97),
    "use_permille":("bool",False),
    "tree_fancy_characters":("bool",True),
    "currency_symbol":("str","$"),
    "current_year":("int","datetime.now().year"),
    "minimum_year":("int",1800),
    "date_format":("str","%m/%d/%y"),
    "bullion_hint":("str"," (Bullion)"),
    "show_color":("bool",True),
    "colors_8_bit":("bool",True),
    "show_metal_colors":("bool",True),
    "color_definitions":("dict:dict",{"metals","types","tags","others"}),
    "color_definitions:metals":("dict:str",{"ag":"silver","au":"bright_yellow","pd":"bronze","pt":"rose","rh":"lime","other":"red"}),
    "color_definitions:types":("dict:str",{"country":"blue","denomination":"purple","value":"yellow","purchase":"teal"}),
    "color_definitions:tags":("dict:str",{"bullion":"magenta"}),
    "color_definitions:other":("dict:str",{"gain":"green","loss":"red"}),
    "db_config":("dict:basic",{"host":("str","localhost"),"port":("int",3306),"user":("str","root"),"password":("None",None),"database":("str","coin_data")}),
    "enforce_prices_set":("bool",True),
}

config_options_comments = {
    "default_retention":["Default price retention value for every coin that does not","have it explicitly set. Default is 97% (0.97)"],
    "use_permille":"Set to True to use milessimal fineness (parts per 1000 instead of percent)",
    "tree_fancy_characters":["This dictates whether the tree uses less-supported characters in order","to improve visuals. Default is True if not set."],
    "current_year":"Current year",
    "minimum_year":"Earliest number that will be considered a year and not a face value",
    "show_color":"Toggles all colors on or off",
    "colors_8_bit":"Whether to use 8 bit colors instead of 3 bit colors",
    "show_metal_colors":"Whether coin metals will be colored",
    "color_definitions":"Different colors for things that are printed",
    "color_definitions:metals":"The colors of metals when printed. Key needs to be the index used in database for metal",
    "color_definitions:types":"The colors of item types",
    "color_definitions:tags":"The colors of tags",
    "color_definitions:other":"Other colors",
    "db_config":"Database connection parameters",
    "enforce_prices_set":"If True, the program will not run if the metal prices have not be set in the database"
}

config_options_header_comments = {
    "default_retention":"This is the value that is show when --hide_price is not set. It appears as the sell value. This is the percentage of the melt value that merchants will typically buy the coin at. Default is 97%.",
    "use_permille":"This is used to toggle between using percent or permille for the fineness of coins. Permille is parts per thousand, whereas percent is parts per thousand. A True value will use permille, while a False value will use percent. Ex: 900 permille = 90 percent, 835 permille = 83.5 percent.",
    "tree_fancy_characters":"By default, the tree output of the program uses characters that are not included in the basic ASCII mapping, and thus may not be supported by your terminal or system. Set this value to False to disable these characters and revert to basic characters in ASCII.",
    "currency_symbol":"This is the symbol that is placed before any prices displayed by the program.",
    "current_year":"Set this to the current year. Used in conjunction with minimum year to determine which numeric values are years as opposed to face values. Any numeric value between minimum_year and current_year is considerd a year, while any number outside of this range is considered a face value. This can be hardcoded (Ex: 2026), or can be the value datetime.now().year to automatically fetch it.",
    "minimum_year":"The minimum year used for the process described for current_year",
    "date_format":"This is a format string for how dates will be displayed. It is used mainly for purchases, as the years that a coin was minted is displayed differently. %m is replaced with the month, %d the day, and %y the year. Within this string can be any other characters, except for \'%\'. Ex: the date is 6 Feburary 2026 and date_format is \"%m:%d - %y\". The date would thus be displayed as 02:06 - 2026. Note that the month is displayed as a number, and not as the name of the month.",
    "bullion_hint":"The text displayed after any denomination that is tagged as bullion. It is placed immediately after the name of the denomination, so it is usually desirable to start the string with a space. Set to an empty string to not print anything. Note that there is also a configuration option to change the color of these denominations, so this extra hint may be redundant.",
    "show_color":"This enables or disables color printing in the terminal. Set to False if weird output is occuring, such as: \\0[033;5m...",
    "colors_8_bit":"This enables 8 bit color support. 8 bit colors allows for 256 different colors. Setting this to False reverts to 3 bit colors, which supports only 8 different colors. If show_color is set to False, this option will do nothing.",
    "show_metal_colors":"This toggles coloring for the names of metals. If this is True, the names of metals will be colored, using the colors defined below. Ex: Gold will use a gold color. Set to True to disable this coloring.",
    "color_definitions":"This dictionary defines which colors to use for various different aspects of the program. All colors must be defined in colors.py. See colors.py for the defined colors.",
    "color_definitions['metals']":"The colors used for metals. Below will be which metal the keys stand for.\n~ag: silver\n~au: gold\n~pd: palladium\n~pt: platinum\n~rh: rhodium\n~other: All other metals.",
    "color_definitions['types']":"The colors used for the different levels of the tree.\n~country: the country level of the tree. Ex: France\n~denomination: The denomination of the coin. Ex: Franc\n~value: The face value of the coin. Ex: 10\n~purchase: Any coin purchases.",
    "color_definitions['tags']":"The colors used for tags defined.\n~bullion: all denominations tagged as bullion.",
    "color_definitions['other']":"The colors used for miscellaneous other items.\n~gain: The price change between the purchase price of a coin and its current melt value is positive.\n~loss: The same as gain but the difference is negative.",
    "db_config":"This dictionary is all of the configuration needed to connect to the database. By default, this program uses mariadb, so you must specify the connection parameters.",
    "enforce_prices_set":"This specifies whether the program will allow you to continue without the prices of metals set in the database. By default, the program will terminate after it fetches from the database, metal prices that have not be set. Set to False to bypass this. Note that by default, metal prices are set to -1, so the melt values of coins will be displayed as negative."
}


def PrintConfigImports():
    print("from datetime import datetime")
    print()



def PrintComment(dictionary,key,depth=0,tab=None):
    """ Prints out lines of comments, at the specified tab level

    Args:
        comment (): A list of lines for comments. '# ' will be prepended to each line printed
        depth (): The number of tabs to place before the comment
        tab (): The characters to print for each tab. Pass None to use default of PrintDepth().
    """

    # Comments should be a list of strings. If not, places the single string into its own list
    try:
        general.PrintComment(dictionary[key],depth,tab)
    except KeyError:
        return


def CloseDictionary(depth,to_depth=1,tab=None):
    """ Prints '}' as needed to close nested dictionaries

    Args:
        depth (): The current depth
        to_depth (): The depth to close dictionaries to
        tab (): Characters to use as the tab for each depth

    Returns: to_depth
        
    """

    if depth > 0 and to_depth >= 0 and depth >= to_depth:
        while depth >= to_depth:
            depth -= 1
            if tab is not None:
                PrintDepth(depth,tab)
            else:
                PrintDepth(depth)
            print("}",end="")
            if to_depth > 1 and depth < to_depth:
                print(",")
            else:
                print()
        print()
    return to_depth


def IsBasicConfig(data_type):
    """ Determines whether to provided datatype is basic, so that it can be printed simply

    Args:
        data_type (): A string for the data type

    Returns:
        
    """
    if data_type == "basic" or data_type == "str" or data_type == "float" or data_type == "int" or data_type == "bool" or data_type == "None":
        return True
    else:
        return False

def PrintBasicConfig(key,data_type,value,depth=0,key_in_quotes=False,comma_at_end=False):
    if IsBasicConfig(data_type):
        if key_in_quotes:
            key = f'\"{key}\"'
        if data_type == "str":
            value = f'\"{value}\"'
        PrintDepth(depth)
        if comma_at_end:
            value = f"{value},"
        print(f"{key} = {value}")
        return True
    return False

def GetDepthAndLastItem(text):
    text_index = 0
    index = 0
    current_depth = 0
    while index > -1:
        current_depth += 1
        index = text.find(":",index)
        if index > -1:
            index += 1
            text_index = index
    return (current_depth,text[text_index:])


def PrintDefaultConfig():
    general.PrintHeaderWhale("Josh Gillum","5 Feburary 2026")
    option_comments = [("bullet" if key.find('[') < 0 else "bullet2",f"{key}: {value}") for key,value in config_options_header_comments.items()]
    general.PrintHeaderComments([("regular","This file contains basic configuration for the program. Below will be a summary of each item that can be configured.")]+option_comments)
    PrintConfigImports()
    keys = list(config_options.keys())
    depth = 0 # Stores how deep within nested dictionaries we are
    # Loops through every config option key
    for i in range(len(keys)):
        key = keys[i]
        value = config_options[key]
        data_type,value = value
        if data_type.startswith("dict"):

            # Decodes what the data type and name are
            current_depth,name = GetDepthAndLastItem(key)
            _, child_data_type = GetDepthAndLastItem(data_type)

            # Closes previous dictionaries (if needed)
            depth = CloseDictionary(depth,current_depth)

            # Prints comments for the variable, if any exist
            PrintComment(config_options_comments,key,current_depth-1)

            # Opens new dictionary
            PrintDepth(current_depth-1)

            # If nested, the name is a key in its parent dictionary, so its name must be in quotes
            if current_depth > 1:
                name = f'\"{name}\"'

            print(f"{name} =", "{")

            # Dictionary does not store nested dictionaries
            if not child_data_type == "dict":
                # Loops through each item of the dictionary
                for child_key,child_value in value.items():

                    # The data type and value for the child item
                    printable_data_type = child_data_type
                    printable_value = child_value
                    # Basic data type means that it is a mix of basic types
                    if child_data_type == "basic":
                        printable_data_type = child_value[0]
                        printable_value = child_value[1]
                    PrintBasicConfig(child_key,printable_data_type,printable_value,current_depth,key_in_quotes=True,comma_at_end=True)

            depth = current_depth
        # Any type other than dictionary
        else:
            depth = CloseDictionary(depth,1)
            depth = 0
            PrintComment(config_options_comments,key,depth)
            PrintBasicConfig(key,data_type,value)
        print()
    CloseDictionary(depth)


def PrintValueError(variable_name,variable_type):
    if variable_type == "float":
        print(float_value_error[0],f"\'{variable_name}\'",float_value_error[1])
    elif variable_type == "bool":
        print(bool_value_error[0],f"\'{variable_name}\'",bool_value_error[1])
    elif variable_type == "int":
        print(int_value_error[0],f"\'{variable_name}\'",int_value_error[1])
    elif variable_type == "str":
        print(str_value_error[0],f"\'{variable_name}\'",str_value_error[1])
    elif variable_type == "dict":
        print(dict_value_error[0],f"\'{variable_name}\'",dict_value_error[1])

def PrintAttributeError(variable_name,variable_default):
    print(missing_variable_error[0],f"\'{variable_name}\'",missing_variable_error[1],variable_default)

def PrintKeyError(variable_name,dictionary_name,message=""):
    print(f"The key \"{variable_name}\" is missing. Add it to the dictionary",f"\"{dictionary_name}\" in {config_file_name}.",message)

def CheckKeys(dictionary,dictionary_name,keys):
    num_errors = 0
    for key in keys:
        message = ""
        if isinstance(key,tuple):
            message = key[1]
            key = key[0]
        try:
            dictionary[key]
        except KeyError:
            if num_errors == 0:
                print("Keys are missing in",dictionary_name)
            num_errors += 1
            PrintKeyError(key,dictionary_name,message)
    return num_errors


def ValidateConfig():
    errors_count = 0
    # --- Default Retention --- 
    variable_name = "default_retention"
    variable_default = "default_retention = 0.97"
    try:
        if not isinstance(config.default_retention,(float,int)): # Incorrect type
            PrintValueError(variable_name,"float")
            print()
            errors_count += 1
    except AttributeError: # Variable is not defined
        PrintAttributeError(variable_name,variable_default)
        print()
        errors_count += 1

    # --- Tree Fancy Characters --- 
    variable_name = "tree_fancy_characters"
    variable_default = "tree_fancy_characters = True"
    try:
        if not isinstance(config.tree_fancy_characters,bool): # Incorrect type
            PrintValueError(variable_name,"bool")
            print()
            errors_count += 1
    except AttributeError: # Variable is not defined
        PrintAttributeError(variable_name,variable_default)
        print()
        errors_count += 1

    # --- Currency Symbol --- 
    variable_name = "currency_symbol"
    variable_default = "currency_symbol = \"$\""
    try:
        if not isinstance(config.currency_symbol,str): # Incorrect type
            PrintValueError(variable_name,"str")
            print()
            errors_count += 1
    except AttributeError: # Variable is not defined
        PrintAttributeError(variable_name,variable_default)
        print()
        errors_count += 1

    # --- Current Year --- 
    variable_name = "current_year"
    variable_default = "current_year = datetime.now().year # alternatively: current_year = xxxx & replace xxxx with year"
    try:
        if not isinstance(config.current_year,int): # Incorrect type
            PrintValueError(variable_name,"int")
            print()
            errors_count += 1
    except AttributeError: # Variable is not defined
        PrintAttributeError(variable_name,variable_default)
        print()
        errors_count += 1

    # --- Minimum Year --- 
    variable_name = "minimum_year"
    variable_default = "minimum_year = 1800"
    try:
        if not isinstance(config.minimum_year,int): # Incorrect type
            PrintValueError(variable_name,"int")
            print()
            errors_count += 1
    except AttributeError: # Variable is not defined
        PrintAttributeError(variable_name,variable_default)
        print()
        errors_count += 1

    # --- Date Format --- 
    variable_name = "date_format"
    variable_default = "date_format = %m/%d/%y"
    try:
        if not isinstance(config.date_format,str): # Incorrect type
            PrintValueError(variable_name,"int")
            errors_count += 1
            print()
        elif config.date_format.find("%d") < 0 or config.date_format.find("%m") < 0 or config.date_format.find("%y") < 0: 
            print(f"{variable_name} must contain the values %d, %m, and %y in it somewhere. These are placeholders for the day, month, and year of a date, respectively. Ex: \"%m/%d/%y\"")
            errors_count += 1
            print()
    except AttributeError: # Variable is not defined
        PrintAttributeError(variable_name,variable_default)
        print()
        errors_count += 1


    # --- Bullion Hint --- 
    variable_name = "bullion_hint"
    variable_default = "bullion_hint = \" (Bullion)\" # This is the text displayed after a denomination's name for all denominations tagged as bullion."
    try:
        if not isinstance(config.bullion_hint,str): # Incorrect type
            PrintValueError(variable_name,"str")
            print()
            errors_count += 1
    except AttributeError: # Variable is not defined
        PrintAttributeError(variable_name,variable_default)
        print()
        errors_count += 1

    # --- Show Color --- 
    variable_name = "show_color"
    variable_default = "show_color = True # Toggles all colors on or off"
    try:
        if not isinstance(config.show_color,bool): # Incorrect type
            PrintValueError(variable_name,"bool")
            print()
            errors_count += 1
    except AttributeError: # Variable is not defined
        PrintAttributeError(variable_name,variable_default)
        print()
        errors_count += 1

    # --- Colors 8 Bit --- 
    variable_name = "colors_8_bit"
    variable_default = "colors_8_bit = True # Whether to use 8 bit colors instead of 3 bit colors"
    try:
        if not isinstance(config.colors_8_bit,bool): # Incorrect type
            PrintValueError(variable_name,"bool")
            print()
            errors_count += 1
    except AttributeError: # Variable is not defined
        PrintAttributeError(variable_name,variable_default)
        print()
        errors_count += 1

    # --- Show Metal Colors --- 
    variable_name = "show_metal_colors"
    variable_default = "show_metal_colors = True # Whether coin metals will be colored"
    try:
        if not isinstance(config.show_metal_colors,bool): # Incorrect type
            PrintValueError(variable_name,"bool")
            print()
            errors_count += 1
    except AttributeError: # Variable is not defined
        PrintAttributeError(variable_name,variable_default)
        print()
        errors_count += 1

    # --- Color Definitions --- 
    variable_name = "color_definitions"
    variable_default = """
# Different colors for things that are printed
color_definitions = {
    # The colors of metals when printed. Key needs to be the index used in database for metal
    "metals":{ 
        "ag":"silver",
        "au":"bright_yellow",
        "pd":"bronze",
        "pt":"rose",
        "rh":"lime",
        "other":"red"
    },
    # The colors of item types
    "types" : {
        "country":"blue",
        "denomination":"purple",
        "value":"yellow",
        "purchase":"teal"
    },
    # The colors of tags
    "tags": {
        "bullion":"magenta"
    },
    # Other colors
    "other": {
        "gain":"green",
        "loss":"red"
    }
}
    """
    try:
        if not isinstance(config.color_definitions,dict): # Incorrect type
            PrintValueError(variable_name,"dict")
            print()
            errors_count += 1
        else: # Correct type. Check subdictionaries
            # ~~~ Metals subdictionary ~~~
            try:
                if not isinstance(config.color_definitions["metals"],dict): # Incorrect type
                    PrintValueError(variable_name,"dict")
                    print()
                    errors_count += 1
            except KeyError: # Variable is not defined
                PrintKeyError("metals",variable_name,"This dictionary may be empty, however it must exist. Keys should be the primary keys in metals table in database.")
                print()
                errors_count += 1

            # ~~~ Types subdictionary ~~~
            try:
                if not isinstance(config.color_definitions["types"],dict): # Incorrect type
                    PrintValueError(variable_name,"dict")
                    print()
                    errors_count += 1
                else:
                    num_errors = CheckKeys(config.color_definitions["types"],f"{variable_name}[\"types\"]",["country","denomination","value","purchase"])
                    if num_errors:
                        print()
                        errors_count += num_errors
            except KeyError: # Variable is not defined
                PrintKeyError("types",variable_name)
                print()
                errors_count += 1

            # ~~~ Tags subdictionary ~~~
            try:
                if not isinstance(config.color_definitions["tags"],dict): # Incorrect type
                    PrintValueError(variable_name,"dict")
                    print()
                    errors_count += 1
                else:
                    num_errors = CheckKeys(config.color_definitions["tags"],f"{variable_name}[\"tags\"]",["bullion"])
                    if num_errors:
                        print()
                        errors_count += num_errors
            except KeyError: # Variable is not defined
                PrintKeyError("tags",variable_name)
                print()
                errors_count += 1

            # ~~~ Other subdictionary ~~~
            try:
                if not isinstance(config.color_definitions["other"],dict): # Incorrect type
                    PrintValueError(variable_name,"dict")
                    print()
                    errors_count += 1
                else:
                    num_errors = CheckKeys(config.color_definitions["other"],f"{variable_name}[\"other\"]",["gain","loss"])
                    if num_errors:
                        print()
                        errors_count += num_errors
            except KeyError: # Variable is not defined
                PrintKeyError("other",variable_name)
                print()
                errors_count += 1

    except AttributeError: # Variable is not defined
        PrintAttributeError(variable_name,variable_default)
        print()
        errors_count += 1

    # --- DB Config --- 
    variable_name = "db_config"
    variable_default = """
# Database Connection Parameters
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": None,
    "database": "coin_data",
}
    """
    try:
        if not isinstance(config.db_config,dict): # Incorrect type
            PrintValueError(variable_name,"dict")
            print()
            errors_count += 1
        else:
            num_errors = CheckKeys(config.db_config,variable_name,["host","port","user",("password","It is best to set the value of this to None (no quotes). This will prompt you for the database password each time the program is run."),"database"])
            if num_errors:
                print()
                errors_count += num_errors
    except AttributeError: # Variable is not defined
        PrintAttributeError(variable_name,variable_default)
        print()
        errors_count += 1

    # --- Enforce Prices Set --- 
    variable_name = "enforce_prices_set"
    variable_default = "enforce_prices_set = True # If metal prices must be changed from default."
    try:
        if not isinstance(config.enforce_prices_set,bool): # Incorrect type
            PrintValueError(variable_name,"bool")
            print()
            errors_count += 1
    except AttributeError: # Variable is not defined
        PrintAttributeError(variable_name,variable_default)
        print()
        errors_count += 1


    return errors_count

if __name__ == "__main__":
    print("Errors:",ValidateConfig())
    PrintDefaultConfig()
