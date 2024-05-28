from abc import ABC, abstractmethod

from lingolift.llm.gpt_adapter import GPTAdapter


class AbstractGenerator(ABC):
    """
    Abstract base class for all generative tasks in the lingolift application.
    """

    gpt_adapter: GPTAdapter

    @abstractmethod
    def __init__(self, gpt_adapter: GPTAdapter):
        self.gpt_adapter = gpt_adapter
