from typing import List

from schemas.employe import Employe as EmployeeSchema
from schemas.employe import EmployeCreate
from database.connection import get_db, Base, engine
from database.models import Employee as EmployeModel

from fastapi import APIRouter, Path, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

router = APIRouter(tags=["employee"])

Base.metadata.create_all(engine)


@router.post(
    "/employees", response_model=EmployeeSchema, status_code=status.HTTP_201_CREATED
)
async def create_product(employee: EmployeCreate, db: Session = Depends(get_db)):
    params = employee.dict()

    new_employee = EmployeModel(**params)
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


@router.get(
    "/employees", response_model=List[EmployeeSchema], status_code=status.HTTP_200_OK
)
async def read_employees(
    offset: int = 0, limit: int = 25, db: Session = Depends(get_db)
):
    employees = db.query(EmployeModel).offset(offset).limit(limit).all()
    return employees


@router.get(
    "/employees/{id}", response_model=EmployeeSchema, status_code=status.HTTP_200_OK
)
async def read_employee(id: int = Path(gt=0), db: Session = Depends(get_db)):
    employee = db.query(EmployeModel).get(id)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
        )
    return employee
