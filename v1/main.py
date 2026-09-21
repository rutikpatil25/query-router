"""FastAPI backend for the query router."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from router import route_query


app = FastAPI(title="Local/Online Query Router", version="1.0.0")


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="User query to classify")


@app.get("/")
def root() -> dict:
    return {
        "name": "Local/Online Query Router",
        "status": "ok",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/route")
def route(request: QueryRequest) -> dict:
    try:
        return route_query(request.query)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except FileNotFoundError as error:
        raise HTTPException(
            status_code=503, detail="Model files are missing; run train.py first"
        ) from error
