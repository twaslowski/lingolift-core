from pydantic import BaseModel


class UposExplanation(BaseModel):
    upos: str
    explanation: str
