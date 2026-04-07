import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import JWTError, jwt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def _validate_secret_key() -> None:
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY is not configured")
    if len(SECRET_KEY) < 32:
        raise ValueError("SECRET_KEY must be at least 32 characters")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    _validate_secret_key()

    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "iat": now})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict | None:
    try:
        _validate_secret_key()
    except ValueError:
        return None
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
