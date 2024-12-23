from fastapi import APIRouter, HTTPException
from app.services.application_service import ApplicationService
from app.services.animal_service import AnimalService
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/applications", tags=["Application"])

class ApplicationCreate(BaseModel):
    user_id: int
    animal_id: int
    
@router.post("/")
async def create_application(application: ApplicationCreate):
    isAnimalAvailable = AnimalService.check_animal_availability(application.animal_id)
    if not isAnimalAvailable:
        raise HTTPException(status_code=400, detail="The animal is not available for adoption.")
    result = ApplicationService.create_application(
        user_id=application.user_id,
        animal_id=application.animal_id
    )

    if result["success"]:
        return result["data"]
    else:
        detail_message = "Conditions not met: " + result["reasons"]
        raise HTTPException(status_code=400, detail=detail_message)


@router.get("/")
async def get_applications(user_id: Optional[int]=None, animal_id: Optional[int]=None, shelter_id:Optional[int]= None):
    # 依據查詢參數決定要查詢的條件
    apps = ApplicationService.get_applications(user_id=user_id, animal_id=animal_id, shelter_id = shelter_id)
    if not apps:
        raise HTTPException(status_code=404, detail="No applications found for given conditions.")
    return apps


@router.put("/{application_id}/status")
async def update_application_status(application_id: int, status: str):
    updated_app = ApplicationService.update_application_status(application_id, status)

    if not updated_app:
        raise HTTPException(status_code=404, detail="Application not found or update failed.")

    # 如果更新為 S(成功)，則將該動物其他待處理中的申請全部改為 F(失敗)
    if status == "S":
        ApplicationService.fail_all_prev_applications(updated_app["animal_id"], application_id)

    return updated_app

@router.get("/stats")
async def get_total_application_statistics():
    statistics = ApplicationService.get_total_application_statistics()
    if not statistics:
        raise HTTPException(status_code=404, detail="Failed to retrieve statistics")
    return statistics

@router.get("/stats/{filter}")
async def get_filtered_statistics(filter: str):
    statistics = ApplicationService.get_filtered_application_statistics(filter)
    if not statistics:
        raise HTTPException(status_code=404, detail="Failed to retrieve statistics")
    return statistics