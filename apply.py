from coinInfo import coins
import coinInfo

for coin in coins:
    print(f"{coin}: CoinData()")




silver_coins = [
        "centimes_20",
        "centimes_50_1",
        "centimes_50_2",
        "franc_1_1",
        "franc_1_2",
        "franc_2",
        "franc_5_1",
        "franc_5_2",
        "franc_10_1",
        "franc_20_2",
        "franc_100_1",
        ]

gold_coins = [
        "franc_5_3",
        "franc_10_2",
        "franc_20_1",
        "franc_50",
        "franc_100_2",
        "franc_100_3",
        ]


france = coinInfo.buildCountry("france")
for line in france.print():
    print(line)
