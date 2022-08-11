import datetime
from email.mime import base

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Float,
    Enum,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy

from database.connection import Base

from schemas.orders import OrderStatusValues


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), nullable=False, unique=True)


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    seats = Column(Integer, nullable=False)


class ProductOrdered(Base):
    __tablename__ = "products_ordered"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantityOrdered = Column(Integer, nullable=False)

    product = relationship("Product", cascade="all, delete")
    name = association_proxy("product", "name")
    price = association_proxy("product", "price")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    employee = Column(Integer, ForeignKey("employees.id"))
    table = Column(Integer, ForeignKey("tables.id"))
    status = Column(
        Enum(OrderStatusValues), default=OrderStatusValues.PENDING, nullable=False
    )
    createdAt = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updatedAt = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    products = relationship("ProductOrdered", cascade="all,delete")

    @hybrid_property
    def total(self):
        if self.products:
            return sum(
                [
                    ordered_products.product.price * ordered_products.quantityOrdered
                    for ordered_products in self.products
                ]
            )
        return 0


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sku = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
