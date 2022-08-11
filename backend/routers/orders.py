from datetime import datetime
from collections import Counter
from typing import List

from schemas.orders import Order as OrderSchema
from schemas.orders import OrderCreate, OrderStatusValues, OrderUpdate

from database.connection import get_db, Base, engine
from database.models import Order as OrderModel
from database.models import ProductOrdered as ProductOrderedModel
from database.models import Product as ProductModel
from fastapi import APIRouter, Path, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

router = APIRouter(tags=["order"])

Base.metadata.create_all(engine)


@router.get(
    "/orders",
    response_model=List[OrderSchema],
    response_model_by_alias=False,
)
async def read_orders(
    offset: int = 0,
    limit: int = 25,
    status: OrderStatusValues = OrderStatusValues.PENDING,
    db: Session = Depends(get_db),
):
    orders = (
        db.query(OrderModel)
        .filter(OrderModel.status == status)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return orders


@router.post(
    "/orders",
    response_model=OrderSchema,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED,
)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    out_stock = []

    cnt_products = Counter(order.products)
    for product_id in cnt_products.keys():
        product = db.query(ProductModel).get(product_id)
        if product.stock < cnt_products[product_id]:
            out_stock.append(product.name)
        else:
            product.stock -= cnt_products[product_id]
            db.add(product)
    
    if len(out_stock) != 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": "Order not created, products out stock",
                    "products": out_stock
                    }
        )

    new_order = OrderModel(table=order.table, employee=order.employee)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for product in cnt_products.keys():
        productsOrdered = ProductOrderedModel(
            product_id=product,
            order_id=new_order.id,
            quantityOrdered=cnt_products[product],
        )

        db.add(productsOrdered)

    db.commit()
    db.refresh(new_order)
    return new_order


@router.get("/orders/{id}", response_model=OrderSchema, response_model_by_alias=False)
async def read_order(id: int = Path(gt=0), db: Session = Depends(get_db)):
    order = db.query(OrderModel).get(id)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    return order

@router.delete("/orders/{id}", status_code=status.HTTP_200_OK)
async def delete_order(id: int = Path(gt=0), db: Session = Depends(get_db)):
    order = db.query(OrderModel).get(id)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    db.delete(order)
    db.commit()
    return {"detail": "Product deleted successfuly"}

@router.put("/orders/{id}", response_model=OrderSchema, response_model_by_alias=False, status_code=status.HTTP_200_OK)
async def update_order(order: OrderUpdate,  id: int = Path(gt=0), db: Session = Depends(get_db)):
    params = order.dict()
    order = db.query(OrderModel).get(id)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    order.status = params["order_status"]
    order.updatedAt = datetime.now()
    db.add(order)
    db.commit()
    db.refresh(order)
    return order