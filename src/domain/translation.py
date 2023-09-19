from dataclasses import dataclass


@dataclass
class Translation:
    natural_translation: str
    literal_translation: str
    original_sentence: str
