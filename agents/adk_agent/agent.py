from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset, StdioConnectionParams, StdioServerParameters
)

root_agent = LlmAgent(
    name="week0_adk_agent",
    model="gemini-2.0-flash",
    instruction="Use MCP tools to add numbers and create idempotent events.",
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="python",
                    args=["-m", "tools.mcp_server.mcp_stdio"],  # runs the file above
                ),
            ),
            # tool_filter=["add", "create_event"],  # optional: expose subset
        )
    ],
)
