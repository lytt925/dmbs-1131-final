from fastapi import APIRouter, HTTPException
from app.services.animal_service import AnimalService

router = APIRouter(prefix="/animals", tags=["Animals"])

@router.get("/")
async def get_animals(animal_name: str=None, animal_id: int=None, shelter_id: int=None):
    animals = AnimalService.get_animals(animal_name, animal_id, shelter_id)
    if not animals:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animals