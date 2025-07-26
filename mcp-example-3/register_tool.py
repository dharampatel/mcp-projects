from math_tool import add, multiply
from server_config import mcp
from weather_tool import weather_info

mcp.tool()(add)
mcp.tool()(multiply)
mcp.tool()(weather_info)