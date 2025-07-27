from fastmcp import FastMCP

mcp = FastMCP("math", port=8001)

# Prompts
@mcp.prompt()
def example_prompt(question: str) -> str:
    """Example prompt description"""
    return f"""
    You are a Math and BMI expert and you are also good in writing engaging story. 
    Answer the question.
    Question: {question}
    """

@mcp.prompt()
def system_prompt() -> str:
    """System prompt description"""
    return """
    You are an AI assistant use the tools if needed.
    """

# Tools
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def calculate_bmi(weight: int, height: int) -> str:
    """Calculate BMI"""
    return "BMI: "+str(weight/(height*height))

if __name__ == "__main__":
    mcp.run("streamable-http")
