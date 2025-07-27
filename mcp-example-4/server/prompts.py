def example_prompt(question: str) -> str:
    """Example prompt description"""

    return f"""
    You are a helpful assistant. Answer the question for math and weather.
    Question: {question}
    """


def system_prompt() -> str:
    """System prompt description"""

    return """
    You are a helpful AI assistant use the tools if needed.
    """