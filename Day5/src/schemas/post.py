from pydantic import BaseModel, ConfigDict, Field


class PostCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    content: str = Field(..., min_length=1)


class Post(PostCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
