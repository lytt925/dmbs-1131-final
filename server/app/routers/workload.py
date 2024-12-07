from fastapi import APIRouter, HTTPException
from app.services.workload_service import WorkloadService

router = APIRouter(prefix="/workloads", tags=["Workloads"])

@router.get("/")
async def get_averaged_workload(employee_id: int=None, month: str=None):
    workloads = WorkloadService.get_averaged_workload_by_month(employee_id, month)
    if type(workloads) is dict:
        raise HTTPException(status_code=workloads["error_code"], detail=workloads["message"])
    return workloads