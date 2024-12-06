from fastapi import APIRouter, HTTPException
from app.services.care_service import CareService

router = APIRouter(prefix="/carerecords", tags=["Care Records"])

@router.get("/{animal_id}")
async def get_care(animal_id: int):
    care_record = CareService.get_care_by_id(animal_id)
    if not care_record:
        raise HTTPException(status_code=404, detail="Care records not found")
    return care_record

@router.post("/")
async def create_care(animal_id: int, employee_id: int, care_type: str):
    care_record = CareService.create_care(animal_id, employee_id, care_type)
    if not care_record:
        raise HTTPException(status_code=422, detail="Unprocessable Content")
    return care_record