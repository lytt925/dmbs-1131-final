from fastapi import APIRouter, HTTPException
from app.services.statistics_service import StatisticsService

router = APIRouter(prefix="/statistics", tags=["Statistics"])

@router.get("/application")
async def get_total_application_statistics():
    statistics = StatisticsService.get_total_application_statistics()
    if not statistics:
        raise HTTPException(status_code=404, detail="Failed to retrieve statistics")
    return statistics

@router.get("/application/{filter}")
async def get_filtered_statistics(filter: str):
    statistics = StatisticsService.get_filtered_application_statistics(filter)
    if not statistics:
        raise HTTPException(status_code=404, detail="Failed to retrieve statistics")
    return statistics