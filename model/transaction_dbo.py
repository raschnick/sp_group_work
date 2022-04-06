from datetime import datetime
from decimal import Decimal


class TransactionDbo:
    transaction_id: int
    transaction_date: datetime
    depot_id: int
    currency_id: int
    currency_rate: Decimal
    amount: Decimal
