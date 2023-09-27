from dataclasses import dataclass


@dataclass
class Words:
    word: str
    translation: str


@dataclass
class LiteralTranslation:
    words: list[Words]
