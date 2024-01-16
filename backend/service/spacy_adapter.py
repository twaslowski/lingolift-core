import iso639
import spacy
from dotenv import load_dotenv

models = {
    "DE": "de_core_news_sm",
    "RU": "ru_core_news_sm",
    "ES": "es_core_news_sm",
    "FR": "fr_core_news_md",
    "PT": "pt_core_news_sm",
}


class LanguageNotAvailableException(Exception):
    pass


def perform_analysis(sentence: str, language_iso_code: str) -> list[dict]:
    model = models.get(language_iso_code.upper(), None)
    if model is None:
        # try to throw a readable error message first, fall back on country code when required
        try:
            raise LanguageNotAvailableException(f"Language {iso639.to_name(language_iso_code)} is not available.")
        except iso639.NonExistentLanguageError:
            raise LanguageNotAvailableException(f"Language {language_iso_code} is not available.")
    nlp = spacy.load(model)
    doc = nlp(sentence)
    return [{
        "word": str(token.text),
        "lemma": str(token.lemma_),
        "morphology": str(token.morph),
        "dependencies": str(token.head),
    } for token in doc if str(token.morph) != '']


if __name__ == '__main__':
    load_dotenv()
    print(perform_analysis("Как у тебя сегодня дела?", "russian"))
