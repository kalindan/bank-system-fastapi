from pydantic import BaseModel, Field


class Limits(BaseModel):
    daily_limit: float = Field(gt=0)
    num_of_withdrawals: int = Field(gt=0)
