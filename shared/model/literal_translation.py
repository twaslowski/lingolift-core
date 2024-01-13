from pydantic import BaseModel


class LiteralTranslation(BaseModel):
    word: str
    translation: str
