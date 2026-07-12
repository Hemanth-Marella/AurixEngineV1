from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from typing import Annotated
from typing import TypedDict


class State(TypedDict): # ty

    # state = {
    #     "messages": [
    #         HumanMessage("Hi"),
    #         AIMessage("Hello")
    #     ]
    # }
    messages : Annotated[list,add_messages]  # Annotated lets you attach extra information (metadata) to a type.