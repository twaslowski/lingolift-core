from typing import Iterator

import nlp.universal_features as universal_features
import spacy
from shared.model.syntactical_analysis import SyntacticalAnalysis, PartOfSpeech, Morphology
from spacy.tokens.token import Token
from nlp.language_detection import llm_detect_language

models = {
    "DE": "de_core_news_sm",
    "RU": "ru_core_news_sm",
    "ES": "es_core_news_sm",
    "FR": "fr_core_news_md",
    "PT": "pt_core_news_sm",
}


def perform_analysis(sentence: str) -> Iterator[SyntacticalAnalysis]:
    """
    Performs a syntactical analysis on a sentence in a given language.
    :param sentence: Source sentence
    :param language_iso_code: The ISO-639-1 code of the language to analyze, in order to load a model.
    :return:
    """
    language_code = str(llm_detect_language(sentence))
    nlp = spacy.load(models.get(language_code))
    doc = nlp(sentence)

    for token in doc:
        tags = pos_tags_to_dict(token)
        morphology = None
        if token.pos_ == 'PUNCT':
            return
        if tags:
            morphology = Morphology(tags=tags_dict_to_list(tags),
                                    explanation=convert_to_legible_features(tags, token))
        yield SyntacticalAnalysis(
            word=token.text,
            pos=PartOfSpeech(value=token.pos_, explanation=spacy.explain(token.pos_)),
            morphology=morphology,
            lemma=extract_lemma(token),
            dependency=extract_dependency(token)
        )


def convert_to_legible_features(tags: dict, token: Token) -> str:
    """
    Converts the Universal Feature tags to a legible format.
    :param tags: A list of Universal Feature tags.
    :param token: A spaCy token.
    :return: A legible format of the Universal Feature tags.
    """
    match token.pos_:
        case 'VERB' | 'AUX':
            return universal_features.convert_to_legible_tags(tags, universal_features.VERBAL_FEATURES)
        case 'NOUN' | 'DET' | 'ADJ':
            return universal_features.convert_to_legible_tags(tags, universal_features.NOMINAL_FEATURES)
        case _:
            return ''


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
    tags = str(token.morph).split('|')
    return {
        tag.split('=')[0]: tag.split('=')[1] for tag in tags if tag != ''
    }


def tags_dict_to_list(tags: dict[str, str]) -> list[str]:
    """
    Converts a dictionary of tags to a list of strings.
    This exists for backwards compatibility so I don't have to rewrite the whole shared Morphology structure
    right now. Will be refactored at a later point in time.
    :param tags: A dictionary of tags.
    :return: A list of strings.
    """
    return [f"{k}={v}" for k, v in tags.items()]


if __name__ == '__main__':
    response = list(perform_analysis('Wie viel kostet das Bier?'))
    for r in response:
        print(r.stringify())
