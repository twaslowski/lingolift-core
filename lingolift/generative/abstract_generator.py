from abc import ABC, abstractmethod

from lingolift.llm.gpt_adapter import OpenAIAdapter


class AbstractGenerator(ABC):
    """
    Abstract base class for all generative tasks in the lingolift application.
    """

    gpt_adapter: OpenAIAdapter

    @abstractmethod
    def __init__(self, gpt_adapter: OpenAIAdapter):
        self.gpt_adapter = gpt_adapter
