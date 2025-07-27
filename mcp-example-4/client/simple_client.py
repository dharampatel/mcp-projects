import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")

async def main():
    async with client:

        # List available prompts
        prompts = await client.list_prompts()
        print("\n******************************Prompts******************************")
        for prompt in prompts:
            print("prompt: ", prompt)

        # List available resources
        resources = await client.list_resources()
        print("\n**********************************Resources*************************")
        for resource in resources:
            print("resource: ", resource)

        # List available resource templates
        resource_templates = await client.list_resource_templates()
        print("\n***************************Resource Templates******************************")
        for resource_template in resource_templates:
            print("resource_template: ", resource_template)

        # List available tools
        mcp_tools = await client.list_tools()
        print("\n************************Tools*********************************")
        for tool in mcp_tools:
            print("tool: ", tool)

            # Get a prompt
            prompt = await client.get_prompt("example_prompt", arguments={"question": "what is 2+2"})
            print("\n**************************Prompt**********************")
            print("prompt: ", prompt.messages[0].content.text)

            # Read a resource
            content = await client.read_resource("greeting://Alice")
            print("\n*************************Content***********************")
            print("content: ", content[0].text)

            # Call a tool
            result = await client.call_tool("add", arguments={"a": 2, "b": 2})
            print("\n********************Result***************************")
            print("math tool: ", result.content[0].text)

            result = await client.call_tool("weather_info", arguments={"location": "Delhi"})
            print("\n********************Result***************************")
            print("weather tool: ", result.content[0].text)



if __name__ == "__main__":
    asyncio.run(main())
