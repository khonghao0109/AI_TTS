from fastapi import APIRouter, Cookie, Depends, HTTPException, Path, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.schemas.post import Post, PostCreate
from src.services.post_service import (
    create_post,
    delete_post,
    get_post_by_id,
    get_posts,
    update_post,
)

router = APIRouter()
POST_NOT_FOUND_DETAIL = "Post not found"


@router.post("/posts", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post_endpoint(
    data: PostCreate, db: AsyncSession = Depends(get_db)
) -> Post:
    post = await create_post(db, data)
    return Post.model_validate(post)


@router.get("/posts", response_model=list[Post])
async def get_posts_endpoint(
    request: Request,
    keyword: str | None = None,
    user_session: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
) -> list[Post]:
    user = "session" if user_session else "guest"
    print(f"[Request-ID: {request.state.request_id}] user = {user}")
    posts = await get_posts(db, keyword)
    return [Post.model_validate(post) for post in posts]


@router.get("/posts/{post_id}", response_model=Post)
async def get_post_by_id_endpoint(
    post_id: int = Path(..., gt=0), db: AsyncSession = Depends(get_db)
) -> Post:
    post = await get_post_by_id(db, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail=POST_NOT_FOUND_DETAIL)
    return Post.model_validate(post)


@router.put("/posts/{post_id}", response_model=Post)
async def update_post_endpoint(
    data: PostCreate,
    post_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
) -> Post:
    post = await update_post(db, post_id, data)
    if post is None:
        raise HTTPException(status_code=404, detail=POST_NOT_FOUND_DETAIL)
    return Post.model_validate(post)


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_endpoint(
    post_id: int = Path(..., gt=0), db: AsyncSession = Depends(get_db)
) -> None:
    is_deleted = await delete_post(db, post_id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail=POST_NOT_FOUND_DETAIL)
