from typing import List

from schemas.table import Table as TableSchema
from schemas.table import TableCreate
from database.connection import get_db, Base, engine
from database.models import Table as Table_model

from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

router = APIRouter(tags=["table"])

Base.metadata.create_all(engine)


@router.post("/tables", response_model=TableSchema, status_code=status.HTTP_201_CREATED)
async def create_product(product: TableCreate, db: Session = Depends(get_db)):
    params = product.dict()

    new_table = Table_model(**params)
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return new_table
