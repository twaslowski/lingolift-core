from pydantic import BaseModel


class UposExplanation(BaseModel):
    upos_feats: str
    explanation: str
