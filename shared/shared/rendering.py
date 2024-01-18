from enum import Enum
from typing import Optional

import emoji

from shared.exception import ApplicationException
from shared.model.literal_translation import LiteralTranslation
from shared.model.response_suggestion import ResponseSuggestion
from shared.model.syntactical_analysis import SyntacticalAnalysis
from shared.model.translation import Translation


class MarkupLanguage(Enum):
    MARKDOWN = 'markdown'
    HTML = 'html'


class Stringifier:
    def __init__(self, markup_language: MarkupLanguage):
        self.markup_language = markup_language

    def introductory_text(self) -> str:
        return f"""
        Hi! I'm the Grammr Bot. I will support you in learning a new language  
        {emoji.emojize(':smiling_face_with_open_hands:')}. {self.linebreak()}
        If you send me a sentence in a foreign language, I will ...
        - translate it for you {emoji.emojize(':open_book:')}{self.linebreak()}
        - {self.hyperlink('provide you with some insights into the grammar of the sentence ',
                          'https://universaldependencies.org/format.html#morphological-annotation')}
                          {emoji.emojize(':nerd_face:')}
                          {self.linebreak()}
        - help you respond with some suggestions {emoji.emojize(':pen:')}{self.linebreak()}
        
        Alright, let's get started! Text me something – for example, '¿Donde esta la biblioteca?'.
        """

    def disclaimer(self) -> str:
        return f"""I'm currently under active development. You can
        {self.hyperlink('view my source code on GitHub', 'https://github.com/TobiasWaslowski/lingolift/')} if you want,
        or {self.hyperlink('contact my creator', 'https://www.linkedin.com/in/twaslowski/')}
        if you have any questions or remarks."""

    def coalesce_analyses(self, literal_translations: list[LiteralTranslation],
                          syntactical_analysis: list[SyntacticalAnalysis]) -> str:
        """
        If both a literal translation of the words in the sentence and the syntactical analysis (i.e. part-of-speech
        tagging) are available, they get coalesced in this function, meaning each word gets displayed alongside its
        translation and its morphological features. If only the literal translation is available, the translations
        are displayed. If neither or only the morphological analysis is available, the function returns an error message.
        :param literal_translations:
        :param syntactical_analysis:
        :param ml: Rendering Mode; HTML or Markdown. Different clients may use different modes of displaying information
        :return:
        """
        response_string = self.headline("Vocabulary and Grammar breakdown")
        for word in literal_translations:
            analysis = self.find_analysis(word.word, syntactical_analysis)
            response_string += f"{self.bold(word.word)}: {word.translation}"
            if analysis:
                response_string += f"; {analysis.stringify()}{self.linebreak()}"
            else:
                response_string += self.linebreak()
        return response_string

    @staticmethod
    def find_analysis(word: str, syntactical_analyses: list[SyntacticalAnalysis]) -> \
            Optional[SyntacticalAnalysis]:
        """
        :param word: Word from the literal translation
        :param syntactical_analyses: Set of syntactical analyses for words in the sentence
        :return: The analysis for the word including the lemma, dependencies and morphology, if available.
        """
        if type(syntactical_analyses) == ApplicationException:
            return None
        for analysis in syntactical_analyses:
            if analysis.word == word:
                return analysis
        return None

    def stringify_translation(self, sentence: str, translation: Translation) -> str:
        return f"{self.headline('Translation')}" \
               f"'{self.italic(sentence)}' is {self.italic(translation.language_name.capitalize())} " \
               f"and translates to '{self.italic(translation.translation)}' in English.\n"

    def stringify_suggestions(self, suggestions: list[ResponseSuggestion]) -> str:
        response_string = self.headline("Response suggestions")
        for suggestion in suggestions:
            response_string += f"'{self.italic(suggestion.suggestion)}'\n"
            response_string += f"{suggestion.translation}\n\n"
        return response_string

    def bold(self, text: str) -> str:
        if self.markup_language == MarkupLanguage.MARKDOWN:
            return f"**{text}**"
        elif self.markup_language == MarkupLanguage.HTML:
            return f"<b>{text}</b>"

    def italic(self, text: str) -> str:
        if self.markup_language == MarkupLanguage.MARKDOWN:
            return f"*{text}*"
        elif self.markup_language == MarkupLanguage.HTML:
            return f"<i>{text}</i>"

    def headline(self, text: str) -> str:
        if self.markup_language == MarkupLanguage.MARKDOWN:
            return f"### {text}\n\n"
        elif self.markup_language == MarkupLanguage.HTML:
            # currently only used for telegram client, which does not support <h3> tags or equivalents
            return f"{self.bold(text)}\n"

    def linebreak(self) -> str:
        if self.markup_language == MarkupLanguage.MARKDOWN:
            return "\n\n"
        elif self.markup_language == MarkupLanguage.HTML:
            return "\n"

    def hyperlink(self, text: str, link: str) -> str:
        if self.markup_language == MarkupLanguage.MARKDOWN:
            return f"[{text}]({link})"
        elif self.markup_language == MarkupLanguage.HTML:
            return f"<a href='{link}'>{text}</a>"
