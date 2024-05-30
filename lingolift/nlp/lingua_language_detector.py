from lingua import Language, LanguageDetector, LanguageDetectorBuilder
from shared.exception import LanguageNotIdentifiedException

from lingolift.nlp.abstract_language_detector import AbstractLanguageDetector

MIN_DISTANCE = 0.6

DEFAULT_LANGUAGES = [
    Language.SPANISH,
    Language.GERMAN,
    Language.RUSSIAN,
    Language.FRENCH,
    Language.PORTUGUESE,
]

DEFAULT_DETECTOR = (
    LanguageDetectorBuilder.from_languages(*DEFAULT_LANGUAGES)
    .with_preloaded_language_models()
    .with_minimum_relative_distance(MIN_DISTANCE)
    .build()
)


class LinguaLanguageDetector(AbstractLanguageDetector):
    detector: LanguageDetector

    def __init__(self, detector: LanguageDetector = DEFAULT_DETECTOR):
        self.detector = detector

    def detect_language(self, text: str) -> str:
        language = self.detector.detect_language_of(text)
        if language is None:
            raise LanguageNotIdentifiedException()
        else:
            return str(language.iso_code_639_1).split(".")[1]
