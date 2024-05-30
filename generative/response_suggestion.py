from shared.model.response_suggestion import ResponseSuggestion

from lingolift.generative.abstract_generator import AbstractGenerator
from lingolift.llm.abstract_adapter import AbstractLLMAdapter
from lingolift.llm.message import SYSTEM, USER, Message


class ResponseSuggestionGenerator(AbstractGenerator):
    def __init__(self, llm_adapter: AbstractLLMAdapter):
        super().__init__(llm_adapter)

    def generate_response_suggestions(
        self, sentence: str, number_suggestions: int = 2
    ) -> list[ResponseSuggestion]:
        context = [Message(role=SYSTEM, content=RESPONSE_SUGGESTIONS_SYSTEM_PROMPT)]
        prompt = RESPONSE_SUGGESTIONS_USER_PROMPT.format(number_suggestions, sentence)
        context.append(Message(role=USER, content=prompt))
        response = self.llm_adapter.parse_response(
            self.llm_adapter.exchange(context, json_mode=True, model_name="gpt-4o")
        )
        return [
            ResponseSuggestion(**suggestion)
            for suggestion in response["response_suggestions"]
        ]


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
