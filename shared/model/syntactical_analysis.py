from pydantic import BaseModel

class SyntacticalAnalysis(BaseModel):
    text: str
    morphology: str
    lemma: str
