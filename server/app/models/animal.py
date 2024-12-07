from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class SexEnum(str, Enum):
    FEMALE = "F"
    MALE = "M"


class SizeEnum(str, Enum):
    SMALL = "S"
    MEDIUM = "M"
    LARGE = "L"
    EXTRA_LARGE = "XL"


class SpeciesEnum(str, Enum):
    DOG = "狗"
    CAT = "貓"


class CreateAnimalModel(BaseModel):
    name: str = "Buddy"
    species: SpeciesEnum = SpeciesEnum.DOG
    breed: str = "Golden Retriever"
    size: SizeEnum = SizeEnum.LARGE
    is_sterilized: bool = True
    sex: SexEnum = SexEnum.FEMALE
    shelter_id: int = 1


class AnimalModel(CreateAnimalModel):
    animal_id: int
    death_time: Optional[datetime] = None
    adoption_status: str = "未領養"
    leave_at: Optional[datetime] = None
    arrived_at: datetime
