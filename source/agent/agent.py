import os, getpass
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage
from crud import add_task, list_tasks, update_task_status, delete_task

sys_msg = SystemMessage(content="You are a helpful assistant tasked with helping the user with his TODO list.")

def assistant(state: MessagesState):
   return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

tools = [add_task, list_tasks, update_task_status, delete_task]
llm = ChatOpenAI(model="gpt-4o")

llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)

builder = StateGraph(MessagesState)

builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)
builder.add_edge("tools", "assistant")
react_graph = builder.compile()

# Method to invoke the react_graph and return the last message in the messages property from the response
import asyncio
from typing import List, Dict, Any
from langchain_core.messages import BaseMessage

async def invoke_and_get_last_message(messages: List[BaseMessage]) -> Any:
    """
    Invokes the react_graph with the given messages and returns the last message in the response's messages property.
    """
    response = await react_graph.ainvoke({"messages": messages})
    # Expecting response to be a dict with a 'messages' property (list)
    if isinstance(response, dict) and "messages" in response and response["messages"]:
        return response["messages"][-1].content
    return None

