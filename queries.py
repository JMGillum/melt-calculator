#   Author: Josh Gillum              .
#   Date: 18 January 2026           ":"         __ __
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
        select_columns = "coins.coin_id,coins.gross_weight,coins.fineness,coins.precious_metal_weight,GROUP_CONCAT(year SEPARATOR ', ') AS combined_years,coins.metal,coins.name,face_values.value_id,face_values.value,face_values.display_name as value_name,denominations.denomination_id,denominations.display_name as denomination_name,countries.country_id,countries.display_name as country_name,tags.bullion"
        base_query = "from coins inner join years on coins.coin_id = years.coin_id inner join face_values on coins.face_value_id = face_values.value_id inner join denominations on face_values.denomination_id = denominations.denomination_id inner join countries on denominations.country_id = countries.country_id inner join tags on denominations.tags = tags.tag_id"
        if country:
            base_query = f"{base_query} inner join country_names on countries.country_id = country_names.country_id"
        if denomination:
            base_query = f"{base_query} inner join denomination_names on denominations.denomination_id = denomination_names.denomination_id"
        if face_value_name:
            base_query = f"{base_query} inner join face_values_names on face_values.value_id = face_values_names.value_id"
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
            (country_query, country, "country_names"),
            (denomination_query, denomination, "denomination_names"),
            (value_name_query, face_value_name, "face_values_names"),
        ]
        for i in range(len(queries)):
            item = queries[i]
            if item[1]:
                queries[i] = (
                    f"{item[2]}.name like ?", item[1], 1
                )
                if found_first_specifier:
                    queries[i] = (f"AND {queries[i][0]}", item[1],1)
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


        return_query = base_query
        variables = []
        if found_first_specifier:
            return_query += " where "
            for item in queries:
                if item[0]:
                    return_query += item[0]
                    repetitions = 6
                    if len(item) == 3:
                        repetitions = item[2]
                    for _ in range(repetitions):
                        variables.append(item[1])
        return_query += " GROUP BY coin_id"
        if year:
            return_query += " HAVING combined_years like ?"
            variables.append(f"%{year}%")

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
        return "SELECT name,country_id from country_names;"

    def countryId(name):
        query = "SELECT country_id from country_names where name=?;"
        return (query,(name,))

    def countryDisplayName(country_id):
        query = "SELECT display_name from countries where country_id=?;"
        return (query,(country_id,))

    def denominationId(name):
        query = "SELECT denomination_id from denomination_names where name=?;"
        return (query,(name,))

    def denominationDisplayName(country_id):
        query = "SELECT display_name from denominations where denomination_id=?;"
        return (query,(country_id,))

    def metals():
        return "SELECT metal_id,name,price,price_date from metals;"

    def updateMetalPrice(metal_id,price,date):
        query = "UPDATE metals set price=?,price_date=? where metal_id=?"
        return (query,(price,date,metal_id))

    def purchases():
        return "SELECT purchases.coin_id,purchases.unit_price,purchases.purchase_quantity,purchases.purchase_date,specific_coins.id,specific_coins.year,specific_coins.mintmark FROM purchases LEFT JOIN specific_coins ON purchases.specific_coin=specific_coins.id;"

    def purchasesByCoinId(coin_id,purchase_id=False,specific_coin_id=False):
        query_purchase_id = ""
        if purchase_id:
            query_purchase_id = ",purchases.purchase_id"
        query_specific_coin_id = ""
        if specific_coin_id:
            query_specific_coin_id = ",specific_coins.id"
        return (f"select purchases.coin_id,purchases.unit_price,purchases.purchase_quantity,purchases.purchase_date,specific_coins.id,specific_coins.year,specific_coins.mintmark{query_purchase_id}{query_specific_coin_id} from purchases left join specific_coins on purchases.specific_coin=specific_coins.id where purchases.coin_id = ?",(coin_id,))

    def addPurchase(**kwargs):
        coin_id = Queries.__unpack(kwargs,"coin_id")
        purchase_date = Queries.__unpack(kwargs,"purchase_date")
        unit_price = Queries.__unpack(kwargs,"unit_price")
        quantity = Queries.__unpack(kwargs,"quantity")
        specific_coin_id = Queries.__unpack(kwargs,"specific_coin_id")


        columns = [x for x in [("coin_id",coin_id),("purchase_date",purchase_date),("unit_price",unit_price),("purchase_quantity",quantity),("specific_coin",specific_coin_id)] if x[1] is not None]
        column_names = [x[0] for x in columns]
        column_names = ",".join(column_names)
        column_placeholders = ["?" for x in columns]
        column_placeholders = ",".join(column_placeholders)

        columns = [x[1] for x in columns]

        if not coin_id or not purchase_date or not unit_price:
            return ""
        purchase_date = str(purchase_date)
        if not purchase_date[0] == '"':
            purchase_date = f'"{purchase_date}'
        if not purchase_date[-1] == '"':
            purchase_date = f'{purchase_date}"'
        base_query = f"INSERT INTO purchases({column_names}) VALUES({column_placeholders});"
        return (base_query,(columns))

    def specificCoin(coin_id,year=None,mintmark=None):
        base_query = "SELECT id,year,mintmark from specific_coins where coin_id = ?"
        year_query = " AND year = ?"
        mintmark_query = " AND mintmark = ?"
        query = base_query
        variables = None
        if year:
            query += year_query
            if mintmark:
                variables = (coin_id,year,mintmark)
                query += mintmark_query
            else:
                variables = (coin_id,year)
        else:
            if mintmark:
                variables = (coin_id,mintmark)
                query += mintmark_query
            else:
                variables = (coin_id,)
        return (f"{query};",variables)

    def addSpecificCoin(coin_id,year=None,mintmark=None):
        if not year and not mintmark:
            return ""
        variables = [coin_id]
        columns = ["coin_id"]
        if year is not None:
            variables.append(year)
            columns.append("year")
        if mintmark:
            variables.append(mintmark)
            columns.append("mintmark")

        question_marks = ",".join(["?" for x in variables])
        columns = ",".join(columns)
        base_query = f"INSERT INTO specific_coins({columns}) VALUES("
        return (f"{base_query}{question_marks});",tuple(variables))

    
    def coinById(coin_id):
        select_columns = "coins.coin_id,coins.gross_weight,coins.fineness,coins.precious_metal_weight,coins.years,coins.metal,coins.name,face_values.value_id,face_values.value,face_values.display_name as value_name,denominations.denomination_id,denominations.display_name as denomination_name,countries.country_id,countries.display_name as country_name,tags.bullion"
        base_query = "from coins inner join face_values on coins.face_value_id = face_values.value_id inner join denominations on face_values.denomination_id = denominations.denomination_id inner join countries on denominations.country_id = countries.country_id inner join tags on denominations.tags = tags.tag_id"
        return (f"Select {select_columns} {base_query} where coins.coin_id = ?;",(coin_id,))
        
    def purchasesWithSpecificCoinId(specific_coin_id):
        query = "SELECT purchase_id,coin_id,purchase_date,unit_price,purchase_quantity,specific_coin FROM purchases WHERE specific_coin = ?;"
        return (query,(specific_coin_id,))

    def deleteById(**kwargs):
        purchases = Queries.__unpack(kwargs,"purchases")
        specific_coins = Queries.__unpack(kwargs,"specific_coins")

        query = ""
        variables = []
        if purchases is not None:
            query += "DELETE from purchases where purchase_id = ?;"
            variables.append(purchases)

        if specific_coins is not None:
            query += "DELETE from specific_coins where id = ?;"
            variables.append(specific_coins)

        return (query,tuple(variables))

    def selectById(**kwargs):
        purchases = Queries.__unpack(kwargs,"purchases")
        specific_coins = Queries.__unpack(kwargs,"specific_coins")

        query = ""
        variables = []
        if purchases is not None:
            query += "SELECT purchase_id,coin_id,purchase_date,unit_price,purchase_quantity,specific_coin FROM purchases WHERE purchase_id = ?;"
            variables.append(purchases)

        if specific_coins is not None:
            query += "SELECT id,coin_id,year,mintmark FROM specific_coins WHERE id = ?;"
            variables.append(specific_coins)

        return (query,tuple(variables))




