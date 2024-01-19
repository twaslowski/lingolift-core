from service.generate import generate_translation


def translation_handler(event, _):
    return generate_translation(event.get('sentence')).model_dump()

