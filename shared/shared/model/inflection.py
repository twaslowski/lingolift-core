from pydantic import BaseModel


class Inflection(BaseModel):
    word: str
    morphology: dict[str, str]


class Inflections(BaseModel):
    pos: str
    inflections: list[Inflection]
