import iso639
from shared.model.literal_translation import LiteralTranslation
from shared.model.response_suggestion import ResponseSuggestion
from shared.model.translation import Translation
from shared.model.upos_explanation import UposExplanation

from llm.gpt_adapter import openai_exchange
from llm.message import Message, USER, SYSTEM
from llm.prompts import TRANSLATION_USER_PROMPT, RESPONSES_USER_PROMPT, \
    TRANSLATION_SYSTEM_PROMPT, RESPONSES_SYSTEM_PROMPT, LEGIBLE_UPOS_SYSTEM_PROMPT, LEGIBLE_UPOS_USER_PROMPT
from service.literal_translation import generate_literal_translation
from util.timing import timed


@timed
def generate_translation(sentence: str) -> Translation:
    context = [Message(role=SYSTEM, content=TRANSLATION_SYSTEM_PROMPT),
               Message(role=USER, content=TRANSLATION_USER_PROMPT + sentence)]
    response = openai_exchange(context, json_mode=True)
    response['language_name'] = iso639.to_name(response['language_code'])
    return Translation(**response)


@timed
def generate_responses(sentence: str, number_suggestions: int = 2) -> list[ResponseSuggestion]:
    context = [Message(role=SYSTEM, content=RESPONSES_SYSTEM_PROMPT)]
    prompt = RESPONSES_USER_PROMPT.format(number_suggestions, sentence)
    context.append(Message(role=USER, content=prompt))
    response = openai_exchange(context, json_mode=True)
    return [ResponseSuggestion(**suggestion) for suggestion in response['response_suggestions']]


@timed
def generate_literal_translations(sentence: str) -> list[LiteralTranslation]:
    return generate_literal_translation(sentence)


@timed
def generate_legible_upos(word: str, upos_feats: str) -> UposExplanation:
    context = [Message(role=USER, content=LEGIBLE_UPOS_SYSTEM_PROMPT),
               Message(role=SYSTEM, content=LEGIBLE_UPOS_USER_PROMPT.format(upos_feats, word))]
    response = openai_exchange(context)
    response['upos_feats'] = upos_feats
    print(response)
    return UposExplanation(**response)
