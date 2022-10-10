import json


from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Column, VARCHAR, Integer
from typing import Optional, List


pwd_context = CryptContext(schemes=["bcrypt"])


class UserOutput(SQLModel):
    id: int
    username: str


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column("username", VARCHAR, unique=True, index=True))
    password_hash: str = ""

    def set_password(self, password):
        """Setting the passwords actually sets password_hash."""
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        """Verify given password by hashing and comparing to password_hash."""
        return pwd_context.verify(password, self.password_hash)


class CarInput(SQLModel):
    size: Optional[str]
    fuel: Optional[str] = "diesel"
    doors: Optional[int]
    transmission: Optional[str] = "manual"
    '''
    class Config:
        schema_extra = {
            "example": {
                "size": "m",
                "doors": 5,
                "transmission": "manual",
                "fuel": "hybrid"
            }
        }
        '''


class Car(CarInput, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)


class CarOutput(CarInput):
    id: int


def load_db() -> List[CarOutput]:
    with open("cars.json") as f:
        return [CarOutput.parse_obj(obj) for obj in json.load(f)]


def save_db(cars: List[CarInput]):
    with open("cars.json", "w") as f:
        json.dump([car.dict() for car in cars], f, indent=4)
