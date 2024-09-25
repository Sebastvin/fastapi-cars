from pydantic import BaseModel, field_validator, Field
from datetime import date
from typing import List


CURRENT_YEAR: int = date.today().year
MINIMAL_YEAR: int = 1980


class CarBase(BaseModel):
    brand: str
    model: str
    year: int = Field(..., ge=MINIMAL_YEAR, le=CURRENT_YEAR)

    @field_validator("brand")
    def check_brand(cls, v):
        v = v.strip()
        if len(v) == 0:
            raise ValueError("Brand cannot be empty")
        if len(v) > 100:
            raise ValueError("Brand name is too long")
        return v

    @field_validator("model")
    def check_model(cls, v):
        v = v.strip()
        if len(v) == 0:
            raise ValueError("Model cannot be empty")
        if len(v) > 100:
            raise ValueError("Model name is too long")
        return v


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
