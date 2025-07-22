import asyncio
import nest_asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

nest_asyncio.apply()

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")

            # ✅ Fix: Await the coroutine
            answer = await session.call_tool("add", arguments={"a": 10, "b": 30})
            print(f"10 + 30 = {answer.content[0].text}")
            print(f"10 + 30 = {answer.structuredContent}")

asyncio.run(main())
