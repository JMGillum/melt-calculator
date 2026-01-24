import config

config_file_name = "config.py"

float_value_error = ("Error. Value for",f"in {config_file_name} must be a float value (number with optional decimal portion).")
bool_value_error = ("Error. Value for",f"in {config_file_name} must be a boolean value (True/False).")
int_value_error = ("Error. Value for",f"in {config_file_name} must be an integer value (whole number).")
str_value_error = ("Error. Value for",f"in {config_file_name} must be a string value (surrounded in quotes).")
dict_value_error = ("Error. Value for",f"in {config_file_name} must be a dictionary value (surrounded in curly brackets).")

missing_variable_error = ("Config file is missing",f"value. Add the following to {config_file_name} and modify the value if needed:\n")

def printValueError(variable_name,variable_type):
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

def printAttributeError(variable_name,variable_default):
    print(missing_variable_error[0],f"\'{variable_name}\'",missing_variable_error[1],variable_default)

def printKeyError(variable_name,dictionary_name,message=""):
    print(f"The key \"{variable_name}\" is missing. Add it to the dictionary",f"\"{dictionary_name}\" in {config_file_name}.",message)

def checkKeys(dictionary,dictionary_name,keys):
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
            printKeyError(key,dictionary_name,message)
    return num_errors


def validateConfig():
    errors_count = 0
    # --- Default Retention --- 
    variable_name = "default_retention"
    variable_default = "default_retention = 0.97"
    try:
        if not isinstance(config.default_retention,(float,int)): # Incorrect type
            printValueError(variable_name,"float")
            print()
            errors_count += 1
    except AttributeError: # Variable is not defined
        printAttributeError(variable_name,variable_default)
        print()
        errors_count += 1

    # --- Tree Fancy Characters --- 
    variable_name = "tree_fancy_characters"
    variable_default = "tree_fancy_characters = True"
    try:
        if not isinstance(config.tree_fancy_characters,bool): # Incorrect type
            printValueError(variable_name,"bool")
            print()
            errors_count += 1
    except AttributeError: # Variable is not defined
        printAttributeError(variable_name,variable_default)
        print()
        errors_count += 1

    # --- Currency Symbol --- 
    variable_name = "currency_symbol"
    variable_default = "currency_symbol = \"$\""
    try:
        if not isinstance(config.currency_symbol,str): # Incorrect type
            printValueError(variable_name,"str")
            print()
            errors_count += 1
    except AttributeError: # Variable is not defined
        printAttributeError(variable_name,variable_default)
        print()
        errors_count += 1

    # --- Current Year --- 
    variable_name = "current_year"
    variable_default = "current_year = datetime.now().year # alternatively: current_year = xxxx & replace xxxx with year"
    try:
        if not isinstance(config.current_year,int): # Incorrect type
            printValueError(variable_name,"int")
            print()
            errors_count += 1
    except AttributeError: # Variable is not defined
        printAttributeError(variable_name,variable_default)
        print()
        errors_count += 1

    # --- Minimum Year --- 
    variable_name = "minimum_year"
    variable_default = "minimum_year = 1800"
    try:
        if not isinstance(config.minimum_year,int): # Incorrect type
            printValueError(variable_name,"int")
            print()
            errors_count += 1
    except AttributeError: # Variable is not defined
        printAttributeError(variable_name,variable_default)
        print()
        errors_count += 1

    # --- Date Format --- 
    variable_name = "date_format"
    variable_default = "date_format = %m/%d/%y"
    try:
        if not isinstance(config.date_format,str): # Incorrect type
            printValueError(variable_name,"int")
            errors_count += 1
            print()
        elif config.date_format.find("%d") < 0 or config.date_format.find("%m") < 0 or config.date_format.find("%y") < 0: 
            print(f"{variable_name} must contain the values %d, %m, and %y in it somewhere. These are placeholders for the day, month, and year of a date, respectively. Ex: \"%m/%d/%y\"")
            errors_count += 1
            print()
    except AttributeError: # Variable is not defined
        printAttributeError(variable_name,variable_default)
        print()
        errors_count += 1


    # --- Bullion Hint --- 
    variable_name = "bullion_hint"
    variable_default = "bullion_hint = \" (Bullion)\" # This is the text displayed after a denomination's name for all denominations tagged as bullion."
    try:
        if not isinstance(config.bullion_hint,str): # Incorrect type
            printValueError(variable_name,"str")
            print()
            errors_count += 1
    except AttributeError: # Variable is not defined
        printAttributeError(variable_name,variable_default)
        print()
        errors_count += 1

    # --- Show Color --- 
    variable_name = "show_color"
    variable_default = "show_color = True # Toggles all colors on or off"
    try:
        if not isinstance(config.show_color,bool): # Incorrect type
            printValueError(variable_name,"bool")
            print()
            errors_count += 1
    except AttributeError: # Variable is not defined
        printAttributeError(variable_name,variable_default)
        print()
        errors_count += 1

    # --- Colors 8 Bit --- 
    variable_name = "colors_8_bit"
    variable_default = "colors_8_bit = True # Whether to use 8 bit colors instead of 3 bit colors"
    try:
        if not isinstance(config.colors_8_bit,bool): # Incorrect type
            printValueError(variable_name,"bool")
            print()
            errors_count += 1
    except AttributeError: # Variable is not defined
        printAttributeError(variable_name,variable_default)
        print()
        errors_count += 1

    # --- Show Metal Colors --- 
    variable_name = "show_metal_colors"
    variable_default = "show_metal_colors = True # Whether coin metals will be colored"
    try:
        if not isinstance(config.show_metal_colors,bool): # Incorrect type
            printValueError(variable_name,"bool")
            print()
            errors_count += 1
    except AttributeError: # Variable is not defined
        printAttributeError(variable_name,variable_default)
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
            printValueError(variable_name,"dict")
            print()
            errors_count += 1
        else: # Correct type. Check subdictionaries
            # ~~~ Metals subdictionary ~~~
            try:
                if not isinstance(config.color_definitions["metals"],dict): # Incorrect type
                    printValueError(variable_name,"dict")
                    print()
                    errors_count += 1
            except KeyError: # Variable is not defined
                printKeyError("metals",variable_name,"This dictionary may be empty, however it must exist. Keys should be the primary keys in metals table in database.")
                print()
                errors_count += 1

            # ~~~ Types subdictionary ~~~
            try:
                if not isinstance(config.color_definitions["types"],dict): # Incorrect type
                    printValueError(variable_name,"dict")
                    print()
                    errors_count += 1
                else:
                    num_errors = checkKeys(config.color_definitions["types"],f"{variable_name}[\"types\"]",["country","denomination","value","purchase"])
                    if num_errors:
                        print()
                        errors_count += num_errors
            except KeyError: # Variable is not defined
                printKeyError("types",variable_name)
                print()
                errors_count += 1

            # ~~~ Tags subdictionary ~~~
            try:
                if not isinstance(config.color_definitions["tags"],dict): # Incorrect type
                    printValueError(variable_name,"dict")
                    print()
                    errors_count += 1
                else:
                    num_errors = checkKeys(config.color_definitions["tags"],f"{variable_name}[\"tags\"]",["bullion"])
                    if num_errors:
                        print()
                        errors_count += num_errors
            except KeyError: # Variable is not defined
                printKeyError("tags",variable_name)
                print()
                errors_count += 1

            # ~~~ Other subdictionary ~~~
            try:
                if not isinstance(config.color_definitions["other"],dict): # Incorrect type
                    printValueError(variable_name,"dict")
                    print()
                    errors_count += 1
                else:
                    num_errors = checkKeys(config.color_definitions["other"],f"{variable_name}[\"other\"]",["gain","loss"])
                    if num_errors:
                        print()
                        errors_count += num_errors
            except KeyError: # Variable is not defined
                printKeyError("other",variable_name)
                print()
                errors_count += 1

    except AttributeError: # Variable is not defined
        printAttributeError(variable_name,variable_default)
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
            printValueError(variable_name,"dict")
            print()
            errors_count += 1
        else:
            num_errors = checkKeys(config.db_config,variable_name,["host","port","user",("password","It is best to set the value of this to None (no quotes). This will prompt you for the database password each time the program is run."),"database"])
            if num_errors:
                print()
                errors_count += num_errors
    except AttributeError: # Variable is not defined
        printAttributeError(variable_name,variable_default)
        print()
        errors_count += 1

    # --- Enforce Prices Set --- 
    variable_name = "enforce_prices_set"
    variable_default = "enforce_prices_set = True # If metal prices must be changed from default."
    try:
        if not isinstance(config.enforce_prices_set,bool): # Incorrect type
            printValueError(variable_name,"bool")
            print()
            errors_count += 1
    except AttributeError: # Variable is not defined
        printAttributeError(variable_name,variable_default)
        print()
        errors_count += 1


    return errors_count

if __name__ == "__main__":
    print("Errors:",validateConfig())
