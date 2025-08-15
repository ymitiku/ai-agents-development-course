#!/usr/bin/env python
"""
Week 0 smoke test (MCP over STDIO)

Spawns the MCP STDIO server at tools/mcp_server/mcp_stdio.py and
calls the "add" tool 50 times, reporting success rate and latency.

Usage:
  poetry run python scripts/run_smoke.py
"""

import asyncio
import json
import os
import random
import statistics
import time


async def run_mcp_smoke():
    from mcp import ClientSession, StdioServerParameters, types
    from mcp.client.stdio import stdio_client

    # You can override which command to run via env if needed
    cmd = os.environ.get("MCP_CMD", "python")
    args = os.environ.get("MCP_ARGS", "-m tools.mcp_server.mcp_stdio").split()

    server_params = StdioServerParameters(command=cmd, args=args)

    latencies = []
    ok = 0

    # Connect to the MCP server over stdio
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Sanity-check the tool exists
            tools = await session.list_tools()
            names = {t.name for t in tools.tools}
            if "add" not in names:
                raise RuntimeError(f"'add' tool not found; available tools: {sorted(names)}")

            for _ in range(50):
                a = random.randint(-10**6, 10**6)
                b = random.randint(-10**6, 10**6)

                t0 = time.time()
                result = await session.call_tool("add", {"a": a, "b": b})
                latencies.append(time.time() - t0)

                # Prefer structured content (dict) if provided by the server
                data = getattr(result, "structuredContent", None)

                # Fallback: try to parse the first text content as JSON
                if not isinstance(data, dict):
                    for c in getattr(result, "content", []) or []:
                        if isinstance(c, types.TextContent):
                            try:
                                data = json.loads(c.text)
                                break
                            except Exception:
                                pass

                if not isinstance(data, dict):
                    continue

                if data.get("total") == a + b and "trace_id" in data:
                    ok += 1

    p95 = sorted(latencies)[int(len(latencies) * 0.95) - 1]
    p50 = statistics.median(latencies)
    print(f"[W0][MCP] add: success={ok}/50, p50={p50:.3f}s, p95={p95:.3f}s")


if __name__ == "__main__":
    asyncio.run(run_mcp_smoke())
