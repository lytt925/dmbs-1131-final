from fastapi import APIRouter, HTTPException
from app.services.workload_service import WorkloadService

router = APIRouter(prefix="/workloads", tags=["Workloads"])

@router.get("/")
async def get_averaged_workload(employee_id: int=None, month: str=None):
    workloads = WorkloadService.get_averaged_workload(employee_id, month)
    if not workloads:
        raise HTTPException(status_code=404, detail="Workload not found")
    return workloads