from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Product(BaseModel):
    name : str = Field(min_length=1, max_length=50)
    sku : str = Field(min_length=1, max_length=50, unique=True)
    price : float = Field(gt = 0.0)
    stock : int = Field(gt = 1)

    class Config:
        orm_mode=True