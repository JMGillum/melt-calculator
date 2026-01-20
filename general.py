from datetime import datetime

def strToNum(num):
    fail = False
    temp_num = 0
    try:  # Converts the temp_num from a string to either an int or float
        temp_num = int(num)
    except ValueError:
        try:
            temp_num = float(num)
        except ValueError:
            index = num.find("/")
            dash = num.find("-")
            if dash < 0:
                dash = num.find(" ")
            if index > 0:
                if dash > 0:
                    prefix = num[:dash]
                    numerator = num[dash + 1 : index]
                else:
                    prefix = 0
                    numerator = num[:index]
                try:
                    denominator = num[index + 1 :]
                    try:
                        numerator = int(numerator)
                        denominator = int(denominator)
                        prefix = int(prefix)
                        temp_num = round(
                            prefix + numerator / denominator, 2
                        )
                    except ValueError:
                        fail = True
                except IndexError:
                    fail = True
            else:
                fail = True
    return (fail,temp_num)


def getConfirmation(prompt):
    while True:
        response = input(f"{prompt} (y/n): ").lower()
        if response == 'y' or response == "yes":
            return True
        elif response == 'n' or response == "no":
            return False
        else:
            print("You must enter either 'y' or 'n'.")


def getDate():
    date_prompt = "Enter date as either: 'D.M.Y', 'M/D/Y', or 'Y-M-D': "
    tries = 0
    found_date = None
    response = None
    while tries == 0 or response or response is None:
        if tries == 0 or response is None:
            response = input(date_prompt)
        else:
            response = input(f'Press enter to accept {found_date.strftime("%d %B %Y")} or {date_prompt}')
        if tries <= 0 or response:
            tries += 1
            if response:
                values_dot = response.split(".")
                values_slash = response.split("/")
                values_dash = response.split("-")
                day = -1
                month = -1
                year = -1

                if len(values_dot) == 3:
                    day,month,year = values_dot
                elif len(values_slash) == 3:
                    month,day,year = values_slash
                elif len(values_dash) == 3:
                    year,month,day = values_dash

                try:
                    year = int(year)
                    if year < 100:
                        year += 2000
                    found_date = datetime(year,int(month),int(day))
                except TypeError:
                    print("All values must be numeric.")
                    response = None
                except ValueError as e:
                    print(f"Values are outside of the acceptable range. {e}")
                    response = None
                # Ensures date is within the range that can be sent to the database
    return found_date.strftime("%Y-%m-%d")


def selectEntry(entries):
    for i in range(len(entries)):
        if len(entries) > 1:
            print(f"{i+1}: {entries[i]}")
        else:
            print(f"{entries[i]}")
    entry_id = 0
    if len(entries) > 1: # Multiple results from search
        while True:
            try:
                entry_id = int(input("Enter number for entry to select it: "))
            except ValueError:
                print("Must be numeric.")
                continue
            if entry_id <= 0 or entry_id > len(entries):
                print("Value out of range")
                continue
            else:
                entry_id -= 1
                break
    return entry_id
