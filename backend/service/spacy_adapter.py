import spacy
from dotenv import load_dotenv

models = {
    "german": "de_core_news_sm",
    "russian": "ru_core_news_sm",
    "spanish": "es-core-news-sm",
    "french": "fr-core-news-md",
    "portuguese": "pt-core-news-sm",
}


class LanguageNotAvailableException(Exception):
    pass


def perform_analysis(sentence: str, language: str) -> list[dict]:
    language_key = models.get(language.lower())
    if language_key is None:
        raise LanguageNotAvailableException(f"Language {language} is not available.")
    nlp = spacy.load(language_key)
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
