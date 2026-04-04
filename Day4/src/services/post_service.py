from src.schemas.post import Post, PostCreate

posts_storage: list[Post] = []


def create_post(data: PostCreate) -> Post:
    post = Post(id=len(posts_storage) + 1, title=data.title, content=data.content)
    posts_storage.append(post)
    return post


def get_posts(keyword: str | None = None) -> list[Post]:
    if keyword is None:
        return posts_storage.copy()

    keyword_lower = keyword.lower()
    return [
        post
        for post in posts_storage
        if keyword_lower in post.title.lower() or keyword_lower in post.content.lower()
    ]


def get_post_by_id(post_id: int) -> Post | None:
    for post in posts_storage:
        if post.id == post_id:
            return post
    return None


def update_post(post_id: int, data: PostCreate) -> Post | None:
    for index, post in enumerate(posts_storage):
        if post.id == post_id:
            updated_post = Post(id=post_id, title=data.title, content=data.content)
            posts_storage[index] = updated_post
            return updated_post
    return None


def delete_post(post_id: int) -> bool:
    for index, post in enumerate(posts_storage):
        if post.id == post_id:
            posts_storage.pop(index)
            return True
    return False
