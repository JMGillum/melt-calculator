import json
from db.sql.statement import Queries
from pathlib import Path

def Diff(db, database_1:str, database_2:str, data_load_path:str|None=None, input_file_path:str|None=None, excluded_tables:list=[], filter_by_series:list[str]|None=None, one_way:bool=False):

    data_file = Path(data_load_path) / Path("setup.json")
    if input_file_path:
        data_file = Path(input_file_path)
    
    with open(data_file, "r") as f:
        data = json.load(f)

    for table in data:
        table_name = table["name"]
        if table_name in excluded_tables:
            continue
        columns = [x["name"] for x in table["columns"]]
        s = Queries.Diff(table_name, columns, database_1, database_2)
        results_1 = db.Fetch(s)
        results_2 = None
        if not one_way:
            # Fetches differences the reverse way
            s = Queries.Diff(table_name, columns, database_2, database_1)
            results_2 = db.Fetch(s)

        yield (results_1, results_2, columns, table_name)

def PrintDiff(table_name, only_in_database_1, only_in_database_2, database_1, database_2):
    # Should be table_name, then two generators
    if only_in_database_1 or only_in_database_2:
        print(f"---------Table: {table_name}----------")
        if only_in_database_1:

            print(f"Present in {database_1} and not {database_2}")
            for line in only_in_database_1:
                print(f"> {line}")
        if only_in_database_2:

            print(f"Present in {database_2} and not {database_1}")
            for line in only_in_database_2:
                print(f"< {line}")


def __ExportDiffJSON(only_in_database_1, only_in_database_2, table_name, columns):
    additions = []
    removals = []
    for item in only_in_database_1:
        # Things being deleted
        removals.append({columns[i]: item[i] for i in range(len(columns))})
    for item in only_in_database_2:
        # Things being added
        additions.append({columns[i]: item[i] for i in range(len(columns))})

    changes = {}
    if additions:
        changes |= {"table": table_name, "insert": additions}
    if removals:
        changes |= {"table": table_name, "delete": additions}
    return changes



def ExportDiff(only_in_database_1, only_in_database_2, table_name, columns, export_format:str="json"):
    if export_format == "json":
        return __ExportDiffJSON(only_in_database_1, only_in_database_2, table_name, columns)

