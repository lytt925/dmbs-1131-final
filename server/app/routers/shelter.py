from fastapi import APIRouter, HTTPException
from app.services.shelter_service import ShelterService

router = APIRouter(prefix="/shelters", tags=["Shelters"])

@router.get("/")
async def get_shelters():
    """
    Get all shelters.
    """
    try:
        data = ShelterService.get_shelters()
        return {
            "message": "Shelters retrieved successfully",
            "data": data,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/occupancy")
async def get_shelter_occupancy():
    """
    Get the current occupancy rates for all shelters.
    """
    try:
        data = ShelterService.get_shelter_occupancy()
        return {
            "message": "Shelter occupancy rates retrieved successfully",
            "data": data,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/retention")
async def get_shelter_animal_retention():
    """
    Get the average retention (stay duration in days) of animals, grouped by species and shelter.
    """
    try:
        data = ShelterService.get_shelter_animal_retention()
        return {
            "message": "Animal retention data retrieved successfully",
            "data": data,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
