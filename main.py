import collection
import data
from data import silver_spot_price, gold_spot_price
import search
from metals import Metals

def price(data):
    if isinstance(data,collection.CoinCollection):
        data.price(silver_spot_price,gold_spot_price)


# United States
united_states = data.coinsUnitedStates()

# France
france = data.coinsFrance()

# Germany
germany = data.coinsGermany()

# Mexico
mexico = data.coinsMexico()

# Italy
italy = data.coinsItaly()

# Canada
canada = data.coinsCanada()


data = collection.CoinCollection(
    countries=sorted([canada,united_states, mexico, france, germany, italy], key=lambda country: country.name),
    name="Precious Metals",
)

price(data)

data.tree.cascading_set_fancy(True)
interactive_mode = False

lines = []
if interactive_mode:
    s = search.Search()
    results = s.performSearch(data, "France")
    # results = search.performSearch(data, "France")
    if results is None or len(results) == 0:
        print("No results found")
    else:
        if not isinstance(results, list):
            results = [results]
        for item in results:
            if isinstance(item, collection.Country) or isinstance(
                item, collection.Denomination
            ):
                item.tree.cascading_set_fancy(True)
                lines += item.tree.print()
            else:
                print(item)
else:
    lines = data.tree.print()

for line in lines:
    print(line)
