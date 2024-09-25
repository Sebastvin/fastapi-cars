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
        orm_mode = True


class CarCreate(CarBase):
    pass


class CarResponse(CarBase):
    id: int
    ratings: List[CarRatingBase] = []

    class Config:
        orm_mode = True
