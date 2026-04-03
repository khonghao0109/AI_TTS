import httpx

from src.config import HTTP_TIMEOUT_SECONDS, OPENLIBRARY_SEARCH_URL


def fetch_books() -> list[dict[str, object]]:
    try:
        with httpx.Client(timeout=HTTP_TIMEOUT_SECONDS) as client:
            response = client.get(OPENLIBRARY_SEARCH_URL)
            response.raise_for_status()

        data = response.json()
        docs = data.get("docs")

        if not isinstance(docs, list):
            print("Invalid response format: 'docs' is not a list")
            return []

        if not all(isinstance(item, dict) for item in docs):
            print("Invalid response format: 'docs' contains non-dict items")
            return []

        return docs
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e.response.status_code}")
        return []
    except httpx.RequestError as e:
        print(f"Request failed: {e}")
        return []
