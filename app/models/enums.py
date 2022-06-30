import enum


class TransactionType(str, enum.Enum):
    WITHDRAWAL = "withdrawal"
    DEPOSIT = "deposit"
    TRANSFER = "transfer"
    NONE = "none"
