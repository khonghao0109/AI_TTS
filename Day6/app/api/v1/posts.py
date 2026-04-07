from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/posts")
async def list_posts(current_user: User = Depends(get_current_user)) -> dict:
    return {
        "message": "Protected posts endpoint",
        "current_user": {
            "id": current_user.id,
            "email": current_user.email,
            "role": current_user.role,
        },
    }
