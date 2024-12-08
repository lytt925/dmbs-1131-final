from fastapi import APIRouter, HTTPException, Query
from app.services.registration_service import RegistrationService
from pydantic import BaseModel


class SignUpActivityRequest(BaseModel):
    user_id: int
    activity_id: int

class CancelActivityRegistrationRequest(BaseModel):
    user_id: int
    activity_id: int


router = APIRouter(prefix="/registrations", tags=["Registration"])


@router.post("/")
async def sign_up_for_activity(request: SignUpActivityRequest):
    result = RegistrationService.sign_up_for_activity(
        user_id=request.user_id,
        activity_id=request.activity_id,
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return {
        "message": "Successfully signed up for activity",
        "data": result["data"],
    }


@router.patch("/")
async def cancel_activity_registration(request: CancelActivityRegistrationRequest):
    result = RegistrationService.cancel_activity_registration(
        user_id=request.user_id,
        activity_id=request.activity_id,
    )

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return {
        "message": "Successfully cancelled activity registration",
        "data": result["data"],
    }

@router.get("/")
async def get_registrations_by_user_id(
    user_id: int,
    page: int = Query(1, ge=1, description="Page number (must be >= 1)"),
    per_page: int = Query(
        10, ge=1, le=100, description="Number of items per page (1-100)"
    ),
):
    """
    Get registrations for a specific user with pagination.
    """
    try:
        result = RegistrationService.get_registration_by_user_id(
            user_id=user_id, page=page, per_page=per_page
        )
        return {
            "message": "Registrations retrieved successfully",
            "data": result["data"],
            "meta": result["meta"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
