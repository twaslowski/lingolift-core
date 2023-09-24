from dataclasses import dataclass


@dataclass
class WordTranslation:
    word: str
    translation: str


@dataclass
class LiteralTranslation:
    literal_translation: str
    words: WordTranslation
