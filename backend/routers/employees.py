from typing import List

from schemas.employe import Employe as EmployeeSchema
from schemas.employe import EmployeCreate
from database.connection import get_db, Base, engine
from database.models import Employee as Employe_model

from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

router = APIRouter(tags=["employee"])

Base.metadata.create_all(engine)


@router.post(
    "/employees", response_model=EmployeeSchema, status_code=status.HTTP_201_CREATED
)
async def create_product(product: EmployeCreate, db: Session = Depends(get_db)):
    params = product.dict()

    new_employee = Employe_model(**params)
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee
