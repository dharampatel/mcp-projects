import asyncio
from fastmcp import Client
import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration

genai.configure(api_key = "AIzaSyAUhe6ZJ_YFRdB2djJtUHc6kHF5KrML0SM")
client = Client("http://localhost:8000/mcp")
def convert_to_function_declarations(mcp_tools):
    return [
        FunctionDeclaration(
            name=tool.name,
            description=tool.description,
            parameters={
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"},
                },
                "required": ["a", "b"]
            }
        ) for tool in mcp_tools
    ]


async def main():
    async with client:
        mcp_tools = await client.list_tools()
        function_decls = convert_to_function_declarations(mcp_tools)

        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            tools=function_decls
        )

        prompt = "Weather in Delhi?"
        response = await model.generate_content_async(prompt)

        # Extract tool name and params
        function_call = response.candidates[0].content.parts[0].function_call
        print("Tool call:", function_call.name)

        if not function_call.name:
            print("Sorry operation is not supported!")
            return

        a = function_call.args['a']
        b = function_call.args['b']

        print(f"a = {a}, b = {b}")

        result = await client.call_tool(function_call.name, arguments={"a": a, "b": b})
        print(f"Output: {a} & {b} = {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(main())

