from pydantic import BaseModel, Field


class EmployeCreate(BaseModel):
    username: str = Field(min_length=1, max_length=50)


class Employe(EmployeCreate):
    id: int = Field(ge=1)

    class Config:
        orm_mode = True
