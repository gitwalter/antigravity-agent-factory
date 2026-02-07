"""Sample Python application for testing FRESH scenario."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """Root endpoint."""
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    """Get item by ID."""
    return {"item_id": item_id, "q": q}
