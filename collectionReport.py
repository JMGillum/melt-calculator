from coinInfo import Coins
import data
from coinData import Purchase

tab = "    "
currency_symbol="$"




if __name__ == "__main__":
    Coins.price(data.silver_spot_price,data.gold_spot_price)
    Coins.linkPurchases()

    price_sum = 0.0
    purchase_count = 0
    price_delta = 0.0
    for coin in Coins.owned:
        coin = Coins.coins[coin]
        print(coin.data.print("%c %F %d [%y]... %a %m [Melt: %v Value: (%V)]"))
        temp_sum = 0.0
        temp_count = 0.0
        temp_delta = 0.0
        value = coin.data.value*coin.data.retention
        for node in coin.nodes:
            if isinstance(node,Purchase):
                print(f"  {node}")
                price_sum += (node.price * node.quantity)
                purchase_count += node.quantity
                price_delta += ((value - node.price)*node.quantity)
                temp_sum += (node.price * node.quantity)
                temp_count += node.quantity
                temp_delta += ((value - node.price)*node.quantity)
        if temp_count > 0:
            temp_total_value = value * temp_count
            temp_average = temp_sum / temp_count
            print(Coins.print_statistics(temp_sum,temp_count,value))

        print()

    if purchase_count > 0:
        print("~~~Totals:~~~")
        print(Coins.print_statistics(price_sum,purchase_count,(price_sum+price_delta)/purchase_count))
        
