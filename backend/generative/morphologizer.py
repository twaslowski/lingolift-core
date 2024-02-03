from llm.gpt_adapter import openai_exchange
from llm.message import Message
from nlp.syntactical_analysis import extract_relevant_tags

import spacy


def inflect(word: str, morphology: str) -> str:
    prompt = "Inflect the following word according to the CoNNL-U Universal Feature Tags: {}, {}"
    msg = Message(role="user", content=prompt.format(word, morphology))
    return openai_exchange([msg], model_name="ft:gpt-3.5-turbo-1106:tobiorg::8npM4Pcf", json_mode=False)


def get_initial_morphology(word: str) -> str:
    nlp = spacy.load("de_core_news_sm")
    doc = nlp(word)
    token = doc[0]
    return extract_relevant_tags(token)


if __name__ == '__main__':
    tags = get_initial_morphology("Hund")
    print(tags)
