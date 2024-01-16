import iso639
import spacy
from dotenv import load_dotenv

from shared.model.syntactical_analysis import SyntacticalAnalysis

models = {
    "DE": "de_core_news_sm",
    "RU": "ru_core_news_sm",
    "ES": "es_core_news_sm",
    "FR": "fr_core_news_md",
    "PT": "pt_core_news_sm",
}


class LanguageNotAvailableException(Exception):
    error_message: str

    def __init__(self, error_message: str):
        self.error_message = error_message


def perform_analysis(sentence: str, language_iso_code: str) -> list[SyntacticalAnalysis]:
    model = models.get(language_iso_code.upper(), None)
    if model is None:
        # try to throw a readable error message first, fall back on country code when required
        try:
            raise LanguageNotAvailableException(f"Language {iso639.to_name(language_iso_code)} is not available.")
        except iso639.NonExistentLanguageError:
            raise LanguageNotAvailableException(f"Language {language_iso_code} is not available.")
    nlp = spacy.load(model)
    doc = nlp(sentence)

    # this is honestly kind of hacky because it doesn't allow for any elegant validation logic;
    # inlining everything may not be sustainable in the long run
    return [SyntacticalAnalysis(
        word=str(token.text),
        lemma=str(token.lemma_),
        morphology=str(token.morph),
        pos=str(token.pos_),
        pos_explanation=str(spacy.explain(token.pos_)).capitalize(),
        dependency=str([a.text for a in token.ancestors][0]) if [a.text for a in token.ancestors] else ""
    ) for token in doc]


if __name__ == '__main__':
    load_dotenv()
    print([a.model_dump() for a in perform_analysis("Как у тебя сегодня дела?", "RU")])
