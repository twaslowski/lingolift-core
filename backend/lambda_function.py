from service.generate import generate_translation, generate_literal_translations, generate_responses


def translation_handler(event, _):
    sentence = event.get('sentence')
    logging.info(f"Received sentence: {sentence}")
    try:
        response = generate_translation(sentence)
        return response.model_dump()
    except iso639.LanguageNotFoundError:
        return ApplicationException(f"Language for sentence {sentence} could not be identified.").dict(), 400


def response_suggestion_handler(event, _):
    return [r.model_dump() for r in generate_responses(event.get('sentence'))]


def literal_translation_handler(event, _):
    return [r.model_dump() for r in generate_literal_translations(event.get('sentence'))]
