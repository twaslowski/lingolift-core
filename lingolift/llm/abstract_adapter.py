from abc import ABC, abstractmethod

from lingolift.llm.message import Message


class AbstractLLMAdapter(ABC):
    @abstractmethod
    def exchange(
        self, messages: list[Message], model_name: str, json_mode: bool = False
    ) -> dict | str:
        pass

    @staticmethod
    @abstractmethod
    def parse_response(self, gpt_response: str) -> dict:
        pass
