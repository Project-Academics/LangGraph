import base64
import os
import dotenv
dotenv.load_dotenv()

from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage, AIMessage

class Output(TypedDict):
    text: str

class Input(TypedDict):
    file_content: str

class State(Output, Input):
    pass  # or bytes, depending on use case

graph_builder = StateGraph(State, output=Output, input=Input)

llm = init_chat_model("google_genai:gemini-2.0-flash", disable_streaming=True)

def chatbot(state: State) -> Output:
    image_data = state["file_content"]

    message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Transcribe what's in the image:",
            },
            {
                "type": "image",
                "source_type": "base64",
                "data": image_data,
                "mime_type": "image/jpeg",
            },
        ],
    }

    result = llm.invoke([message]).text()
    print(result)

    return {"text": result}

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
# graph_builder.set_finish_point("chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile() 