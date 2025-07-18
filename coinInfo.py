from coinData import CoinData
from tree.tree import Tree
from tree.node import Node
from metals import Metals
from purchases import purchases

class NamedList:
    def __init__(self, name, items):
        self.name = name
        self.items = items

    def __str__(self):
        if self.name:
            return self.name
        else:
            return ""


    def __list__(self):
        if self.items:
            return self.items
        else:
            return ""


    def __getitem__(self, key):
        return self.items[key]


    def __setitem__(self, key, newvalue):
        self.items[key] = newvalue


class Coins:
    coins = {
        "centimes_20": Node(data= CoinData(
            years=list(range(1848, 1921)),
            weight=1,
            fineness=0.9,
            metal=Metals.SILVER,
            country="France",
            face_value=20,
            denomination="Centimes"
        )),
        "centimes_50_1": Node(data=CoinData(
            years=list(range(1848, 1867)),
            weight=2.5,
            fineness=0.9,
            metal=Metals.SILVER,
            country="France",
            face_value=50,
            denomination="Centimes"
        )),
        "centimes_50_2": Node(data=CoinData(
            years=list(range(1866, 1921)),
            weight=2.5,
            fineness=0.835,
            metal=Metals.SILVER,
            country="France",
            face_value=50,
            denomination="Centimes"
        )),
        "franc_1_1": Node(CoinData(
            years=list(range(1848, 1867)),
            weight=5,
            fineness=0.9,
            metal=Metals.SILVER,
            country="France",
            face_value=1,
            denomination="Franc"
        )),
        "franc_1_2": Node(CoinData(
            years=list(range(1866, 1921)),
            weight=5,
            fineness=0.835,
            metal=Metals.SILVER,
            country="France",
            face_value=1,
            denomination="Franc"
        )),
        "franc_2": Node(CoinData(
            years=list(range(1848, 1921)),
            weight=10,
            fineness=0.9,
            metal=Metals.SILVER,
            country="France",
            face_value=2,
            denomination="Franc"
        )),
        "franc_5_1": Node(CoinData(
            years=list(range(1848, 1921)),
            weight=25,
            fineness=0.9,
            metal=Metals.SILVER,
            country="France",
            face_value=5,
            denomination="Franc"
        )),
        "franc_5_2": Node(CoinData(
            years=list(range(1960, 1970)),
            weight=12,
            fineness=0.835,
            metal=Metals.SILVER,
            country="France",
            face_value=5,
            denomination="Franc"
        )),
        "franc_5_3": Node(CoinData(
            years=list(range(1848, 1915)),
            weight=1.6129,
            fineness=0.9,
            metal=Metals.GOLD,
            country="France",
            face_value=5,
            denomination="Franc"
        )),
        "franc_10_1": Node(CoinData(
            years=[x for x in list(range(1929, 1940)) if x not in [1935, 1936]],
            weight=10,
            fineness=0.68,
            metal=Metals.SILVER,
            country="France",
            face_value=10,
            denomination="Franc"
        )),
        "franc_10_2": Node(CoinData(
            years=list(range(1848, 1915)),
            weight=3.2258,
            fineness=0.90,
            metal=Metals.GOLD,
            country="France",
            face_value=10,
            denomination="Franc"
        )),
        "franc_20_1": Node(data=CoinData(
            years=[x for x in range(1906, 1915)],
            weight=6.4516,
            fineness=0.9,
            metal=Metals.GOLD,
            country="France",
            face_value=20,
            denomination="Franc"
        ),nodes=[]),
        "franc_20_2": Node(CoinData(
            years=list(range(1929, 1940)),
            weight=20,
            fineness=0.68,
            metal=Metals.SILVER,
            country="France",
            face_value=20,
            denomination="Franc"
        )),
        "franc_50": Node(CoinData(
            years=list(range(1848, 1915)),
            weight=16.129,
            fineness=0.9,
            metal=Metals.GOLD,
            country="France",
            face_value=20,
            denomination="Franc"
        )),
        "franc_100_1": Node(CoinData(
            years=[x for x in range(1982, 2001)],
            weight=15,
            fineness=0.9,
            metal=Metals.SILVER,
            country="France",
            face_value=100,
            denomination="Franc"
        )),
        "franc_100_2": Node(CoinData(
            years=list(range(1848, 1915)),
            weight=32.2581,
            fineness=0.9,
            metal=Metals.GOLD,
            country="France",
            face_value=100,
            denomination="Franc"
        )),
        "franc_100_3": Node(CoinData(
            years=list(range(1929, 1937)),
            weight=6.55,
            fineness=0.9,
            metal=Metals.GOLD,
            country="France",
            face_value=100,
            denomination="Franc"
        )),
    }

    # Used to build the tree from just a coin object
    coins_reverse_build = {
        "centimes_20": ("centimes_20","centimes","france"),
        "centimes_50_1": ("centimes_50","centimes","france"),
        "centimes_50_2": ("centimes_50","centimes","france"),
        "franc_1_1": ("franc_1","franc","france"),
        "franc_1_2": ("franc_1","franc","france"),
        "franc_2": ("franc_2","franc","france"),
        "franc_5_1": ("franc_5","franc","france"),
        "franc_5_2": ("franc_5","franc","france"),
        "franc_5_3": ("franc_5","franc","france"),
        "franc_10_1": ("franc_10","franc","france"),
        "franc_10_2": ("franc_10","franc","france"),
        "franc_20_1": ("franc_20","franc","france"),
        "franc_20_2": ("franc_20","franc","france"),
        "franc_50": ("franc_50","franc","france"),
        "franc_100_1": ("franc_100","franc","france"),
        "franc_100_2": ("franc_100","franc","france"),
        "franc_100_3": ("franc_100","franc","france"),
    }


    # Indicates which coins are made of silver
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

    # Indicates which coins are made of gold
    gold_coins = [
        "franc_5_3",
        "franc_10_2",
        "franc_20_1",
        "franc_50",
        "franc_100_2",
        "franc_100_3",
    ]

    values = {
        "centimes_20": NamedList("20", ["centimes_20"]),
        "centimes_50": NamedList("50", ["centimes_50_1", "centimes_50_2"]),
        "franc_1": NamedList("1", ["franc_1_1", "franc_1_2"]),
        "franc_2": NamedList("2", ["franc_2"]),
        "franc_5": NamedList("5", ["franc_5_1", "franc_5_2", "franc_5_3"]),
        "franc_10": NamedList("10", ["franc_10_1", "franc_10_2"]),
        "franc_20": NamedList("20", ["franc_20_1", "franc_20_2"]),
        "franc_50": NamedList("50", ["franc_50"]),
        "franc_100": NamedList("100", ["franc_100_1", "franc_100_2", "franc_100_3"]),
    }

    denominations = {
        "centimes": NamedList("Centimes", ["centimes_20", "centimes_50"]),
        "franc": NamedList(
            "Franc",
            [
                "franc_1",
                "franc_2",
                "franc_5",
                "franc_10",
                "franc_20",
                "franc_50",
                "franc_100",
            ],
        ),
    }

    countries = {
        "france": NamedList("France", ["centimes", "franc"]),
    }


    def linkPurchases():
        for purchase in purchases:
            try:
                coin = Coins.coins[purchase]
                coin.nodes += purchases[purchase]

            except KeyError:
                print(f"{purchase} is not a valid key")

    def buildCountry(country, first_time=True):
        """country is name, first_time will apply metals and country"""
        current_denominations = []
        for denomination in Coins.countries[country]:
            current_values = []
            for value in Coins.denominations[denomination]:
                current_coins = []
                for coin in Coins.values[value]:
                    temp = Coins.coins[coin]
                    if isinstance(temp,Node):
                        current_coins.append(temp)
                    else:
                        current_coins.append(Node(data=temp))
                # Sorts the coins by first year available
                current_coins = sorted(current_coins, key=lambda x: x.data.years[0])
                if isinstance(Coins.values[value], NamedList):
                    current_values.append(
                        Tree(name=str(Coins.values[value]), nodes=current_coins)
                    )
                else:
                    current_values.append(Tree(name=value, nodes=current_coins))
            if isinstance(Coins.denominations[denomination], NamedList):
                current_denominations.append(
                    Tree(name=str(Coins.denominations[denomination]), nodes=current_values)
                )
            else:
                current_denominations.append(Tree(name=denomination, nodes=current_values))
        return Tree(name=str(Coins.countries[country]), nodes=current_denominations)


    def buildTree(coin_ids,debug=False):
        results = Tree(name="Results",nodes=[])
        needed_countries = {}
        needed_denominations = {}
        needed_values = {}
        for coin_id in coin_ids:
            try:
                information = Coins.coins_reverse_build[coin_id]
                try:
                    value_found = needed_values[information[0]]
                    needed_values[information[0]] = (value_found + [coin_id])
                except KeyError: # coin_id's value is not a valid key in needed_values yet
                    needed_values[information[0]] = [coin_id]

                try:
                    denominations_found = needed_denominations[information[1]]
                    if not [x for x in denominations_found if x == information[0]]:
                        needed_denominations[information[1]] = (denominations_found + [information[0]])
                except KeyError: # coin_id's value is not a valid key in needed_values yet
                    needed_denominations[information[1]] = [information[0]]
                try:
                    countries_found = needed_countries[information[2]]
                    if not [x for x in countries_found if x == information[1]]:
                        needed_countries[information[2]] = (countries_found + [information[1]])
                except KeyError:
                    needed_countries[information[2]] = [information[1]]
            except KeyError: # coin_id is not a valid key in coins_reverse_build
                try:
                    information = Coins.values[coin_id]
                    coin_ids += list(information)
                except KeyError:
                    try:
                        information = Coins.denominations[coin_id]
                        coin_ids += list(information)
                    except KeyError:
                        try:
                            information = Coins.countries[coin_id]
                            coin_ids += list(information)
                        except KeyError:
                            pass
                        


            if debug:
                print(f"---{coin_id}---")
                print(f"Values: {needed_values}")
                print(f"Denominations: {needed_denominations}")
                print(f"Countries: {needed_countries}")
                print()

        current_countries = []
        for country in needed_countries:
            current_denominations = []
            for denomination in Coins.countries[country]:
                if denomination in needed_denominations:
                    current_values = []
                    for value in Coins.denominations[denomination]:
                        if value in needed_values:
                            current_coins = []
                            for coin in Coins.values[value]:
                                if coin in coin_ids:
                                    temp = Coins.coins[coin]
                                    if isinstance(temp,Node):
                                        current_coins.append(temp)
                                    else:
                                        current_coins.append(Node(data=temp))
                            # Sorts the coins by first year available
                            current_coins = sorted(current_coins, key=lambda x: x.data.years[0])
                            if isinstance(Coins.values[value], NamedList):
                                current_values.append(
                                    Tree(name=str(Coins.values[value]), nodes=current_coins)
                                )
                            else:
                                current_values.append(Tree(name=value, nodes=current_coins))
                    if isinstance(Coins.denominations[denomination], NamedList):
                        current_denominations.append(
                            Tree(name=str(Coins.denominations[denomination]), nodes=current_values)
                        )
                    else:
                        current_denominations.append(Tree(name=denomination, nodes=current_values))
            
            if isinstance(Coins.countries[country], NamedList):
                current_countries.append(
                    Tree(name=str(Coins.countries[country]), nodes=current_denominations)
                )
            else:
                current_countries.append(Tree(name=country, nodes=current_denominations))
        results = Tree(name="Results", nodes=current_countries)
        return results
            
    
    def search(country=None,denomination=None,face_value=None,year=None,debug=False):
        found_denominations = list(Coins.denominations.keys())
        if country is not None:
            try:
                found_denominations = Coins.countries[country.lower()]
            except KeyError:
                return None

        if debug:
            print("Denominations found:")
            for item in found_denominations:
                print(f"  {item}")

        found_values = []
        if denomination is not None:
            matches = [x for x in found_denominations if Coins.denominations[x].name.lower() == denomination.lower()]
            if matches:
                try:
                    found_values = Coins.denominations[matches[0]]
                except KeyError:
                    return None
            else:
                return None
        else:
            for denom in found_denominations:
                found_values += Coins.denominations[denom]

        if debug:
            print("Values found:")
            for item in found_values:
                print(f"  {item}")

        found_coins = []
        if face_value is not None:
            matches = [x for x in found_values if (Coins.values[x].name == face_value or str(Coins.values[x].name).lower() == str(face_value).lower())]
            if matches:
                try: 
                    found_coins = Coins.values[matches[0]]
                except KeyError:
                    return None
            else:
                return None
        else:
            for value in found_values:
                found_coins += Coins.values[value]

        
        if debug:
            print("Coins found:")
            for item in found_coins:
                print(f"  {item}")


        results = []
        if year is not None:
            matches = [x for x in found_coins if year in (Coins.coins[x].years if isinstance(Coins.coins[x],CoinData) else Coins.coins[x].data.years)]
            if matches:
                try:
                    results.append(matches[0])
                except KeyError:
                    return None
            else:
                return None
        else:
            results = found_coins

        if debug:
            print("Results:")
            for item in results:
                print(f"  {item}")

        return Coins.buildTree(results,debug)

