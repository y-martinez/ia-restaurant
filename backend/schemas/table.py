from pydantic import BaseModel, Field


class TableCreate(BaseModel):
    pass


class Table(TableCreate):
    id: int = Field(ge=1)

    class Config:
        orm_mode = True
