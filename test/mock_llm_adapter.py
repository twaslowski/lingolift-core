import json

from lingolift.llm.abstract_adapter import AbstractLLMAdapter
from lingolift.llm.message import Message


class MockLLMAdapter(AbstractLLMAdapter):
    next_response: dict | str

    def exchange(
        self, messages: list[Message], model_name: str, json_mode: bool = False
    ) -> dict | str:
        return self.next_response

    @staticmethod
    def parse_response(gpt_response: str) -> dict:
        return json.loads(gpt_response)

    def next_response(self, response: str | dict) -> None:
        self.next_response = response
