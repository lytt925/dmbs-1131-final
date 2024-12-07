from fastapi import APIRouter, HTTPException
from app.services.animal_service import AnimalService
from app.models.animal import CreateAnimalModel

router = APIRouter(prefix="/animals", tags=["Animals"])


@router.get("/")
async def get_animals(
    animal_name: str = None, animal_id: int = None, shelter_id: int = None
):
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
async def update_animals_adoption(
    animal_name: str = None, animal_id: int = None, shelter_id: int = None, adoption_status: str = "已領養"
):
    animals = AnimalService.update_animals_adoption(adoption_status, animal_name, animal_id, shelter_id)
    if not animals:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animals


@router.post("/")
async def create_animal(animal: CreateAnimalModel):
    created_animal = AnimalService.create_animal(
        name=animal.name,
        species=animal.species,
        breed=animal.breed,
        size=animal.size,
        is_sterilized=animal.is_sterilized,
        sex=animal.sex,
        shelter_id=animal.shelter_id,
    )

    if not created_animal:
        raise HTTPException(status_code=400, detail="Unable to create animal.")

    return created_animal
