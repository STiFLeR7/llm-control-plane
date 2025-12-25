from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from app.main import handle_request

app = FastAPI(
    title="LLM Control Plane API",
    description="Controlled, auditable inference backend",
    version="0.4.0",
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str
    embedding_model: Optional[str] = None  # NEW


@app.post("/query")
def query_control_plane(payload: QueryRequest):
    """
    Thin HTTP adapter.
    No logic lives here.
    """
    return handle_request(
        user_query=payload.query,
        embedding_model=payload.embedding_model,
    )
