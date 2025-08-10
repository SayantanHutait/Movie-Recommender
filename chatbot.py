# chat_agent.py

from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
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
    topic="general"
)
tools = [search_tool]

checkpointer = InMemorySaver()

# Create the React agent
agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt="""
    keep the topic general
You are a helpful AI assistant to give answer about movies. If you know the answer, respond directly.
If not, use the web search tool.
""",
checkpointer=checkpointer
)


config = {"configurable": {"thread_id": "1"}}

if __name__ == "__main__":
    chat_history = []  # keeps previous messages

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Add user message to chat history
        chat_history.append({"role": "user", "content": user_input})

        # Run the agent with full history
        result = agent.invoke({"messages": [HumanMessage(content=user_input)]}, config=config)

        # Extract assistant message and print it
        assistant_msg = result["messages"][-1]
        print("Bot:", assistant_msg.content)


