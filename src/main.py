from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Car, Base, CarRating
from schemas import CarCreate, CarResponse, CarRatingCreate, CarResponseWithAvg
from sqlalchemy import func, desc
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/cars/", response_model=List[CarResponse])
def create_car(db: Session = Depends(get_db)):
    cars = db.query(Car).all()
    return cars


@app.post("/cars/", response_model=CarResponse)
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    db_car = Car(**car.model_dump())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


@app.post("/cars/{car_id}/rate")
def create_rating(
    car_id: int, car_rating: CarRatingCreate, db: Session = Depends(get_db)
):
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    db_rating = CarRating(**car_rating.model_dump(), car_id=car_id)
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating


@app.get("/cars/top10", response_model=List[CarResponseWithAvg])
def get_top_ten_ratings_cars(db: Session = Depends(get_db)):
    avg_ratings = (
        db.query(CarRating.car_id, func.avg(CarRating.rating).label("avg_rating"))
        .group_by(CarRating.car_id)
        .subquery()
    )

    top_cars = (
        db.query(Car, avg_ratings.c.avg_rating)
        .outerjoin(avg_ratings, Car.id == avg_ratings.c.car_id)
        .order_by(desc(avg_ratings.c.avg_rating))
        .limit(10)
        .all()
    )

    result = []
    for car, avg_rating in top_cars:
        car_dict = {
            "id": car.id,
            "brand": car.brand,
            "model": car.model,
            "year": car.year,
            "average_rating": round(avg_rating, 2),
            "ratings": [{"id": r.id, "rating": r.rating} for r in car.ratings],
        }
        result.append(car_dict)

    return result
