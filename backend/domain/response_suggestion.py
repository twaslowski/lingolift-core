from dataclasses import dataclass


@dataclass
class ResponseSuggestion:
    suggestion: str
    translation: str
