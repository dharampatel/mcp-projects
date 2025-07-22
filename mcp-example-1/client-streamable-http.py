import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def main():
    async with streamablehttp_client("http://localhost:8050/mcp") as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")

            res = await session.call_tool("add", {"a": 2, "b": 3})
            print("2 + 3 =", res.content[0].text)

            res1 = await session.call_tool("multiply", {"a": 2, "b": 3})
            print("2 * 3 =", res1.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())
