from typing import Iterator

import iso639
import spacy
from shared.model.syntactical_analysis import SyntacticalAnalysis, PartOfSpeech, Morphology
from spacy.tokens.token import Token
from nlp.language_detection import detect_language

from generative.upos import generate_legible_upos

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
    language_code = str(detect_language(sentence))
    nlp = spacy.load(models.get(language_code))
    doc = nlp(sentence)

    for token in doc:
        tags = extract_relevant_tags(token)
        morphology = None
        if token.pos_ == 'PUNCT':
            return
        if tags:
            # morphology_explanation = generate_legible_upos(token.text, '|'.join(tags)).explanation
            morphology = Morphology(tags=tags, explanation="")
        yield SyntacticalAnalysis(
            word=token.text,
            pos=PartOfSpeech(value=token.pos_, explanation=spacy.explain(token.pos_)),
            morphology=morphology,
            lemma=extract_lemma(token),
            dependency=extract_dependency(token)
        )


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
        case 'VERB' | 'AUX':
            relevant_tags = ['Number', 'Person', 'Tense']
        case 'NOUN' | 'DET' | 'ADJ':
            relevant_tags = ['Gender', 'Case', 'Number']
        case _:
            relevant_tags = []
    tags = str(token.morph).split('|')
    return [tag for tag in tags if tag.split('=')[0] in relevant_tags]


if __name__ == '__main__':
    response = list(perform_analysis('Wie viel kostet das Bier?'))
    for r in response:
        print(r.stringify())
