import os
from pathlib import Path
import treasure.config

def ImmediateSubDirectories(path):
    return [f.name for f in os.scandir(path) if f.is_dir()]

def CheckOrdering(series,order):
    errors = 0
    for o in order:
        if o not in series:
            print(f"Error: Series ({o}) specified in order string was not found")
            errors += 1
    return errors

def SetupDB(db,path):
    files = ["setup.sql","countries.sql","denominations.sql","values.sql","coins.sql","coins_years.sql","purchases.sql"]
    for file in files:
        f = path / Path(file)
        print(f"Loading file: {f}")
        db.ExecuteScript(f, commit_on_success=True, rollback_on_failure=True, exit_on_failure=True)
        

def Start(db,args,config):
    errors = []
    path = Path(config["load_path"])
    series = ImmediateSubDirectories(path)

    order = None
    try:
        order = args["order"]
        if not order:
            order = None
        else:
            order = treasure.config.ParseSpecificationString(args["order"],allow_dict=False)

    # Key did not exist in args dictionary
    except KeyError:
        order = None

    # Likely that args["order"] was not of string type.
    except AttributeError:
        order = None

    # Raised by treasure.config.ParseSpecificationString when the string has errors
    except ValueError:
        errors.append("There is an error in your order string. See the manual for proper usage.")
        return 1,errors


    if order is None:
        errors.append("You must specify the order to load series. Pass the \'--help\' flag to learn how to use it.")
        return 1,errors

    if CheckOrdering(series,order) > 0:
        errors.append(f"Ensure that the series name in the order string was spelled correctly. If it was, check if a directory with the same name as the series exists at this path:\n{path}\nAlso ensure that this is the desired path. If it is not, update the config file or pass \'--help\' to this command to learn how to specify the path.")
        return 1,errors

    print("Series will be loaded in the following order:")
    for o in order:
        print(o)
        SetupDB(db, path / Path(o))


    return 0,errors
