import os

import spacy
from shared.model.token.token import Token
import shared.model.token.mapper as mapper
from shared.model.token.upos import UPOS


def perform_analysis(sentence: str) -> list[Token]:
    """
    Performs a syntactical analysis on a sentence in a given language.
    :param sentence: source sentence
    :return: a list of domain-specific well-structured Token objects that represent a subset of the spaCy token objects
    """
    nlp = spacy.load(os.getenv("SPACY_MODEL"))
    doc = nlp(sentence)
    tokens = mapper.from_spacy_doc(doc)
    return [token for token in tokens if token.upos != UPOS.PUNCT]
