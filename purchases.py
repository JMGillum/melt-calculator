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
