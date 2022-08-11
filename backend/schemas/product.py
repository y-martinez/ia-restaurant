from typing import Optional
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    price: float = Field(gt=0.0)
    stock: int = Field(ge=1)


class ProductCreate(ProductBase):
    sku: str = Field(unique=True, regex="^P-[A-Z0-9]{6}$")


class ProductUpdate(ProductBase):
    name: Optional[str] = Field(min_length=1, max_length=50)
    price: Optional[float] = Field(gt=0.0)
    stock: Optional[int] = Field(ge=1)


class Product(ProductCreate):
    id: int = Field(gt=0, unique=True)

    class Config:
        orm_mode = True


class ProductName(BaseModel):
    name: str = Field(min_length=1, max_length=50)

    class Config:
        orm_mode = True
