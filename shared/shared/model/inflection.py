from typing import Union

from pydantic import BaseModel
from shared.model.syntactical_analysis import PartOfSpeech


class Inflection(BaseModel):
    word: str
    morphology: dict[str, str]


class Inflections(BaseModel):
    """
    Represents a list of inflections for a given word.
    Additionally contains the part-of-speech-tag ['NOUN', 'VERB'] of that word.
    """

    pos: PartOfSpeech
    gender: Union[str, None]  # for nouns only
    inflections: list[Inflection]
