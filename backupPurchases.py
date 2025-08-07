from db_interface import DB_Interface
import config
from queries import Queries

def convertSQL(query,values):
    for item in values:
        query = query.replace("?",f'"{item}"',1)
    return query

if __name__ == "__main__":
    try:
        db = DB_Interface()
        db.connect(config.db_config)
        specific_coins = {}
        purchases = db.fetchPurchases()
        current_specific_coin_id = 1
        purchases = sorted(purchases,key= lambda purchase: purchase[3])
        purchase_queries = []
        specific_coin_queries = []
        for purchase in purchases:
            purchase_args = {"coin_id": purchase[0],"purchase_date":purchase[3],"unit_price":purchase[1],"quantity":purchase[2]}
            if purchase[4] is not None:
                try:
                    specific_coins[purchase[4]]
                except KeyError:
                    specific_coins[purchase[4]] = (current_specific_coin_id,purchase[0],purchase[5],purchase[6])
                    current_specific_coin_id += 1
                purchase_args["specific_coin_id"] = specific_coins[purchase[4]][0]
            purchase_queries.append(Queries.addPurchase(**purchase_args))
        for key in specific_coins.keys():
            _,coin_id,year,mintmark = specific_coins[key]
            specific_coin_queries.append(Queries.addSpecificCoin(coin_id,year,mintmark))
        print("--Specific coins")
        for item in specific_coin_queries:
            print(convertSQL(*item))
        print()
        print("--Purchases")
        for item in purchase_queries:
            print(convertSQL(*item))

    finally:
        db.closeConnection()
