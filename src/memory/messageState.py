from langgraph.graph import START, MessagesState, StateGraph
from typing_extensions import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict
from typing import Sequence

class ChatState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    individual_context: str
    emotional_context: str
    theoretical_context: str



