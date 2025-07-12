import collection
import data
import search
silver_spot_price = 36.00





# United States
united_states = data.coinsUnitedStates()

# France
france = data.coinsFrance()

# Mexico
mexico = data.coinsMexico()


data = collection.CoinCollection(countries=sorted([united_states,mexico,france],key=lambda country: country.name),name="Precious Metals")


data.tree.cascading_set_fancy(True)
interactive_mode = False

lines = []
if interactive_mode:
    results = search.performSearch(data,"France")
    if results is None or len(results) == 0:
        print("No results found")
    else:
        if not isinstance(results,list):
            results = [results]
        for item in results:
            if isinstance(item,collection.Country) or isinstance(item,collection.Denomination):
                item.tree.cascading_set_fancy(True)
                lines += item.tree.print()
            else:
                print(item)
else:
    lines = data.tree.print()

for line in lines:
    print(line)
