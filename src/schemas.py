from pydantic import BaseModel, field_validator
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


class CarRatingCreate(BaseModel):
    rating: int

    @field_validator("rating")
    def check_rating_range(cls, v):
        if v < 1 or v > 5:
            raise ValueError("Rating must be between 1 and 5")
        return v


class CarResponseWithAvg(BaseModel):
    id: int
    brand: str
    model: str
    year: int
    average_rating: float
    ratings: List[CarRatingBase]

    class Config:
        orm_mode = True
