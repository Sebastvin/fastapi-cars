from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import engine, get_db
from models import Car, Base, CarRating
from schemas import CarCreate, CarResponse, CarRatingCreate, CarResponseWithAvg
from sqlalchemy import func, desc
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI()


# function for debugging purposes
@app.get("/cars/", response_model=List[CarResponse])
def get_all_cars(db: Session = Depends(get_db)):
    cars = db.query(Car).all()
    return cars


@app.post("/cars/", response_model=CarResponse)
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    try:
        db_car = Car(**car.model_dump())
        db.add(db_car)
        db.commit()
        db.refresh(db_car)
        return db_car
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )


@app.post("/cars/{car_id}/rate")
def create_rating(
    car_id: int, car_rating: CarRatingCreate, db: Session = Depends(get_db)
):
    try:
        db_car = db.query(Car).filter(Car.id == car_id).first()
        if db_car is None:
            raise HTTPException(status_code=404, detail="Car not found")

        db_rating = CarRating(**car_rating.model_dump(), car_id=car_id)
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        return db_rating
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )


@app.get("/cars/top10", response_model=List[CarResponseWithAvg])
def get_top_ten_ratings_cars(db: Session = Depends(get_db)):
    try:
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
            if avg_rating:
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
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )
