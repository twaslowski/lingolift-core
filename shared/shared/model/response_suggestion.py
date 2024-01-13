from pydantic import BaseModel


class ResponseSuggestion(BaseModel):
    suggestion: str
    translation: str
