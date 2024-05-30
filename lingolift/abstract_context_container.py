import abc
import os

from lingolift.llm.abstract_adapter import AbstractLLMAdapter
from lingolift.llm.openai_adapter import OpenAIAdapter


class AbstractLambdaContextContainer(abc.ABC):
    llm_adapter: AbstractLLMAdapter

    def __init__(self, llm_adapter: AbstractLLMAdapter = None):
        self.llm_adapter = llm_adapter or self.default_openai_adapter()

    @staticmethod
    def default_openai_adapter() -> OpenAIAdapter:
        """
        Creates a default OpenAIAdapter instance.
        Notably, the "NO_KEY_PROVIDED" fallback is used to allow for testing without an API key.
        It defers the error message if the key is not provided to the OpenAIAdapter
        until when the first request is made.
        :return:
        """
        openai_api_key = os.getenv("OPENAI_API_KEY", "NO_KEY_PROVIDED")
        return OpenAIAdapter(openai_api_key)
