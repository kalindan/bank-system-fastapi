from pydantic import BaseModel

class Limits(BaseModel):
    daily_limit: float
    num_of_withdrawals: int
