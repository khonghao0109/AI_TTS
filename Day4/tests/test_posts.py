from fastapi.testclient import TestClient

from src.main import app
from src.services.post_service import posts_storage

client = TestClient(app)


def setup_function():
    posts_storage.clear()


def test_root_health_check():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}


def test_create_post_valid():
    payload = {"title": "Hello FastAPI", "content": "Test content"}

    response = client.post("/posts", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == payload["title"]
    assert body["content"] == payload["content"]


def test_create_post_invalid_returns_422():
    payload = {"title": "Hi", "content": ""}

    response = client.post("/posts", json=payload)

    assert response.status_code == 422


def test_get_posts_returns_list():
    client.post("/posts", json={"title": "Post 1", "content": "Content 1"})
    client.post("/posts", json={"title": "Post 2", "content": "Content 2"})

    response = client.get("/posts")

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 2
    assert body[0]["id"] == 1
    assert body[1]["id"] == 2


def test_get_post_by_id_returns_object():
    client.post("/posts", json={"title": "Only post", "content": "One"})

    response = client.get("/posts/1")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == "Only post"
    assert body["content"] == "One"


def test_get_post_by_id_not_found_returns_404():
    response = client.get("/posts/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Post not found"
