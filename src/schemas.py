from pydantic import BaseModel, field_validator, Field
from datetime import date
from typing import List


CURRENT_YEAR: int = date.today().year
MINIMAL_YEAR: int = 1980


class CarBase(BaseModel):
    brand: str
    model: str
    year: int = Field(..., ge=MINIMAL_YEAR, le=CURRENT_YEAR)


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


class CarRatingCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)


class CarResponseWithAvg(BaseModel):
    id: int
    brand: str
    model: str
    year: int
    average_rating: float
    ratings: List[CarRatingBase]

    class Config:
        from_attributes = True
