# scripts/check_idempotency_mcp.py
import asyncio, json
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

async def main():
    params = StdioServerParameters(command="python", args=["-m","tools.mcp_server.mcp_stdio"])
    async with stdio_client(params) as (r,w):
        async with ClientSession(r,w) as s:
            await s.initialize()
            payload = {"title":"Week0 Review","when":"2025-08-20T10:00:00Z"}
            a = await s.call_tool("create_event", payload)
            b = await s.call_tool("create_event", payload)
            print("A:", a.structuredContent or a.content)
            print("B:", b.structuredContent or b.content)

if __name__ == "__main__":
    asyncio.run(main())
