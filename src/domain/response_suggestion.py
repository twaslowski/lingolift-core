from dataclasses import dataclass


@dataclass
class ResponseSuggestion:
    response: str
    translation: str
