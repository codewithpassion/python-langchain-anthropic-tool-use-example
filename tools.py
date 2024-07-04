from langchain_core.tools import tool


@tool
def get_weather(location: str) -> str:
    """Get the weather for a given location"""
    return f"The weather in {location} is mostly sunny"


tools = [get_weather]
