from abc import ABC, abstractmethod


class AbstractLanguageDetector(ABC):
    @abstractmethod
    def detect_language(self, text: str) -> str:
        pass
