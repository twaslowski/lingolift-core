from lingua import LanguageDetectorBuilder, Language
from shared.exception import ApplicationException

MIN_DISTANCE = 0.7
LANGUAGES = [Language.SPANISH, Language.GERMAN, Language.RUSSIAN, Language.FRENCH, Language.PORTUGUESE]
DETECTOR = (LanguageDetectorBuilder.from_languages(*LANGUAGES)
            .with_preloaded_language_models()
            .with_minimum_relative_distance(MIN_DISTANCE)
            .build())


class LanguageNotAvailableException(ApplicationException):
    pass


def detect_language(sentence: str) -> str:
    language = DETECTOR.detect_language_of(sentence)
    if language is None:
        raise LanguageNotAvailableException(
            f"This language is not supported: p < {MIN_DISTANCE}. Supported languages: {LANGUAGES}")
    else:
        return str(language.iso_code_639_1).split('.')[1]
