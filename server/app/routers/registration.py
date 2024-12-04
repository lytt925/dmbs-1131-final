from fastapi import APIRouter, HTTPException
from app.services.registration_service import RegistrationService
from pydantic import BaseModel

class SignUpActivityRequest(BaseModel):
    user_id: int
    activity_id: int
    status: str

class CancelActivityRegistrationRequest(BaseModel):
    user_id: int
    activity_id: int

router = APIRouter(prefix="/registrations", tags=["Registration"])

@router.post("/")
async def sign_up_for_activity(request: SignUpActivityRequest):
    result = RegistrationService.sign_up_for_activity(
        user_id=request.user_id,
        activity_id=request.activity_id,
        status=request.status,
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