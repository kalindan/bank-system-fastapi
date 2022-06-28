from datetime import datetime
from .account_model import AccountBase
from .customer_model import CustomerBase
from .transaction_model import TransactionBase, TransactionType
   
class TransactionRead(TransactionBase):
    transaction_type: TransactionType
    date: datetime
    
class AccountRead(AccountBase):
    id: int
    balance: float
    transactions: list["TransactionRead"] = []
    
class CustomerRead(CustomerBase):
    id: int
    accounts: list["AccountRead"] = [] 