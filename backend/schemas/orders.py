from datetime import datetime
from enum import Enum

from typing import List
from pydantic import BaseModel, Field

from schemas.product import ProductName


class OrderStatusValues(str, Enum):
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"
    IN_PROCESS = "IN PROCESS"
    DELIVERED = "DELIVERED"
    COMPLETED = "COMPLETED"


class ProductOrdered(BaseModel):
    id: int = Field(alias="product_id")
    name: str = Field(alias="product_name")
    price: float = Field(alias="product_price")
    quantityOrdered: int = Field(gt=0)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


# Order Schema
class OrderBase(BaseModel):
    pass


class OrderCreate(OrderBase):
    employee: int = Field(ge=1)
    table: int = Field(ge=1)
    products: List[int] = Field(gt=0)


class Order(OrderBase):
    id: int = Field(gt=0, unique=True)
    status: OrderStatusValues
    employee: int = Field(ge=1)
    table: int = Field(ge=1)
    total: float = Field(gt=0)
    createdAt: datetime = Field(default=datetime.today())
    updatedAt: datetime = Field(default=datetime.today())
    products: List[ProductOrdered]

    class Config:
        orm_mode = True

class OrderUpdate(OrderBase):
    order_status: OrderStatusValues
    #updatedAt: datetime = Field(default=datetime.today())