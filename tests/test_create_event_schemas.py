import json
from pathlib import Path


def test_create_event_schema_loads():
    p = Path(__file__).parents[1] / "tools" / "mcp_server" / "schemas" / "create_event.json"
    data = json.loads(p.read_text())
    assert "name" in data and data["name"] == "create_event"
    assert "input_schema" in data and "output_schema" in data
    props = data["input_schema"]["properties"]
    assert "title" in props and "when" in props
    assert "when_iso" in data["output_schema"]["properties"]
