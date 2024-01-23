from typing import Iterator

import iso639
import spacy
from shared.exception import ApplicationException
from shared.model.syntactical_analysis import SyntacticalAnalysis, PartOfSpeech, Morphology
from spacy.tokens.token import Token

from generative.upos import generate_legible_upos

models = {
    "DE": "de_core_news_sm",
    "RU": "ru_core_news_sm",
    "ES": "es_core_news_sm",
    "FR": "fr_core_news_md",
    "PT": "pt_core_news_sm",
}


class LanguageNotAvailableException(ApplicationException):
    pass


def perform_analysis(sentence: str, language_iso_code: str) -> Iterator[SyntacticalAnalysis]:
    """
    Performs a syntactical analysis on a sentence in a given language.
    :param sentence: Source sentence
    :param language_iso_code: The ISO-639-1 code of the language to analyze, in order to load a model.
    :return:
    """
    model = models.get(language_iso_code.upper(), None)
    if model is None:
        raise_language_not_available_exception(language_iso_code)
    nlp = spacy.load(model)
    doc = nlp(sentence)

    for token in doc:
        tags = extract_relevant_tags(token)
        morphology = None
        if token.pos_ == 'PUNCT':
            return
        if tags:
            morphology_explanation = generate_legible_upos(token.text, '|'.join(tags)).explanation
            morphology = Morphology(tags=tags, explanation=morphology_explanation)
        yield SyntacticalAnalysis(
            word=token.text,
            pos=PartOfSpeech(value=token.pos_, explanation=spacy.explain(token.pos_)),
            morphology=morphology,
            lemma=extract_lemma(token),
            dependency=extract_dependency(token)
        )


def raise_language_not_available_exception(language_iso_code: str):
    # Try to throw a readable error first (with the whole language name)
    # If the country code is entirely invalid, include it in the error message instead
    try:
        raise LanguageNotAvailableException(
            f"Language {iso639.Language.from_part1(language_iso_code)} is not available.")
    except iso639.LanguageNotFoundError:
        raise LanguageNotAvailableException(f"Language {language_iso_code} is not available.")


def extract_dependency(token: Token) -> str | None:
    if ancestors := list(token.ancestors):
        return ancestors[0].text
    else:
        return None


def extract_lemma(token: Token) -> str | None:
    return token.lemma_ if token.text.lower() != token.lemma_.lower() else None


def extract_relevant_tags(token: Token) -> list[str]:
    """
    Extracts the relevant tags from a set of UPOS tags.
    Not all tags are equally relevant to the end-user; for example, Number, Person and Tense are substantially more
    helpful than the Mood or the VerbForm. This also helps narrow down the problem and allows an incremental
    approach to this complex issue.
    :param token: A spaCy token.
    :return: The relevant tags.
    """
    match token.pos_:
        case 'VERB':
            relevant_tags = ['Number', 'Person', 'Tense']
        case 'NOUN' | 'DET' | 'ADJ':
            relevant_tags = ['Gender', 'Case', 'Number']
        case _:
            relevant_tags = []
    tags = str(token.morph).split('|')
    return [tag for tag in tags if tag.split('=')[0] in relevant_tags]


if __name__ == '__main__':
    response = list(perform_analysis('Wie viel kostet das Bier?', 'DE'))
    for r in response:
        print(r.stringify())
