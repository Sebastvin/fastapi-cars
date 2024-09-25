from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    brand = Column(String, index=True)
    model = Column(String, index=True)
    year = Column(Integer)

    ratings = relationship(
        "CarRating", back_populates="car", cascade="all, delete-orphan"
    )


class CarRating(Base):
    __tablename__ = "cars_ratings"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"))
    rating = Column(Integer)

    car = relationship("Car", back_populates="ratings")
