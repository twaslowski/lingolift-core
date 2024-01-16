from pydantic import BaseModel


class SyntacticalAnalysis(BaseModel):
    word: str
    morphology: str
    lemma: str
    pos: str
    pos_explanation: str
