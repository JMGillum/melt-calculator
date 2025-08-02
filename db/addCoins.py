import mariadb
import sys

db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "test",
    "database": "coin_data",
}
defined_countries = []
added_countries = []
added_denominations = []
added_values = []
added_coins = []
country_code = input("ISO 3 Alpha country code=").lower()
denomination_code = input("Denomination code=").lower()
value_code = input("Value code=").lower()
denomination_prefix = f"{country_code}"
value_prefix = f"{denomination_prefix}_{denomination_code}"
coin_prefix = f"{value_prefix}_{value_code}"


def addCountry(country_id):
    name = input(f"Country name for ({country_id}): ").lower()
    while True:
        alternative_names = []
        if not name:
            name = input("A name is required. Enter it here:")
            continue
        for i in range(5):
            response = input("Alternative name? (enter empty string to skip): ")
            if response:
                alternative_names.append(response.lower())
            else:
                break
        print(f"\n---Country Name: {name}---")
        for alternative_name in alternative_names:
            print(f"  {alternative_name}")
        
        response = input("Press enter to continue. Enter new name to re-enter names: ")
        if response:
            name = response
        else:
            break
    query_string = "INSERT INTO countries(country_id,name" 
    for i in range(len(alternative_names)):
        query_string += f",alternative_name_{i+1}"
    query_string += f') VALUES("{country_id}","{name}"'
    for i in range(len(alternative_names)):
        query_string += f',"{alternative_names[i]}"'
    query_string += ");"
    added_countries.append(query_string)


def addDenomination(prefix,code):
    print(f"Denomination id: {prefix}")
    name = input(f"Denomination name for ({prefix}_{code}): ").lower()
    while True:
        alternative_names = []
        if not name:
            name = input("A name is required. Enter it here:")
            continue
        for i in range(5):
            response = input("Alternative name? (enter empty string to skip): ")
            if response:
                alternative_names.append(response.lower())
            else:
                break
        print(f"\n---Denomination name: {name}---")
        for alternative_name in alternative_names:
            print(f"  {alternative_name}")
        
        response = input("Press enter to continue. Enter new name to re-enter names: ")
        if response:
            name = response
        else:
            break
    query_string = "INSERT INTO denominations(denomination_id,country_id,name" 
    for i in range(len(alternative_names)):
        query_string += f",alternative_name_{i+1}"
    query_string += f') VALUES("{prefix}_{code}","{prefix}","{name}"'
    for i in range(len(alternative_names)):
        query_string += f',"{alternative_names[i]}"'
    query_string += ");"
    added_denominations.append(query_string)

def addValue(prefix,code):
    print(f"Value id: {prefix}")
    while True:
        name = input(f"Value name for ({prefix}_{code}) (enter empty string to skip): ").lower()
        alternative_names = []
        if not name:
            break
        for i in range(5):
            response = input("Alternative name? (enter empty string to skip): ")
            if response:
                alternative_names.append(response.lower())
            else:
                break
        print(f"\n---Value name: {name}---")
        for alternative_name in alternative_names:
            print(f"  {alternative_name}")
        
        response = input("Press enter to continue. Enter any character to re-enter names: ")
        if not response:
            break
    query_string = "INSERT INTO face_values(value_id,denomination_id" 
    if name:
        query_string += ",name"
        for i in range(len(alternative_names)):
            query_string += f",alternative_name_{i+1}"
    query_string += f',value) VALUES("{prefix}_{code}","{prefix}"'
    if name:
        query_string += f',"{name}"'
        for i in range(len(alternative_names)):
            query_string += f',"{alternative_names[i]}"'
    query_string += f",{code}"
    query_string += ");"
    added_values.append(query_string)

