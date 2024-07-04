import os
from tools import tools
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage, BaseMessage
from langchain_anthropic import ChatAnthropic

from dotenv import load_dotenv

if not load_dotenv() and not os.getenv("ANTHROPIC_API_KEY"):
    print("Please set the ANTHROPIC_API_KEY environment variable")
    exit(1)

anthropic_key = os.getenv("ANTHROPIC_API_KEY")
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20240620", api_key=anthropic_key, verbose=True
)
llm_with_tools = llm.bind_tools(tools)
messages = []


def exit_program():
    print("Ok, bye!")
    exit(0)


def query():
    try:
        user_input = input("What would you like to do? ")
    except KeyboardInterrupt:
        print()
        exit_program()

    if user_input.lower() in ["quit", "exit"]:
        exit_program()
    return user_input


def call_claude(prompt) -> AIMessage:
    """Call the LLM with the given prompt and return the response.
    returns: AIMessage
    """

    messages.append(HumanMessage(prompt))
    ai_msg: AIMessage = llm_with_tools.invoke(messages)  # type: ignore
    messages.append(ai_msg)
    return ai_msg


def select_tool(tool_name: str):
    toolMap = dict()
    for tool in tools:
        toolMap[tool.name] = tool

    return toolMap[tool_name]


def main():
    while True:
        prompt = query()

        ai_msg = call_claude(prompt)

        if not ai_msg.tool_calls:
            print(ai_msg.content)
            continue
        else:
            for tool_call in ai_msg.tool_calls:
                selected_tool = select_tool(tool_call["name"])
                tool_output = selected_tool.invoke(tool_call["args"])
                messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))

            ai_msg = llm_with_tools.invoke(messages)
            print(ai_msg.content)
            continue


if __name__ == "__main__":
    main()
