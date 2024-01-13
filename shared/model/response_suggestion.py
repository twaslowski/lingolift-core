from pydantic import BaseModel


class ResponseSuggestion(BaseModel):
    suggestion: str
    translation: str

class Suggestions(BaseModel):
    response_suggestions: list[ResponseSuggestion]