from dataclasses import dataclass


@dataclass
class Words:
    word: str
    translation: str


@dataclass
class LiteralTranslation:
    literal_translation: str
    words: list[Words]
