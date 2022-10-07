from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException

from schemas import load_db, save_db, CarInput, CarOutput

app = FastAPI()
db = load_db()


@app.get("/api/cars")
def get_cars(doors: Optional[int] = None, size: Optional[str] = None, transmission=None) -> list:
    result = db
    if size:
        result = [car for car in db if car.size == size]
    if doors:
        result = [car for car in db if car.doors == doors]
    if transmission:
        result = [car for car in db if car.transmission == transmission]

    return result


@app.get("/api/cars/{id}")
def car_by_id(id: int = None):
    result = [car for car in db if car.id == id]
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail='No car with that id={}'.format(id))


@app.post("/api/cars/")
def add_car(car: CarInput) -> CarOutput:
    new_car = CarOutput(size=car.size, doors=car.doors,
                        fuel=car.fuel, transmission=car.transmission,
                        id=len(db)+1)
    db.append(new_car)
    save_db(db)
    return new_car


if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)
