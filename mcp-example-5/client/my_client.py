from typing import List
from typing_extensions import TypedDict
from typing import Annotated

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.checkpoint.memory import MemorySaver

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.resources import load_mcp_resources
from langchain_mcp_adapters.prompts import load_mcp_prompt
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

server_url = "http://localhost:8000/mcp"

async def create_graph(session):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, api_key=google_api_key)

    tools = await load_mcp_tools(session)
    llm_with_tool = llm.bind_tools(tools)

    system_prompt = await load_mcp_prompt(session, "system_prompt")
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt[0].content),
        MessagesPlaceholder("messages")
    ])
    chat_llm = prompt_template | llm_with_tool

    # State Management
    class State(TypedDict):
        messages: Annotated[List[AnyMessage], add_messages]

    # Nodes
    async def chat_node(state: State) -> State:
        state["messages"] = await chat_llm.ainvoke({"messages": state["messages"]})
        return state

    # Building the graph
    graph_builder = StateGraph(State)
    graph_builder.add_node("chat_node", chat_node)
    graph_builder.add_node("tool_node", ToolNode(tools=tools))
    graph_builder.add_edge(START, "chat_node")
    graph_builder.add_conditional_edges("chat_node", tools_condition, {"tools": "tool_node", "__end__": END})
    graph_builder.add_edge("tool_node", "chat_node")
    graph = graph_builder.compile(checkpointer=MemorySaver())

    return graph


async def main():
    config = {"configurable": {"thread_id": "001"}}
    async with streamablehttp_client(server_url) as (read, write, get_session_id):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Check available tools
            tools = await load_mcp_tools(session)
            print("Available tools:", [tool.name for tool in tools])

            # Check available prompts
            prompts = await load_mcp_prompt(session, "example_prompt", arguments={"question": "what is 10+20"})
            print("Available prompts:", [prompt.content for prompt in prompts])
            prompts = await load_mcp_prompt(session, "system_prompt")
            print("Available prompts:", [prompt.content for prompt in prompts])


            # Use the MCP Server in the graph
            agent = await create_graph(session)
            while True:
                message = input("User: ")
                if message in ["exit", "end", "quit"]:
                    print("Goodbye! Let me know if you need anything else in the future")
                    break
                response = await agent.ainvoke({"messages": message}, config=config)
                print("AI: " + response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())