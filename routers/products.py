
from typing import List

from schemas.product import Product as Product_schema
from database.connection import get_db, Base, engine
from database.models import Product as Product_model

from fastapi import APIRouter, Path, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

router = APIRouter(tags=["product"])

Base.metadata.create_all(engine)

@router.get("/products", response_model=List[Product_schema])
async def read_products(offset: int = 0, limit: int = 25, db: Session = Depends(get_db)):
    products = db.query(Product_model).offset(offset).limit(limit).all()
    return products

@router.post("/products", response_model=Product_schema)
async def create_product(product: Product_schema, db: Session = Depends(get_db)):
    params = product.dict()
    new_product = Product_model(**params)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/products/{id}", response_model=Product_schema)
async def read_product(id : int = Path(gt = 0), db: Session = Depends(get_db)):
    product = db.query(Product_model).filter(Product_model.id == id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product