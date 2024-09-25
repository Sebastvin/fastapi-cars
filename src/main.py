from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Car, Base
from schemas import CarCreate, CarResponse


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/cars/", response_model=CarResponse)
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    db_car = Car(**car.model_dump())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car
