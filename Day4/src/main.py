from uuid import uuid4

from fastapi import FastAPI, Request, Response

from src.api.posts import router as posts_router

app = FastAPI()
app.include_router(posts_router)


@app.middleware("http")
async def request_id_middleware(request: Request, call_next) -> Response:
    request_id = request.headers.get("X-Request-ID") or str(uuid4())
    request.state.request_id = request_id
    print(f"[Request-ID: {request_id}] {request.method} {request.url.path}")

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


@app.get("/")
def health_check() -> dict:
    return {"message": "API is running"}
