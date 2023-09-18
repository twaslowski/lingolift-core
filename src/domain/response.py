from dataclasses import dataclass

from src.domain.response_suggestion import ResponseSuggestion
from src.domain.sentence_component import SentenceComponent


@dataclass
class Response:
    summary: str
    sentence_breakdown: list[SentenceComponent]
    response_suggestions: list[ResponseSuggestion]
