from backend.literal_translation import generate_literal_translation
from backend.llm.message import Message, USER, SYSTEM
from backend.llm.gpt_adapter import openai_exchange
from backend.llm.prompts import TRANSLATION_USER_PROMPT, RESPONSES_USER_PROMPT, \
    TRANSLATION_SYSTEM_PROMPT, RESPONSES_SYSTEM_PROMPT
from backend.util.timing import timed


@timed
def generate_translation(sentence: str) -> dict:
    context = [Message(role=SYSTEM, content=TRANSLATION_SYSTEM_PROMPT),
               Message(role=USER, content=TRANSLATION_USER_PROMPT + sentence)]
    response = openai_exchange(context, json_mode=True)
    return response


@timed
def generate_responses(sentence: str, number_suggestions: int = 2) -> dict:
    context = [Message(role=SYSTEM, content=RESPONSES_SYSTEM_PROMPT)]
    prompt = RESPONSES_USER_PROMPT.format(number_suggestions, sentence)
    context.append(Message(role=USER, content=prompt))
    response = openai_exchange(context, json_mode=True)
    return response


@timed
def generate_literal_translations(sentence: str) -> list[dict]:
    return generate_literal_translation(sentence)
