from shared.exception import LanguageNotAvailableException

import shared.universal_features as universal_features
import spacy
from shared.model.syntactical_analysis import (
    SyntacticalAnalysis,
    PartOfSpeech,
    Morphology,
)
from spacy.tokens.token import Token
from nlp.language_detection import llm_detect_language

from typing import Optional

models = {
    "DE": "de_core_news_sm",
    "RU": "ru_core_news_sm",
    "ES": "es_core_news_sm",
    "FR": "fr_core_news_md",
    "PT": "pt_core_news_sm",
}


def perform_analysis(
    sentence: str, language_code: Optional[str] = None
) -> list[SyntacticalAnalysis]:
    """
    Performs a syntactical analysis on a sentence in a given language.
    :param language_code: Can optionally be supplied to override the language detection.
    :param sentence: Source sentence
    :return:
    """
    if not language_code:
        language_code = str(llm_detect_language(sentence))
    try:
        model = models[language_code]
        nlp = spacy.load(model)
    except KeyError:
        raise LanguageNotAvailableException()
    doc = nlp(sentence)

    return [_analyze_token(token) for token in doc if _analyze_token(token) is not None]


def _analyze_token(token: Token) -> SyntacticalAnalysis | None:
    tags = pos_tags_to_dict(token)
    morphology = None
    if token.pos_ == "PUNCT":
        return None
    if tags:
        morphology = Morphology(
            tags=tags, explanation=convert_to_legible_features(tags, token)
        )
    return SyntacticalAnalysis(
        word=token.text,
        pos=PartOfSpeech(value=token.pos_, explanation=spacy.explain(token.pos_)),
        morphology=morphology,
        lemma=extract_lemma(token),
        dependency=extract_dependency(token),
    )


def convert_to_legible_features(tags: dict, token: Token) -> str:
    """
    Converts the Universal Feature tags to a legible format.
    :param tags: A list of Universal Feature tags.
    :param token: A spaCy token.
    :return: A legible format of the Universal Feature tags.
    """
    match token.pos_:
        case "VERB" | "AUX":
            return universal_features.convert_to_legible_tags(
                tags, universal_features.verbal_features
            )
        # Add PRON; in German, articles are referred to as Demonstrativpronomen, which sometimes is categorized as PRON
        case "NOUN" | "DET" | "PRON" | "ADJ":
            return universal_features.convert_to_legible_tags(
                tags, universal_features.nominal_features
            )
        case _:
            return ""


def extract_dependency(token: Token) -> str | None:
    if ancestors := list(token.ancestors):
        return ancestors[0].text
    else:
        return None


def extract_lemma(token: Token) -> str | None:
    return token.lemma_ if token.text.lower() != token.lemma_.lower() else None


def pos_tags_to_dict(token: Token) -> dict[str, str]:
    """
    Extracts a dict of features from the PoS tags of a Token.
    :param token: A spaCy token.
    :return: The features, e.g. {'Case': 'Nom', 'Number': 'Plur'}
    """
    tags = str(token.morph).split("|")
    return {tag.split("=")[0]: tag.split("=")[1] for tag in tags if tag != ""}


if __name__ == "__main__":
    response = list(perform_analysis("Das ist ein Test."))
    for r in response:
        print(r.stringify())
