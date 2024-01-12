from dataclasses import dataclass


@dataclass
class SentenceComponent:
    text: str
    morph: str
    lemma: str
