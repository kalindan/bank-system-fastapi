import enum


class TransactionType(str, enum.Enum):
    WITHDRAWAL = "withdrawal"
    DEPOSIT = "deposit"
    TRANSFER = "transfer"
    NONE = "none"


class Messages(str, enum.Enum):
    ACCOUNT_CREATED = "Account successfully registered"
    ACCOUNT_LOADED = "Account successfully loaded"
    CUSTOMER_CREATED = "Customer successfully registered"
    CUSTOMER_LOADED = "Customer successfully loaded"
    CUSTOMER_AUTHENTICATED = "Customer authenticated"
