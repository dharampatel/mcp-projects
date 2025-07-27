from fastmcp import FastMCP
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv(override=True)
google_api_key = os.getenv("GOOGLE_API_KEY")

mcp = FastMCP("story-writer", port=8002)
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=google_api_key)

@mcp.prompt()
def example_prompt(question: str) -> str:
    """Example prompt description"""
    return f"""
    You are expert in writing engaging story. 
    Answer the question.
    Question: {question}
    """

@mcp.prompt()
def system_prompt() -> str:
    """System prompt description"""
    return """
    You are an AI assistant use the tools if needed.
    """


@mcp.tool()
async def write_story(topic: str) -> str:
    """Write a story.
    Args:
        topic: The story topic
    Returns:
        The written story as a string
    """
    try:
        messages = [
            (
                "system",
                "You are expert on story writing. Create an engaging short story on the given topic in a maximum of 200 words. Provide the output in markdown format only.",
            ),
            ("human", f"The topic is: {topic}"),
        ]
        ai_msg = await model.ainvoke(messages)
        return ai_msg.content
    except Exception as e:
        return f"An error occurred while writing story: {e}"

if __name__ == "__main__":
  mcp.run("streamable-http")