def addCoin(prefix,code):
    print(f"Coin id: {prefix}_{code}")
    name = input(f"Coin name for ({prefix}_{code}) (enter empty string to skip): ").lower()
    while True:
        if name:
            print(f"\n---Coin name: {name}---")
            response = input("Press enter to continue. Enter name here to re-enter name: ")
        else:
            name = ""
            response = False
        if response:
            name = response
            continue
        else:
            break
    gross_weight = ""
    fineness = ""
    precious_metal_weight = ""
    while True:
        gross_weight = input("Enter gross weight (in grams):")
        fineness = input("Enter fineness (90% = 0.9):")
        try:
            gross_weight_usable = float(gross_weight)
            fineness_usable = float(fineness) # Ensures that user enters numeric value
            if fineness_usable > 1:
                while fineness_usable > 10:
                    fineness_usable = fineness_usable / 10
                fineness_usable = float(fineness_usable/10)
            precious_metal_weight = gross_weight_usable * fineness_usable * 0.03215075
            precious_metal_weight = round(precious_metal_weight,4)
            response = input(f"Is the calculated precious metal weight ({precious_metal_weight}) correct? (Press enter to continue. Enter it here (in troy ounces) to manually enter it.)")
            if response:
                precious_metal_weight = response
                float(precious_metal_weight)
            break
        except ValueError:
            print("All values must be numeric.")
            continue
    metal = input("Enter periodic symbol for metal (sil=ag,gol=au,plat=pt,pala=pd,rho=rh):")
    years = ""
    while True:
        years = input("Enter years (comma separated)(shorthand x-y is acceptable):")
        years_list = years.split(",")
        years = ""
        for item in years_list:
            try:
                int(item)
                years += f"{item}, "
            except ValueError:
                if "-" in item:
                    temp = item.find("-")
                    beginning = item[:temp]
                    end = item[temp+1:]
                    try:
                        beginning = int(beginning)
                        end = int(end)
                        for i in range(beginning,end+1):
                            years += f"{i}, "
                    except ValueError: # Two numbers were not actually numbers
                        print("All values must be numbers")
                        continue
                else:
                    print("Values must be individual years or of the form x-y (ex: 1898-1900)")
                    continue
        years = years[:-2] # Chops off trailing comma and space
        break

    query_string = "INSERT INTO coins(coin_id,face_value_id" 
    if name:
        query_string += ",name"
    query_string += ",gross_weight,fineness,precious_metal_weight,years,metal"
    query_string += f') VALUES("{prefix}_{code}","{prefix}"'
    if name:
        query_string += f',"{name}"'
    query_string += f',{gross_weight},{fineness},{precious_metal_weight},"{years}","{metal}"'
    query_string += ");"
    added_coins.append(query_string)

conn = None
cursor = None
try:
    # 2. Establish a Connection
    print("Connecting to MariaDB...")
    conn = mariadb.connect(**db_config)
    print("Connection successful!")

    # 3. Create a Cursor Object
    cursor = conn.cursor()


    # --- Example: Select Data ---
    print("\nSelecting data...")
    select_query = "SELECT coin_id FROM coins WHERE coin_id LIKE ?"
    cursor.execute(
        select_query, (f"{coin_prefix}%",)
    )  # Note the comma for single parameter tuple

    print("Fetched data:")
    temp = list(cursor)
    coin_number = 1
    if temp:
        coin_number = int(temp[-1][0].split("_")[-1]) # Gets count value at end of coin_id
        coin_number += 1
    else:
        print("No data found")
        print("\nSelecting data...")
        select_query = "SELECT value_id FROM face_values WHERE value_id LIKE ?"
        cursor.execute(
            select_query, (f"{value_prefix}%",)
        )  # Note the comma for single parameter tuple

        print("Fetched data:")
        temp = list(cursor)
        if not temp:
            print("No data found")
            print("\nSelecting data...")
            select_query = "SELECT denomination_id FROM denominations WHERE denomination_id LIKE ?"
            cursor.execute(
                select_query, (f"{denomination_prefix}%",)
            )  # Note the comma for single parameter tuple

            print("Fetched data:")
            temp = list(cursor)
            if not temp:
                print("No data found")
                print("\nSelecting data...")
                select_query = "SELECT country_id FROM countries WHERE country_id LIKE ?"
                cursor.execute(
                    select_query, (f"{country_code}",)
                )  # Note the comma for single parameter tuple

                print("Fetched data:")
                temp = list(cursor)
                if not temp:
                    addCountry(country_code)

            addDenomination(denomination_prefix,denomination_code)
        addValue(value_prefix,value_code)
    addCoin(coin_prefix,coin_number)


except mariadb.Error as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
finally:
    # 4. Close Cursor and Connection
    if cursor:
        cursor.close()
        print("Cursor closed.")
    if conn:
        conn.close()
        print("Connection closed.")

for item in [(added_countries,"Countries"),(added_denominations,"Denominations"),(added_values,"Values"),(added_coins,"Coins")]:
    if item[0]:
        print(f"-----{item[1]}-----")
        for query in item[0]:
            print(query)
