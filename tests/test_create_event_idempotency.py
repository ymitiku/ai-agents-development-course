from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import json

async def call_create_event(payload, session):

    await session.initialize()
    return await session.call_tool("create_event", payload)

async def test_create_event_idempotency():
    payload = {"title":"Week0 Review","when":"2025-08-20T10:00:00Z"}
    params = StdioServerParameters(command="python", args=["-m", "tools.mcp_server.mcp_stdio"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            a = await call_create_event(payload, session)
            b = await call_create_event(payload, session)

    a_text = a.content[0].text
    b_text = b.content[0].text
    a_json = json.loads(a_text)
    b_json = json.loads(b_text)


    assert a_json["id"] == b_json["id"], "Idempotency failed: IDs do not match"

