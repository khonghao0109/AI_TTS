from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.post import Post
from src.schemas.post import PostCreate


async def create_post(db: AsyncSession, data: PostCreate) -> Post:
    post = Post(title=data.title, content=data.content)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


async def get_posts(db: AsyncSession, keyword: str | None = None) -> list[Post]:
    stmt = select(Post)
    if keyword:
        keyword_pattern = f"%{keyword}%"
        stmt = stmt.where(
            or_(
                Post.title.ilike(keyword_pattern),
                Post.content.ilike(keyword_pattern),
            )
        )

    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_post_by_id(db: AsyncSession, post_id: int) -> Post | None:
    stmt = select(Post).where(Post.id == post_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def update_post(db: AsyncSession, post_id: int, data: PostCreate) -> Post | None:
    stmt = select(Post).where(Post.id == post_id)
    result = await db.execute(stmt)
    post = result.scalar_one_or_none()
    if post is None:
        return None

    post.title = data.title
    post.content = data.content
    await db.commit()
    await db.refresh(post)
    return post


async def delete_post(db: AsyncSession, post_id: int) -> bool:
    stmt = select(Post).where(Post.id == post_id)
    result = await db.execute(stmt)
    post = result.scalar_one_or_none()
    if post is None:
        return False

    await db.delete(post)
    await db.commit()
    return True
