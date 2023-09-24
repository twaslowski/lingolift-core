import spacy

models = {
    "en": "en_core_web_sm",
    "de": "de_core_news_sm",
    "ru": "ru_core_news_sm"
}


def perform_analysis(sentence: str, language: str):
    language_key = models[language]
    nlp = spacy.load(language_key)
    doc = nlp(sentence)
    return {token.text: {
        "lemma": token.lemma_,
        "morph_analysis": token.morph
    } for token in doc}


if __name__ == '__main__':
    print(perform_analysis("Die schöne Frau geht mit dem Hund spazieren.", "de"))
