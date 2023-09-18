from dataclasses import dataclass


@dataclass
class SentenceComponent:
    word: str
    translation: str
    grammatical_context: str
