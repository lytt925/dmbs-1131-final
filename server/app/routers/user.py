from fastapi import APIRouter, HTTPException
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/{user_id}")
async def get_user(user_id: int):
    user = UserService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/")
async def create_user(name: str, email: str):
    new_user_id = UserService.create_user(name, email)
    return {"message": "User created", "user_id": new_user_id}
