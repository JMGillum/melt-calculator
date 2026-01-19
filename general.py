
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
