from typing import List

from schemas.product import Product as ProductSchema
from schemas.product import ProductCreate, ProductUpdate
from database.connection import get_db, Base, engine
from database.models import Product as ProductModel

from fastapi import APIRouter, Path, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

router = APIRouter(tags=["product"])

Base.metadata.create_all(engine)


@router.get("/products", response_model=List[ProductSchema])
async def read_products(
    offset: int = 0, limit: int = 25, db: Session = Depends(get_db)
):
    products = db.query(ProductModel).offset(offset).limit(limit).all()
    return products


@router.post(
    "/products", response_model=ProductSchema, status_code=status.HTTP_201_CREATED
)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    params = product.dict()
    product = db.query(ProductModel).filter(ProductModel.sku == params["sku"]).first()
    if product is not None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="SKU already on inventory",
        )

    new_product = ProductModel(**params)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get("/products/{id}", response_model=ProductSchema)
async def read_product(id: int = Path(gt=0), db: Session = Depends(get_db)):
    product = db.query(ProductModel).get(id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@router.delete("/products/{id}", status_code=status.HTTP_200_OK)
async def delete_product(id: int = Path(gt=0), db: Session = Depends(get_db)):
    product = db.query(ProductModel).get(id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    db.delete(product)
    db.commit()
    return {"detail": "Product deleted successfuly"}


@router.put(
    "/products/{id}", status_code=status.HTTP_200_OK, response_model=ProductSchema
)
async def update_product(
    product: ProductUpdate, id: int = Path(gt=0), db: Session = Depends(get_db)
):
    params = product.dict()
    product = db.query(ProductModel).get(id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    product.name = params["name"] if params["name"] else product.name
    product.price = params["price"] if params["price"] else product.price
    product.stock = params["stock"] if params["stock"] else product.stock

    db.commit()
    db.refresh(product)

    return product
