from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.models.user import User
from app.services.user_service import create_user, get_user_by_email
from app.utils.hash import verify_password


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email(db, email)
    if user is None:
        return None

    if not user.is_active:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


async def register_user(db: AsyncSession, email: str, password: str) -> User:
    existing_user = await get_user_by_email(db, email)
    if existing_user is not None:
        raise ValueError("Email already exists")

    return await create_user(
        db=db,
        email=email,
        password=password,
        role="user",
    )


async def login_user(db: AsyncSession, email: str, password: str) -> str | None:
    user = await authenticate_user(db=db, email=email, password=password)
    if user is None:
        return None

    return create_access_token({"sub": str(user.id), "role": user.role})
