#   Author: Josh Gillum              .
#   Date: 6 August 2025             ":"         __ __
#                                  __|___       \ V /
#                                .'      '.      | |
#                                |  O       \____/  |
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
#
#    This file stores the Queries class, which provides several different SQL
#    queries. This allows for easily updating queries if SQL changes or another
#    database is used.
#
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

class Queries:
    # Returns a search query for finding coins given some specifiers
    def __unpack(dictionary,key,default_value=None):
        try:
            return dictionary[key]
        except KeyError:
            return default_value
    def search(**kwargs):
        country = Queries.__unpack(kwargs,"country")
        denomination = Queries.__unpack(kwargs,"denomination")
        face_value = Queries.__unpack(kwargs,"face_value")
        face_value_name = Queries.__unpack(kwargs,"face_value_name")
        year = Queries.__unpack(kwargs,"year")
        debug = Queries.__unpack(kwargs,"debug")
        show_only_owned = Queries.__unpack(kwargs,"show_only_owned")
        show_only_not_owned = Queries.__unpack(kwargs,"show_only_not_owned")

        if show_only_owned and show_only_not_owned:
            show_only_owned = False
            show_only_not_owned = False
        select_columns = "coins.coin_id,coins.gross_weight,coins.fineness,coins.precious_metal_weight,coins.years,coins.metal,coins.name,face_values.value_id,face_values.value,face_values.name as value_name,denominations.denomination_id,denominations.name as denomination_name,countries.country_id,countries.name as country_name,tags.bullion"
        base_query = "from coins inner join face_values on coins.face_value_id = face_values.value_id inner join denominations on face_values.denomination_id = denominations.denomination_id inner join countries on denominations.country_id = countries.country_id inner join tags on denominations.tags = tags.tag_id"
        if show_only_owned:
            base_query = f"SELECT DISTINCT {select_columns} {base_query} right join purchases on purchases.coin_id = coins.coin_id"
        elif show_only_not_owned:
            base_query = f"SELECT * from (SELECT DISTINCT {select_columns},purchases.coin_id as filter {base_query} left join purchases on coins.coin_id = purchases.coin_id "
        else:
            base_query = f"SELECT {select_columns} {base_query}"
        found_first_specifier = False
        country_query = ""
        denomination_query = ""
        value_name_query = ""
        value_query = ""
        year_query = ""
        queries = [
            (country_query, country, "countries"),
            (denomination_query, denomination, "denominations"),
            (value_name_query, face_value_name, "face_values"),
        ]
        for i in range(len(queries)):
            item = queries[i]
            if item[1]:
                queries[i] = (
                    f"""(
                    {item[2]}.name like ? or
                    {item[2]}.alternative_name_1 like ? or
                    {item[2]}.alternative_name_2 like ? or
                    {item[2]}.alternative_name_3 like ? or
                    {item[2]}.alternative_name_4 like ? or
                    {item[2]}.alternative_name_5 like ?
                )
                """,
                    item[1],
                )
                if found_first_specifier:
                    queries[i] = (f"AND {queries[i][0]}", item[1])
                found_first_specifier = True

        # Adds specifier for actual value
        if face_value:
            queries.append((value_query, face_value, 1))
            queries[-1] = ("    face_values.value=?", queries[-1][1], queries[-1][2])
            if found_first_specifier:
                queries[-1] = (
                    f"\nAND\n  {queries[-1][0].strip()}",
                    queries[-1][1],
                    queries[-1][2],
                )
            found_first_specifier = True

        # Adds specifier for actual value
        if year:
            queries.append((year_query, f"%{year}%", 1))
            queries[-1] = ("    coins.years like ?", queries[-1][1], queries[-1][2])
            if found_first_specifier:
                queries[-1] = (
                    f"\nAND\n  {queries[-1][0].strip()}",
                    queries[-1][1],
                    queries[-1][2],
                )
            found_first_specifier = True

        return_query = base_query
        variables = []
        if (
            country is not None
            or denomination is not None
            or face_value is not None
            or year is not None
        ):
            return_query += " where "
            for item in queries:
                if item[0]:
                    return_query += item[0]
                    repetitions = 6
                    if len(item) == 3:
                        repetitions = item[2]
                    for _ in range(repetitions):
                        variables.append(item[1])

        if show_only_not_owned:
            return_query += ") as filter_by_owned where filter_by_owned.filter is null"
        return_query += ";"
        if debug:
            print("-----------------------------------")
            print(f"Query:\n{return_query}")
            print(f"Variables:\n{variables}")
            print("-----------------------------------")

        return (return_query, tuple(variables))
    
    def countryNames():
        return "SELECT name,alternative_name_1,alternative_name_2,alternative_name_3,alternative_name_4,alternative_name_5 from countries;"

    def metals():
        return "SELECT metal_id,name,price,price_date from metals;"

    def updateMetalPrice(metal_id,price,date):
        query = "UPDATE metals set price=?,price_date=? where metal_id=?"
        return (query,(price,date,metal_id))

    def purchases():
        return "select purchases.coin_id,purchases.unit_price,purchases.purchase_quantity,purchases.purchase_date,specific_coins.id,specific_coins.year,specific_coins.mintmark from purchases left join specific_coins on purchases.specific_coin=specific_coins.id"
