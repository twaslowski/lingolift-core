from shared.model.upos_explanation import UposExplanation

from llm.gpt_adapter import openai_exchange
from llm.message import Message, USER, SYSTEM
from util.timing import timed


@timed
def generate_legible_upos(word: str, upos_feats: str) -> UposExplanation:
    context = [Message(role=USER, content=LEGIBLE_UPOS_SYSTEM_PROMPT),
               Message(role=SYSTEM, content=LEGIBLE_UPOS_USER_PROMPT.format(upos_feats, word))]
    response = openai_exchange(context)
    response['upos_feats'] = upos_feats
    print(response)
    return UposExplanation(**response)


LEGIBLE_UPOS_SYSTEM_PROMPT = """
Given a word with a set of universal part-of-speech tags, provide a concise, one-sentence explanation of it. 
DO NOT mention a tag, simply explain the morphology of the word. Return your response in the following JSON structure:
{
    "explanation": "PLACEHOLDER_EXPLANATION"
}
"""

LEGIBLE_UPOS_USER_PROMPT = "Explain the universal part-of-speech tag {} for the following word: {}"
