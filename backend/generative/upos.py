from shared.model.upos_explanation import UposExplanation

from llm.gpt_adapter import openai_exchange
from llm.message import Message, USER, SYSTEM
from util.timing import timed

"""
NOTE: This class is technically not required. This could probably be solved without LLM usage as well;
however, taking into account different grammatical rules of different languages would make this very hard
and require more in-depth linguistic knowledge. This is a bit of a shortcut, but it'll help iterating faster.
"""

LEGIBLE_UPOS_SYSTEM_PROMPT = """
Convert a set of CoNNL-U tags into a human-readable text.
For example, the tag Case=Acc|Gender=Masc|Number=Sing should be converted to: "Accusative Singular, Masculine".
Return the converted text as a JSON object with the key "explanation". Example:
{"explanation": "Accusative Singular, Masculine"}
"""

LEGIBLE_UPOS_USER_PROMPT = "Explain the CoNNL-U tag {} for the following word: {}"


@timed
def generate_legible_upos(word: str, upos_feats: str) -> UposExplanation:
    context = [Message(role=USER, content=LEGIBLE_UPOS_SYSTEM_PROMPT),
               Message(role=SYSTEM, content=LEGIBLE_UPOS_USER_PROMPT.format(upos_feats, word))]
    response = openai_exchange(context)
    response['upos_feats'] = upos_feats
    return UposExplanation(**response)
