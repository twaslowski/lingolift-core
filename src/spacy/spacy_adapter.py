import spacy


models = {
    "en": "en_core_web_sm",
    "de": "de_core_news_sm",
    "ru": "ru_core_news_sm"
}

if __name__ == '__main__':
    nlp = spacy.load(models["en"])
    tokens = nlp("for defective verbs with no infinitive the present tense.")

    for token in tokens:
        print(token.text, token.dep)
