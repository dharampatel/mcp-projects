from fastmcp import FastMCP

mcp = FastMCP(name="Calculater App")

@mcp.tool()
def add(a, b):
    """Add two numbers and return result"""
    return a + b


@mcp.tool()
def multiply(a, b):
    """Multiply two numbers and return result"""
    return a * b


if __name__ == "__main__":
    mcp.run(transport="streamable-http")


# run sever by
# uv run server.py
# python server.py
