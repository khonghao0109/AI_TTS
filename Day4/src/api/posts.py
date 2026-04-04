from fastapi import APIRouter, Cookie, HTTPException, Path, Request, status

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
def create_post_endpoint(data: PostCreate) -> Post:
    return create_post(data)


@router.get("/posts", response_model=list[Post])
def get_posts_endpoint(
    request: Request,
    keyword: str | None = None,
    user_session: str | None = Cookie(default=None),
) -> list[Post]:
    user = "session" if user_session else "guest"
    print(f"[Request-ID: {request.state.request_id}] user = {user}")
    return get_posts(keyword)


@router.get("/posts/{post_id}", response_model=Post)
def get_post_by_id_endpoint(post_id: int = Path(..., gt=0)) -> Post:
    post = get_post_by_id(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail=POST_NOT_FOUND_DETAIL)
    return post


@router.put("/posts/{post_id}", response_model=Post)
def update_post_endpoint(data: PostCreate, post_id: int = Path(..., gt=0)) -> Post:
    post = update_post(post_id, data)
    if post is None:
        raise HTTPException(status_code=404, detail=POST_NOT_FOUND_DETAIL)
    return post


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_endpoint(post_id: int = Path(..., gt=0)) -> None:
    is_deleted = delete_post(post_id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail=POST_NOT_FOUND_DETAIL)
