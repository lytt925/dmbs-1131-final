from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.services.employee_service import EmployeeService

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.get("/stats/")
async def get_all_employees_stats(start_time: datetime, end_time: datetime):
    stats = EmployeeService.get_all_employees_stats(start_time, end_time)
    if not stats:
        raise HTTPException(status_code=404, detail="No data found for the given time range.")
    return stats

