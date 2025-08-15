from fastapi import FastAPI, Header
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import hashlib
import uuid
import json
import os

app = FastAPI(title="Week0 MCP Tool Server")

SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "schemas")

with open(os.path.join(SCHEMA_DIR, "add.json"), "r") as f:
    ADD_SCHEMA = json.load(f)
with open(os.path.join(SCHEMA_DIR, "create_event.json"), "r") as f:
    CREATE_EVENT_SCHEMA = json.load(f)

# In-memory event store for idempotency demo
EVENT_STORE: Dict[str, Dict[str, Any]] = {}


class AddIn(BaseModel):
    a: int
    b: int


class AddOut(BaseModel):
    total: int
    trace_id: str


class CreateEventIn(BaseModel):
    title: str = Field(min_length=1)
    when: datetime

    @field_validator("when")
    @classmethod
    def ensure_tz(cls, v: datetime) -> datetime:
        # Normalize to UTC ISO
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v.astimezone(timezone.utc)


class CreateEventOut(BaseModel):
    id: str
    when_iso: str


@app.get("/manifest")
def manifest():
    return {
        "name": "week0-mcp-server",
        "tools": [
            {
                "name": ADD_SCHEMA["name"],
                "input_schema": ADD_SCHEMA["input_schema"],
                "output_schema": ADD_SCHEMA["output_schema"],
            },
            {
                "name": CREATE_EVENT_SCHEMA["name"],
                "input_schema": CREATE_EVENT_SCHEMA["input_schema"],
                "output_schema": CREATE_EVENT_SCHEMA["output_schema"],
            },
        ],
    }


@app.post("/call/add", response_model=AddOut)
def call_add(payload: AddIn):
    trace_id = str(uuid.uuid4())
    return AddOut(total=payload.a + payload.b, trace_id=trace_id)


@app.post("/call/create_event", response_model=CreateEventOut)
def call_create_event(
    payload: CreateEventIn,
    idempotency_key: Optional[str] = Header(default=None, alias="Idempotency-Key"),
):
    # Deterministic id if key provided; else derive from args
    if idempotency_key is None:
        base = f"{payload.title}|{payload.when.isoformat()}"
        idempotency_key = hashlib.sha256(base.encode()).hexdigest()

    if idempotency_key in EVENT_STORE:
        rec = EVENT_STORE[idempotency_key]
        return CreateEventOut(id=rec["id"], when_iso=rec["when_iso"])

    # Create new event
    event_id = str(uuid.uuid4())
    when_iso = payload.when.isoformat()
    EVENT_STORE[idempotency_key] = {"id": event_id, "when_iso": when_iso}
    return CreateEventOut(id=event_id, when_iso=when_iso)

@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
