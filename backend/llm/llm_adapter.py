from enum import Enum

from backend.llm.message import Message


class Adapter(Enum):
    OPENAI = "openai"
    LLAMA = "llama"


def exchange(messages: list[Message], json_mode: bool = False, adapter: Adapter = Adapter.OPENAI):
    match adapter:
        case Adapter.OPENAI:
            pass
        case Adapter.LLAMA:
            pass
    pass
