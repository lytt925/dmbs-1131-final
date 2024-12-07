from fastapi import APIRouter, HTTPException
from datetime import datetime
from pydantic import BaseModel
from enum import Enum
from app.services.employee_service import EmployeeService

router = APIRouter(prefix="/employees", tags=["Employees"])

class PunchType(str, Enum):
    IN = 'I'
    OUT = 'O'

class PunchRequest(BaseModel):
    employee_id: int
    punch_type: PunchType

@router.get("/stats/")
async def get_all_employees_stats(start_time: datetime, end_time: datetime):
    stats = EmployeeService.get_all_employees_stats(start_time, end_time)
    if not stats:
        raise HTTPException(
            status_code=404, detail="No data found for the given time range."
        )
    return stats


@router.post("/punch")
async def create_punch(punch: PunchRequest):
    employee_id = punch.employee_id
    punch_type = punch.punch_type
    punches = EmployeeService.create_punch_for_user(employee_id, punch_type)
    return punches


@router.get("/workloads")
async def get_averaged_workload(employee_id: int=None, month: str=None, year: str=None):
    workloads = EmployeeService.get_averaged_workload_by_month(employee_id, month, year)
    if type(workloads) is dict:
        raise HTTPException(status_code=workloads["error_code"], detail=workloads["message"])
    return workloads