import json
from db.sql.statement import Queries
from pathlib import Path

def diff(db, database_1:str, database_2:str, args:dict, config:dict, excluded_tables:list=[], filter_by_series:list[str]|None=None, one_way:bool=False, enable_printing:bool=True, export_format:str|None=None):

    if export_format is not None:
        export_format = str(export_format).lower()
        if export_format not in ["json"]:
            raise ValueError
        

    data_file = Path(config["load_path"]) / Path("setup.json")
    if args.get("input_file",None):
        data_file = Path(args["input_file"])
    
    with open(data_file, "r") as f:
        data = json.load(f)

    if enable_printing:
        print(f"DIFF between {database_1} and {database_2}")
    for table in data:
        table_name = table["name"]
        if table_name in excluded_tables:
            continue
        columns = [x["name"] for x in table["columns"]]
        found_results = False
        s = Queries.Diff(table_name, columns, database_1, database_2)
        results = db.Fetch(s)
        if results:
            found_results = True
            if enable_printing:
                print(f"---------Table: {table_name}----------")
                print(f"Present in: {database_1} and not {database_2}")
            for line in results:
                if enable_printing:
                    print(line)

        if not one_way:
            # Fetches differences the reverse way
            s = Queries.Diff(table_name, columns, database_2, database_1)
            results = db.Fetch(s)
            if results:
                if not found_results:
                    found_results = True
                    if enable_printing:
                        print(f"---------Table: {table_name}----------")
                if enable_printing:
                    print(f"Present in: {database_2} and not {database_1}")
                for line in results:
                    if enable_printing:
                        print(line)


def PrintDiff(table_name, only_in_database_1, only_in_database_2):
    # Should be table_name, then two generators
    pass
    # diff() should be a generator that yields these tuples, one call does one table.

def export_changes(db, production_database:str, development_database:str, args:dict, config:dict, excluded_tables:list["str"]=["purchases","specific_coins"], filter_by_series:list[str]|None=None, export_format:str="json"):
    diff(db,production_database,development_database,args,config,excluded_tables=excluded_tables, filter_by_series=filter_by_series,one_way=False,enable_printing=False,export_format=export_format)


