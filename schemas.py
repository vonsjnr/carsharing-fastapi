import json

from pydantic import BaseModel
from typing import Optional, List


class CarInput(BaseModel):
    size: str
    fuel: Optional[str] = "diesel"
    doors: int
    transmission: Optional[str] = "manual"


class CarOutput(CarInput):
    id: int


def load_db() -> List[CarOutput]:
    with open("cars.json") as f:
        return [CarOutput.parse_obj(obj) for obj in json.load(f)]


def save_db(cars: List[CarInput]):
    with open("cars.json", "w") as f:
        json.dump([car.dict() for car in cars], f, indent=4)
