import os
from pathlib import Path
import treasure.config
from treasure.filesystem import ImmediateSubDirectories, GenerateHash, CreateDirectories
from treasure.prompt import GetConfirmation
from treasure.text import CenterText
import db.sql.statement as sql_statements

def CheckOrdering(series,order):
    errors = 0
    for o in order:
        if o not in series:
            print(f"Error: Series ({o}) specified in order string was not found")
            errors += 1
    return errors

def LoadFile(db,path,filename):
    f = path / Path(filename)
    print(f"Loading file: {f}")
    db.ExecuteScript(f, commit_on_success=True, rollback_on_failure=True, exit_on_failure=True)

def SetupDB(db,path,sql_dir,hash_algorithm="sha1",force_regenerate=False):
    #files = ["setup.sql","countries.sql","denominations.sql","values.sql","coins.sql","coins_years.sql","purchases.sql"]
    prefixes = ["setup","metals","tags","countries","country_names","denominations","denomination_names","face_values","face_values_names","coins","years","specific_coins","purchases"]
    sql_path = path / Path("sql") / Path(sql_dir)
    if not sql_path.exists():
        CreateDirectories(sql_path)

    for prefix in prefixes:
        old_hash = None
        new_hash = None
        sql_file_path = sql_path / Path(f"{prefix}.sql")
        hash_file_path = sql_path / Path(f"{prefix}.{hash_algorithm}")
        csv_file_path = path / Path(f"{prefix}.csv")

        if not force_regenerate:
            # Check if generate sql file exists
            if sql_file_path.exists():

                # Check if hash file exists
                if hash_file_path.exists():
                    with hash_file_path.open("r") as f:
                        old_hash = f.readline()

        # Check if csv file exists in current dir
        if csv_file_path.exists():

            # Hash file for previous generation exists
            if old_hash is not None:
                new_hash = GenerateHash(csv_file_path,hash_algorithm)

            # If new sql file needs to be generated
            regenerate_sql = False

            # No sql file found
            if new_hash is None:
                print("No existing sql file found. Generating new sql file.")
                regenerate_sql = True

            # Hash mismatch, so file contents have likely changed
            elif old_hash != new_hash:
                print("The csv file appears to have been changed. Regenerating sql file.")
                regenerate_sql = True

            if regenerate_sql:
                db.LoadFromCSV(csv_file_path, sql_file_path, prefix)

                # Generate new hash and save it
                new_hash = GenerateHash(csv_file_path, hash_algorithm)
                with hash_file_path.open("w") as f:
                    f.write(new_hash)

        # Load file into database
        LoadFile(db,sql_path,f"{prefix}.sql")
        

def Start(db,args,config):
    errors = []
    path = Path(config["load_path"])
    if args["input_dir"]:
        path = Path(args["input_dir"])
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

    print(CenterText("DANGER"))
    print("Continuing will alter the database, perhaps irreperably. Please backup before continuing.")
    if not GetConfirmation("Continue"):
        return 1,["Aborting..."]

    LoadFile(db,path,"setup.sql")
    for o in order:
        print(CenterText(o))
        SetupDB(db, path / Path(o), sql_statements.name)


    return 0,errors
