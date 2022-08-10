
import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer,\
    String, Float, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

from database.connection import Base

from schemas.orders import OrderStatusValues

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256))

    #orders = relationship("Order")

class Table(Base):
    __tablename__ = 'tables'
    id = Column(Integer, primary_key=True, index=True)

    #orders = relationship("Order")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    sku = Column(String)
    price = Column(Float)
    stock = Column(Integer)