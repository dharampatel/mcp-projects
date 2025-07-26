from server_config import mcp
import register_tool


if __name__ == "__main__":
    mcp.run(transport="streamable-http")


# run sever by
# uv run server.py
# python server.py
