from pathlib import Path
from treasure.filesystem import AllRegularFiles
import re

class VersionNumber:
    def __init__(self,major=None,moderate=None,minor=None,display_separator=".",string=None):
        if string is not None:
            values = VersionNumber.ParseVersionNumber(string)
            if values is not None:
                major, moderate, minor = values

        self.major = major
        self.moderate = moderate
        self.minor = minor
        self.display_separator = display_separator


    def ParseVersionNumber(string):
        try:
            string = str(string)
            string = string.strip()
            values = string.split(".")
            values_underscore = string.split("_")
            values_space = string.split(" ")

            if len(values_underscore) > len(values):
                values = values_underscore

            if len(values_space) > len(values):
                values = values_space


            if len(values) > 3:
                return None

            major = None
            moderate = None
            minor = None

            if len(values) > 2:
                minor = int(values[2])

            if len(values) > 1:
                moderate = int(values[1])

            if len(values) > 0:
                major = int(values[0])

            return (major,moderate,minor)
            

        except (AttributeError, ValueError):
            return None

    def ExpandedForm(self):
        if self.major is None:
            return None
        major = int(self.major)
        moderate = int(self.moderate) if self.moderate is not None else 0
        minor = int(self.minor) if self.minor is not None else 0

        return (major,moderate,minor)


    def __str__(self):
        s = ""
        if self.major is not None:
            s += f"{self.major}"
            if self.moderate is not None:
                s += f"{self.display_separator}{self.moderate}"
                if self.minor is not None:
                    s += f"{self.display_separator}{self.minor}"

        return s

    def compare(self,other):
        if isinstance(other,VersionNumber):
            this_expanded = self.ExpandedForm()
            other_expanded = other.ExpandedForm()
            return (this_expanded,other_expanded)

        elif isinstance(other,int):
            return (self,VersionNumber(other))

        elif isinstance(other,tuple) and len(other) > 0 and len(other) < 4:
            return (self,VersionNumber(*other))


    def __eq__(self,other):
        vals = self.compare(other)
        if vals is not None:
            return vals[0] == vals[1]

    def __ne__(self,other):
        vals = self.compare(other)
        if vals is not None:
            return vals[0] != vals[1]

    def __gt__(self,other):
        vals = self.compare(other)
        if vals is not None:
            return vals[0] > vals[1]

    def __ge__(self,other):
        vals = self.compare(other)
        if vals is not None:
            return vals[0] >= vals[1]

    def __lt__(self,other):
        vals = self.compare(other)
        if vals is not None:
            return vals[0] < vals[1]

    def __le__(self,other):
        vals = self.compare(other)
        if vals is not None:
            return vals[0] <= vals[1]


def __OptimalPathRecursive(sections,current,route):
    max_found = (current,route)
    for i in range(len(sections)):
        s = sections[i]
        if current == s[0]:
            end = __OptimalPathRecursive(sections[i:],s[1],route)

            # Prefer a route that ends with a larger value
            if end[0] > max_found[0]:
                max_found = end

            # Prefer a route that is shorter if it ends in the same place
            elif end[0] == max_found[0]:
                if len(end[1]) < len(max_found[1]):
                    max_found = end

        if current < s[0]:
            break

    return (max_found[0],[current]+max_found[1])


def OptimalPath(sections, start):
    sections = sorted(sections)
    max_val,route = __OptimalPathRecursive(sections,start,[])
    if max_val == start:
        return None
    else:
        return (max_val,route)


def Start(db, args, config):
    errors = []

    # Determines current database version
    current_version = db.DatabaseVersion()
    if len(current_version) != 1:
        return 1,["Unable to determine database version"]
    for entry in current_version:
        current_version = VersionNumber(entry[0],entry[1])
        break


    # Determines which path to use, the fetches all files here
    path = Path(config["update_path"])
    if args["input_dir"]:
        path = Path(args["input_dir"])

    end = None
    if args["end_version"]:
        end = args["end_version"]

    updates = AllRegularFiles(path)

    # Filters out files with names that do not match the pattern a_b_to_x_y.sql
    # This pattern indicates the update goes from version a.b to x.y
    update_routes=[]
    for entry in updates:
        i = re.findall(r"(\d+)_(\d+)_to_(\d+)_(\d+)\.sql",entry) 
        if i:
            i = i[0]
            if len(i) == 4:
                start = VersionNumber(i[0],i[1])
                end = VersionNumber(i[2],i[3])
                update_routes.append((start,end))
                print(f"{start} -> {end}")


    if not update_routes:
        return 1,[f"No suitable update files found. The path checked was:\n{path}"]


    # Determines which route to take
    print(f"Current version is {current_version}")
    result = OptimalPath(update_routes,current_version)
    if result is None:
        return (1,["No possible route"])
    else:
        print(f"Greatest possible version: {result[0]}")
        for i in range(len(result[1])):
            print(f"{result[1][i]}",end="")
            if i < len(result[1]) -1:
                print("->",end="")

        print()


    start_version = None
    for route in result[1]:
        if start_version is None:
            start_version = route
            continue
        print(f"Performing update: {start_version} -> {route}")
        filename = f"{start_version.major}_{start_version.moderate}_to_{route.major}_{route.moderate}.sql"
        f = path / Path(filename)
        db.ExecuteScript(f, commit_on_success=True, rollback_on_failure=True, exit_on_failure=True)
        start_version = route

    return 0,[]

