from abc import ABC, abstractmethod

from lingolift.llm.abstract_adapter import AbstractLLMAdapter


class AbstractGenerator(ABC):
    """
    Abstract base class for all generative tasks in the lingolift application.
    """

    llm_adapter: AbstractLLMAdapter

    @abstractmethod
    def __init__(self, llm_adapter: AbstractLLMAdapter):
        self.llm_adapter = llm_adapter
