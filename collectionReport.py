from coinInfo import Coins
import data

tab = "    "
currency_symbol="$"

def print_colored(text,color,custom_color=""):
    test = color.lower().strip()
    default = "\033[39;49m"
    red = "\033[38:5:1m"
    blue = "\033[38:5:4m"
    green = "\033[38:5:2m"
    color_string = ""
    if custom_color:
        color_string = custom_color
    else:
        match test:
            case "r":
                color_string = red
            case "b":
                color_string = blue
            case "g":
                color_string = green
    return f"{color_string}{text}{default}"

def print_statistics(total:float,count:int,value:float):
    total = round(total,2)
    count = int(count)
    value = round(value,2)
    total_value = round(value*count,2)
    average = round(total/count,2)
    gain_loss = round(total_value-total,2)
    average_gain_loss = round(value-average,2)
    gain_loss_string = print_colored(f"+{currency_symbol}{gain_loss:.2f}","g") if gain_loss > 0 else print_colored(f"(-{currency_symbol}{-gain_loss:.2f})","r")
    average_gain_loss_string = print_colored(f"+{currency_symbol}{average_gain_loss:.2f}","g") if average_gain_loss > 0 else print_colored(f"(-{currency_symbol}{-average_gain_loss:.2f})","r")
    print(f"{tab}Sum: {currency_symbol}{total:.2f} ~ Avg: {currency_symbol}{average:.2f}",end="")
    print(f" ~ Value: {currency_symbol}{total_value:.2f}  ({currency_symbol}{value:.2f} * {count})",end="")
    print(f" ~ G/L: {gain_loss_string} ~ Avg G/L: {average_gain_loss_string}")


if __name__ == "__main__":
    Coins.linkPurchases()
    Coins.price(data.silver_spot_price,data.gold_spot_price)

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
            print(f"  {node}")
            price_sum += (node.price * node.quantity)
            purchase_count += node.quantity
            price_delta += ((value - node.price)*node.quantity)
            temp_sum += (node.price * node.quantity)
            temp_count += node.quantity
            temp_delta += ((value - node.price)*node.quantity)
        temp_total_value = value * temp_count
        temp_average = temp_sum / temp_count
        print_statistics(temp_sum,temp_count,value)

        print()

    print("~~~Totals:~~~")
    print_statistics(price_sum,purchase_count,(price_sum+price_delta)/purchase_count)
        
