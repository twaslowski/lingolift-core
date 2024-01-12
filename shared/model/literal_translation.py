from pydantic import BaseModel


class Words(BaseModel):
    word: str
    translation: str


class LiteralTranslation(BaseModel):
    literal_translations: list[Words]
