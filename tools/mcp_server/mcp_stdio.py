from typing import Dict
from datetime import datetime, timezone
import hashlib, uuid
from mcp.server.fastmcp import FastMCP  # official MCP Python SDK

mcp = FastMCP("week0")

_EVENT_STORE: Dict[str, Dict[str, str]] = {}

@mcp.tool()
def add(a: int, b: int) -> dict:
    """Return the sum of a and b, and a trace id."""
    return {"total": a + b, "trace_id": str(uuid.uuid4())}

@mcp.tool()
def create_event(title: str, when: str) -> dict:
    """Create (idempotent) event. 'when' must be ISO-8601."""
    dt = datetime.fromisoformat(when.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)

    key = hashlib.sha256(f"{title}|{dt.isoformat()}".encode()).hexdigest()
    if key in _EVENT_STORE:
        return _EVENT_STORE[key]

    rec = {"id": str(uuid.uuid4()), "when_iso": dt.isoformat(), "title": title}
    _EVENT_STORE[key] = rec
    return rec

@mcp.resource("events://")
def get_events() -> dict:
    """Get all events."""
    return {"events": list(_EVENT_STORE.values())}

@mcp.resource("events://{event_id}")
def get_event(event_id: str) -> dict:
    """Get a specific event by ID."""
    if event_id not in _EVENT_STORE:
        raise mcp.NotFound(f"Event with id {event_id} not found.")
    return _EVENT_STORE[event_id]


if __name__ == "__main__":
    # Run over stdio (don’t print to stdout; logs to stderr only)
    mcp.run(transport="stdio")
