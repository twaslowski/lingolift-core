import logging
import sys

import click

from lingolift.nlp.lingua_language_detector import LinguaLanguageDetector

"""
Collection of convenient CLI utilities, primarily around the natural language processing capabilities
of the lingolift application.
"""


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", stream=sys.stdout
)
logging.getLogger().setLevel(logging.INFO)


@click.command()
@click.option("--text", help="Text to analyze.")
def detect_language(text: str):
    """
    Detect language for an arbitrary text.
    """
    detector = LinguaLanguageDetector()
    detector.detect_language(text)
