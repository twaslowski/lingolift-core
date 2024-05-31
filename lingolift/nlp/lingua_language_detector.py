import logging

from lingua import ConfidenceValue, Language, LanguageDetector, LanguageDetectorBuilder
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
        """
        Detects language for the given text. Calculates confidence values for the given languages
        and returns the highest one if it is above a certain threshold.
        The main reason to do this instead of using Lingua's built-in method is to have more control
        and observability.
        :param text: Text for which to detect the language
        :return:
        """
        logging.info(f"Identifying language for the following text: '{text[:30]}'")
        confidence_values = self.detector.compute_language_confidence_values(text)
        logging.info(
            f"Highest confidence values: {[self.stringify_confidence_value(confidence_value) for confidence_value in confidence_values[:3]]}"
        )
        most_probable_language = confidence_values[0]
        if most_probable_language.value < MIN_DISTANCE:
            logging.error(f"Language for not identifiable with sufficient accuracy")
            raise LanguageNotIdentifiedException()
        else:
            return str(most_probable_language.language.iso_code_639_1).split(".")[1]

    @staticmethod
    def stringify_confidence_value(confidence_value: ConfidenceValue):
        return (
            f"{confidence_value.language.name.capitalize()}: {confidence_value.value}"
        )
