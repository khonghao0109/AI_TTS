from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.posts import router as posts_router
from app.db.session import Base, engine
from app.models.user import User  # noqa: F401


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Day6 Auth API", lifespan=lifespan)
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(posts_router, prefix="/api/v1", tags=["posts"])


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Day6 Auth API running"}
