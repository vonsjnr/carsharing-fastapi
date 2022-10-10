from typing import Optional

from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlmodel import Session, select

from db import get_session
from schemas import Car, CarInput, CarOutput, save_db, User
from routers.auth import get_current_user

router = APIRouter(prefix="/api/cars")


@router.get("/")
def get_cars(
        doors: Optional[int] = None, size: Optional[str] = None, transmission=None,
        session: Session = Depends(get_session)) -> list:
    query = select(Car)
    if size:
        query = query.where(Car.size == size)
    if doors:
        query = query.where(Car.doors == doors)
    return session.exec(query).all()


@router.get("/{id}")
def car_by_id(id: int = None):
    result = [car for car in db if car.id == id]
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail='No car with that id={}'.format(id))


@router.post("/", response_model=Car)
def add_car(
        car_input: CarInput,
        session: Session = Depends(get_session),
        user: User = Depends(get_current_user)) -> Car:
    new_car = Car.from_orm(car_input)
    session.add(new_car)
    session.commit()
    session.refresh(new_car)
    return new_car


@router.delete("/{id}", status_code=204)
def remove_car(id: int) -> None:
    matches = [car for car in db if car.id == id]
    if matches:
        car = matches[0]
        db.remove(car)
        save_db(db)
    else:
        raise HTTPException(status_code=404, detail="No car with id={}".format(id))


@router.put("/{id}", response_model=CarOutput)
def change_car(id: int, new_data: CarInput) -> CarOutput:
    matches = [car for car in db if car.id == id]
    if matches:
        car = matches[0]
        car.fuel = new_data.fuel
        car.transmission = new_data.transmission
        car.size = new_data.size
        car.doors = new_data.doors
        save_db(db)
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}")
