from shared.model.response_suggestion import ResponseSuggestion

from llm.gpt_adapter import openai_exchange, parse_response
from llm.message import USER, SYSTEM, Message


def generate_response_suggestions(sentence: str, number_suggestions: int = 2) -> list[ResponseSuggestion]:
    context = [Message(role=SYSTEM, content=RESPONSE_SUGGESTIONS_SYSTEM_PROMPT)]
    prompt = RESPONSE_SUGGESTIONS_USER_PROMPT.format(number_suggestions, sentence)
    context.append(Message(role=USER, content=prompt))
    response = parse_response(openai_exchange(context, json_mode=True))
    return [ResponseSuggestion(**suggestion) for suggestion in response['response_suggestions']]


RESPONSE_SUGGESTIONS_SYSTEM_PROMPT = """
Generate response-suggestions for sentences in other languages. 
Provide an English translation for each potential response in the following JSON structure:
{
  "response_suggestions": [
    {
      "suggestion": "one possible response to the sentence",
      "translation": "a translation of this response"
    },
    {
      "suggestion": "another possible response to the sentence",
      "translation": "a translation of this response"
    }
  ]
}
"""

RESPONSE_SUGGESTIONS_USER_PROMPT = """
Suggest {} response-suggestions for the following sentence: {} 
"""
