from fastapi import APIRouter, HTTPException
from app.services.user_service import UserService
from pydantic import BaseModel


class SignUpActivityRequest(BaseModel):
    user_id: int
    activity_id: int
    status: str


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def get_user(user_id: int = None, email: str = None):
    user = UserService.get_user(user_id, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/")
async def create_user(name: str, email: str, gender: str, password: str, phone: str):
    new_user_id = UserService.create_user(name, email, gender, password, phone)
    return {"message": "User created", "user_id": new_user_id}
