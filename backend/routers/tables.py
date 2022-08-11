from typing import List
from urllib import response

from schemas.table import Table as TableSchema
from schemas.table import TableCreate
from database.connection import get_db, Base, engine
from database.models import Table as TableModel

from fastapi import APIRouter, Path, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

router = APIRouter(tags=["table"])

Base.metadata.create_all(engine)


@router.post("/tables", response_model=TableSchema, status_code=status.HTTP_201_CREATED)
async def create_product(table: TableCreate, db: Session = Depends(get_db)):
    params = table.dict()

    new_table = TableModel(**params)
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return new_table


@router.get("/tables", response_model=List[TableSchema], status_code=status.HTTP_200_OK)
async def read_tables(offset: int = 0, limit: int = 25, db: Session = Depends(get_db)):
    tables = db.query(TableModel).offset(offset).limit(limit).all()
    return tables


@router.get("/tables/{id}", response_model=TableSchema, status_code=status.HTTP_200_OK)
async def read_table(id: int = Path(gt=0), db: Session = Depends(get_db)):
    table = db.query(TableModel).get(id)
    if table is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Table not found"
        )
    return table
