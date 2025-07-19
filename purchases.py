"""
   Author: Josh Gillum              .
   Date: 18 July 2025              ":"         __ __
                                  __|___       \ V /
                                .'      '.      | |
                                |  O       \____/  |
^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

    This file stores all the Purchase objects that represent the personal
    collection. Unfortunately, there is no system for doing this dynamically
    yet, so these must all be manually updated.

    purchases is a dictionary, and the keys represent the coin that the 
    purchase is for. The key here needs to exactly match the key in the Coins
    class. See coinInfo.py for more information. The value associated with the
    key must be a list of Purchase objects. See coinData.py for more information
    about Purchase objects.

    An example Purchase object would be:
        
        Purchase(price=33.90,purchase_date=datetime(2025,7,2))

    * Note that the values inside the datetime constructor are in the order:
        year,month,day.

    An example entry in the purchases dictionary would be:

        "canada_dollar_5": [
            Purchase(price=33.9, purchase_date=datetime(2025, 4, 18)),
            Purchase(price=37.95, purchase_date=datetime(2025, 6, 24)),
            Purchase(price=38.2, purchase_date=datetime(2025, 7, 8)),
        ],

    * This would correspond to the CoinData defined in Coins with the key
    "canada_dollar_5", which happens to be the silver maple leaf bullion

    More values, such as mint_date can be stored in a Purchase object, again
    see coinData.py for more information

^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
"""

from coinData import Purchase
from datetime import datetime


purchases = {
    # Canada
    "canada_dollar_5": [
        Purchase(price=33.9, purchase_date=datetime(2025, 4, 18)),
        Purchase(price=37.95, purchase_date=datetime(2025, 6, 24)),
        Purchase(price=38.2, purchase_date=datetime(2025, 7, 8)),
    ],
    # France
    "franc_10_1": [
        Purchase(price=8.00, mint_date=1931, purchase_date=datetime(2025, 7, 4))
    ],
    "franc_100_1": [
        Purchase(price=11.95, mint_date=1982, purchase_date=datetime(2025, 7, 3))
    ],
    # Germany
    "mark_10": [
        Purchase(
            price=373.98,
            purchase_date=datetime(2025, 7, 5),
            mint_date=1898,
            mint_mark="A",
        )
    ],
    # Italy
    # Mexico
    # United States
    "mercury_dime": [
        Purchase(price=2.56, purchase_date=datetime(2025, 7, 12), quantity=1)
    ],
    "roosevelt_dime": [
        Purchase(price=2.56, purchase_date=datetime(2025, 7, 12), quantity=48),
        Purchase(price=0.1, purchase_date=datetime(2025, 7, 12), quantity=1),
    ],
    "barber_quarter": [
        Purchase(price=6.43, purchase_date=datetime(2025, 7, 12), quantity=4)
    ],
    "standing_liberty_quarter": [
        Purchase(price=6.43, purchase_date=datetime(2025, 7, 12), quantity=4)
    ],
    "washington_quarter": [
        Purchase(price=2.56, purchase_date=datetime(2025, 7, 12), quantity=28)
    ],
    "walking_liberty_half": [
        Purchase(price=12.86, purchase_date=datetime(2025, 7, 12), quantity=9)
    ],
    "benjamin_half": [
        Purchase(price=12.86, purchase_date=datetime(2025, 7, 12), quantity=1)
    ],
}
