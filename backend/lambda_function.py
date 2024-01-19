from service.generate import generate_translation, generate_literal_translations, generate_responses


def translation_handler(event, _):
    return generate_translation(event.get('sentence')).model_dump()


def response_suggestion_handler(event, _):
    return [r.model_dump() for r in generate_responses(event.get('sentence'))]


def literal_translation_handler(event, _):
    return [r.model_dump() for r in generate_literal_translations(event.get('sentence'))]
