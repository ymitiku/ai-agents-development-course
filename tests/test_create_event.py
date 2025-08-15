from contextlib import asynccontextmanager
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import pytest
from typing import AsyncIterator



@pytest.fixture(scope="function")
def mcp_session_factory():
    @asynccontextmanager
    async def _factory() -> AsyncIterator[ClientSession]:
        params = StdioServerParameters(
            command="python",
            args=["-m", "tools.mcp_server.mcp_stdio"],
        )
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                yield session
    return _factory


@pytest.mark.asyncio
async def test_create_event(mcp_session_factory):
    payload = {"title": "Week0 Review", "when": "2025-08-20T10:00:00+00:00"}
    async with mcp_session_factory() as session:
        result = await session.call_tool("create_event", payload)
        result_json = json.loads(result.content[0].text)

    assert isinstance(result_json, dict)
    assert "id" in result_json
    assert "when_iso" in result_json
    assert result_json["title"] == payload["title"]
    assert result_json["when_iso"] == payload["when"]


@pytest.mark.asyncio
async def test_create_event_idempotency(mcp_session_factory):
    payload = {"title":"Week0 Review","when":"2025-08-20T10:00:00+00:00"}
    async with mcp_session_factory() as session:
        a = await session.call_tool("create_event", payload)
        b = await session.call_tool("create_event", payload)

    a_text = a.content[0].text
    b_text = b.content[0].text
    a_json = json.loads(a_text)
    b_json = json.loads(b_text)

    assert a_json["id"] == b_json["id"], "Idempotency failed: IDs do not match"

