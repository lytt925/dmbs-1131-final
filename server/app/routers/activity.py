from fastapi import APIRouter, HTTPException
from app.services.activity_service import ActivityService

router = APIRouter(prefix="/activities", tags=["Activity"])

@router.get("/")
async def get_all_activities_from_now(shelter_id: int = None):
    activities = ActivityService.get_all_activities_from_now(shelter_id)
    if not activities:
        raise HTTPException(status_code=404, detail="No activities found")
    return activities
