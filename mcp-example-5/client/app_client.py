from typing import List
from typing_extensions import TypedDict
from typing import Annotated
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.prompts import load_mcp_prompt
import asyncio
from dotenv import load_dotenv
import os

load_dotenv(override=True)
google_api_key = os.getenv("GOOGLE_API_KEY")

client = MultiServerMCPClient(
    {
        "math": {
            "url": "http://localhost:8001/mcp",
            "transport": "streamable_http",
        },
        "story-writer": {
            "url": "http://localhost:8002/mcp",
            "transport": "streamable_http",
        }
    }
)


async def create_graph(math_session, story_session):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, api_key=google_api_key)

    math_tools = await load_mcp_tools(math_session)
    story_tools = await load_mcp_tools(story_session)
    tools = math_tools + story_tools
    llm_with_tool = llm.bind_tools(tools)

    system_prompt = await load_mcp_prompt(math_session, "system_prompt")
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt[0].content),
        MessagesPlaceholder("messages")
    ])

    chain = prompt_template | llm_with_tool

    # State Management
    class State(TypedDict):
        messages: Annotated[List[AnyMessage], add_messages]

    # Nodes
    async def chat_node(state: State) -> State:
        state["messages"] = await chain.ainvoke({"messages": state["messages"]})
        return state

    # Building the graph
    graph_builder = StateGraph(State)
    graph_builder.add_node("chat_node", chat_node)
    graph_builder.add_node("tools", ToolNode(tools=tools))
    graph_builder.add_edge(START, "chat_node")
    graph_builder.add_conditional_edges("chat_node", tools_condition)
    graph_builder.add_edge("tools", "chat_node")
    graph = graph_builder.compile(checkpointer=MemorySaver())
    return graph


async def main():
    config = {"configurable": {"thread_id": "002"}}
    async with client.session("math") as math_session, client.session("story-writer") as story_session:
        agent = await create_graph(math_session, story_session)
        while True:
            message = input("You: ")
            if message in ["exit", "quit", "end", "q"]:
                print("Good Bye!!!")
                break
            response = await agent.ainvoke({"messages": message}, config=config)
            print("AI: "+response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())