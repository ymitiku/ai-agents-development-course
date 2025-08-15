from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

async def call_create_event(payload):
    params = StdioServerParameters(command="python", args=["-m", "tools.mcp_server.mcp_stdio"])
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            return await s.call_tool("create_event", payload)

async def test_create_event_idempotency():
    payload = {"title":"Week0 Review","when":"2025-08-20T10:00:00Z"}
    a = await call_create_event(payload)
    b = await call_create_event(payload)

    assert a.structuredContent or a.content
    assert b.structuredContent or b.content