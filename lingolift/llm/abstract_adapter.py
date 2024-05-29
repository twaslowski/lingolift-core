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
    def parse_response(gpt_response: str) -> dict:
        """
        Parse the response from an LLM.
        Remove potential hallucinations from the response and load the JSON.
        :param gpt_response: the string response from the model
        :return:
        """
