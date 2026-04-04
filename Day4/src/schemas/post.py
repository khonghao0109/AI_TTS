from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    content: str = Field(..., min_length=1)


class Post(PostCreate):
    id: int
