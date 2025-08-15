import json
from pathlib import Path


def test_add_schema_loads():
    p = Path(__file__).parents[1] / "tools" / "mcp_server" / "schemas" / "add.json"
    data = json.loads(p.read_text())
    assert "name" in data and data["name"] == "add"
    assert "input_schema" in data and "output_schema" in data
    assert data["input_schema"]["required"] == ["a", "b"]
    assert "total" in data["output_schema"]["properties"]
