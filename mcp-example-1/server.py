from fastmcp import FastMCP

mcp = FastMCP(
    name="Calculator"
)

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together"""
    return a * b

# Run the server
if __name__ == "__main__":
    mcp.run(transport="stdio")