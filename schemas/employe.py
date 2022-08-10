from pydantic import BaseModel, Field


class Employee(BaseModel):
    user_name: str = Field(min_length=1, max_length=50)
