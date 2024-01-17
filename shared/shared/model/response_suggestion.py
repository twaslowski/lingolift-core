from pydantic import BaseModel


class ResponseSuggestion(BaseModel):
    suggestion: str
    translation: str


def should_generate_response_suggestions(sentence: str, translation: str) -> bool:
    """
    Response suggestions should generally only be created for questions.
    Interestingly, there isn't a clear-cut way to figure this out – even spaCy doesn't have a straightforward way
    of doing this. This could be solved via an LLM, but for now I want to try approximating this as best as possible.
    :param sentence: The original sentence
    :param translation The translation of the original sentence
    We're looking at both the original sentence and the translation to maximize the amount of hints we can use
    to identify questions.
    # todo a more comprehensive way of doing this could be to search for interrogative phrases,
    potentially using the syntactical analysis of the sentence
    :return: is_question
    """
    return '?' in sentence or '?' in translation
