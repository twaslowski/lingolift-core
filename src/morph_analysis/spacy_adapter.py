import spacy
from dotenv import load_dotenv

models = {
    "en": "en_core_web_sm",
    "de": "de_core_news_sm",
    "ru": "ru_core_news_sm"
}


def perform_analysis(sentence: str, language: str) -> dict:
    language_key = models[language]
    nlp = spacy.load(language_key)
    doc = nlp(sentence)
    return {"sentence": sentence,
            "literal_translation": "Как у тебя сегодня дела?",
            "morph_analysis":
                [{
                    "word": str(token.text),
                    "lemma": str(token.lemma_),
                    "morph_analysis": str(token.morph),
                    "dependencies": str(token.head),
                    # "translation": str(parent.translate_word(token.text))
                }
                    for token in doc]
            }


if __name__ == '__main__':
    load_dotenv()
    print(perform_analysis("Как у тебя сегодня дела?", "ru"))
