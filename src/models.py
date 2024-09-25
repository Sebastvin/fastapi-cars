from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    brand = Column(String, index=True, nullable=False)
    model = Column(String, index=True, nullable=False)
    year = Column(Integer, nullable=False)

    ratings = relationship(
        "CarRating", back_populates="car", cascade="all, delete-orphan"
    )


class CarRating(Base):
    __tablename__ = "cars_ratings"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    rating = Column(Integer, nullable=False)

    car = relationship("Car", back_populates="ratings")
