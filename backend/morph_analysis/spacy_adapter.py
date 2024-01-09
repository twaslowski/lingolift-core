import spacy
from dotenv import load_dotenv

models = {
    "english": "en_core_web_md",
    "german": "de_core_news_sm",
    "russian": "ru_core_news_sm"
}


def perform_analysis(sentence: str, language: str) -> list[dict]:
    language_key = models[language.lower()]
    nlp = spacy.load(language_key)
    doc = nlp(sentence)
    return [{
        "word": str(token.text),
        "lemma": str(token.lemma_),
        "morph_analysis": str(token.morph),
        "dependencies": str(token.head),
    } for token in doc if str(token.morph) != '']


if __name__ == '__main__':
    load_dotenv()
    print(perform_analysis("Как у тебя сегодня дела?", "russian"))
