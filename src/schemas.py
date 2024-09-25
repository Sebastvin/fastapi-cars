from pydantic import BaseModel
from typing import List


class CarBase(BaseModel):
    brand: str
    model: str
    year: int


class CarRatingBase(BaseModel):
    id: int
    rating: int

    class Config:
        from_attributes = True


class CarCreate(CarBase):
    pass


class CarResponse(CarBase):
    id: int
    ratings: List[CarRatingBase] = []

    class Config:
        from_attributes = True


class CarRatingBase(BaseModel):
    rating: int


class CarRatingCreate(CarRatingBase):
    pass


class CarResponseWithAvg(BaseModel):
    id: int
    brand: str
    model: str
    year: int
    average_rating: float
    ratings: List[CarRatingBase]

    class Config:
        orm_mode = True
