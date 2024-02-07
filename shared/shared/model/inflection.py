from pydantic import BaseModel


class Inflection(BaseModel):
    word: str
    morphology: dict[str, str]


class Inflections(BaseModel):
    """
    Represents a list of inflections for a given word.
    Additionally contains the part-of-speech-tag ['NOUN', 'VERB'] of that word.
    """

    pos: str
    inflections: list[Inflection]
