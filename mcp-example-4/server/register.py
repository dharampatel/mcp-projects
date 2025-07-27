from fastmcp import FastMCP

from server.math_tools import add, multiply
from server.prompts import example_prompt, system_prompt
from server.resources import get_greeting, get_config
from server.weather_tool import weather_info

mcp = FastMCP("Common Server")

# Register tools
mcp.tool()(add)
mcp.tool()(multiply)
mcp.tool()(weather_info)

# Register prompts
mcp.prompt()(example_prompt)
mcp.prompt()(system_prompt)

# Register resources
mcp.resource("greeting://{name}")(get_greeting)
mcp.resource("config://app")(get_config)