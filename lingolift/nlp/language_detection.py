from lingua import Language, LanguageDetectorBuilder
from shared.exception import LanguageNotIdentifiedException

MIN_DISTANCE = 0.6
LANGUAGES = [
    Language.SPANISH,
    Language.GERMAN,
    Language.RUSSIAN,
    Language.FRENCH,
    Language.PORTUGUESE,
]
DETECTOR = (
    LanguageDetectorBuilder.from_languages(*LANGUAGES)
    .with_preloaded_language_models()
    .with_minimum_relative_distance(MIN_DISTANCE)
    .build()
)


def detect_language(sentence: str) -> str:
    language = DETECTOR.detect_language_of(sentence)
    if language is None:
        raise LanguageNotIdentifiedException()
    else:
        return str(language.iso_code_639_1).split(".")[1]
