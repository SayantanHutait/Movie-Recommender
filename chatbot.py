# chat_agent.py

from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
load_dotenv()



# Load LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant"
)

# Define tools
search_tool = TavilySearch(
    max_results=4,
    include_image="False",
)
tools = [search_tool]

# Create the React agent
agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt="""
    keep the topic general
You are a helpful AI assistant to give answer about movies. If you know the answer, respond directly.
If not, use the web search tool.
"""
)
def get_response(user_input:str, chat_history:list)->tuple[str,list]:
    chat_history.append({"role": "user", "content": user_input})
    result = agent.invoke({"messages": chat_history})
    assistant_msg = result["messages"][-1]
    chat_history.append({"role": "assistant", "content": assistant_msg.content})
    return assistant_msg.content, chat_history


if __name__ == "__main__":
    chat_history = []  # keeps previous messages

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Add user message to chat history
        chat_history.append({"role": "user", "content": user_input})

        # Run the agent with full history
        result = agent.invoke({"messages": chat_history})

        # Extract assistant message and print it
        assistant_msg = result["messages"][-1]
        print("Bot:", assistant_msg.content)

        # Add assistant response to chat history
        chat_history.append({"role": "assistant", "content": assistant_msg.content})


