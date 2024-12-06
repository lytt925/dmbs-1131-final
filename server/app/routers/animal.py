from fastapi import APIRouter, HTTPException
from app.services.animal_service import AnimalService
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AnimalModel(BaseModel):
    animal_id: int
    name: str
    species: str
    breed: str
    size: str
    death_time: Optional[datetime] = None
    adoption_status: Optional[str] = "未領養"  
    leave_at: Optional[datetime] = None
    arrived_at: datetime
    is_sterilized: bool
    sex: str
    shelter_id: int

router = APIRouter(prefix="/animals", tags=["Animals"])

@router.get("/")
async def get_animals(animal_name: str=None, animal_id: int=None, shelter_id: int=None):
    animals = AnimalService.get_animals(animal_name, animal_id, shelter_id)
    if not animals:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animals

@router.get("/unadopted")
async def get_unadopted_animals():
    animals = AnimalService.get_unadopted_animals()
    if not animals:
        raise HTTPException(status_code=404, detail="No unadopted animals found")
    return animals


@router.put("/")
async def update_animals_adoption(animal_name: str=None, animal_id: int=None, shelter_id: int=None):
    animals = AnimalService.update_animals_adoption(animal_name, animal_id, shelter_id)
    if not animals:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animals

@router.post("/")
async def create_animal(animal: AnimalModel):
    created_animal = AnimalService.create_animal(
        animal_id = animal.animal_id,
        name = animal.name,
        species=animal.species,
        breed=animal.breed,
        size=animal.size,
        death_time= None,
        adoption_status=animal.adoption_status,
        leave_at= None,
        arrived_at=animal.arrived_at,
        is_sterilized=animal.is_sterilized,
        sex=animal.sex,
        shelter_id=animal.shelter_id
    )
    
    if not created_animal:
        raise HTTPException(status_code=400, detail="Unable to create animal.")

    return created_animal