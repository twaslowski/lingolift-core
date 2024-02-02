from llm.gpt_adapter import openai_exchange
from llm.message import Message


def inflect(word: str, morphology: str) -> str:
    prompt = "Inflect the following word according to the CoNNL-U Universal Feature Tags: {}, {}"
    msg = Message(role="user", content=prompt.format(word, morphology))
    return openai_exchange([msg], model_name="ft:gpt-3.5-turbo-1106:tobiorg::8npM4Pcf", json_mode=False)


if __name__ == '__main__':
    inflect("gehen", "Number=Sing|Person=2|Tense=Presf")
