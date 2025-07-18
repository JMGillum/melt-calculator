from coinInfo import Coins
from metals import Metals
from tree.node import Node

tab = "    "

def print_reverse_build():
    coins_reverse_build = [f"{tab}coins_reverse_build ="+" {"]
    values_reverse_build = [f"{tab}values_reverse_build ="+" {"]
    denominations_reverse_build = [f"{tab}denominations_reverse_build ="+" {"]
    for country in Coins.countries:
        for denomination in Coins.countries[country]:
            denominations_reverse_build += [f"{tab}{tab}\"{denomination}\": (\"{country}\"),"]
            for value in Coins.denominations[denomination]:
                values_reverse_build += [f"{tab}{tab}\"{value}\": (\"{denomination}\",\"{country}\"),"]
                for coin in Coins.values[value]:
                    coins_reverse_build += [f"{tab}{tab}\"{coin}\": (\"{value}\",\"{denomination}\",\"{country}\"),"]
    coins_reverse_build += [f"{tab}"+"}"]
    values_reverse_build += [f"{tab}"+"}"]
    denominations_reverse_build += [f"{tab}"+"}"]

    for item in [coins_reverse_build,values_reverse_build,denominations_reverse_build]:
        for line in item:
            print(line)
        print()


def print_metals():
    silver_coins = [f"{tab}silver_coins = ["]
    gold_coins = [f"{tab}gold_coins = ["]
    for country in Coins.countries:
        for denomination in Coins.countries[country]:
            for value in Coins.denominations[denomination]:
                for coin in Coins.values[value]:
                    test = Coins.coins[coin]
                    if isinstance(test,Node):
                        test = test.data
                    if test.metal == Metals.SILVER:
                        silver_coins.append(f"{tab}{tab}\"{coin}\",")
                    if test.metal == Metals.GOLD:
                        gold_coins.append(f"{tab}{tab}\"{coin}\",")
    silver_coins.append(f"{tab}]")
    gold_coins.append(f"{tab}]")
    for line in silver_coins:
        print(line)
    print()
    for line in gold_coins:
        print(line)
    print()



if __name__ == '__main__':
    print_reverse_build()
    print_metals()
