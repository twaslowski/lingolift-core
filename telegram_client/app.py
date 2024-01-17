import asyncio
import logging
import os
from typing import Optional, Union

import telegram.constants
from dotenv import load_dotenv
from shared.client import Client
from shared.exception import ApplicationException
from shared.model.literal_translation import LiteralTranslation
from shared.model.response_suggestion import ResponseSuggestion
from shared.model.syntactical_analysis import SyntacticalAnalysis
from shared.model.translation import Translation
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, Application, CommandHandler, ContextTypes
from telegram.ext import filters as Filters

# setup
load_dotenv()
TOKEN = os.environ.get("TELEGRAM_TOKEN")

# configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


async def handle_text_message(update: Update, _) -> None:
    sentence = update.message.text
    logging.info(f"Received message: {sentence}")
    await reply(update, "Thanks! I've received your sentence, working on the translation now ...", html=False)

    try:
        translation = await client.fetch_translation(sentence)
    except ApplicationException as e:
        await reply(update, f"Sorry, I couldn't translate your sentence: {e.error_message}")
        return

    translation_response = stringify_translation(sentence, translation)
    await reply(update, translation_response)

    await reply(update, "Fetching syntactical analysis for your sentence ...", html=False)

    try:
        # perform all other calls concurrently
        suggestions, literal_translations, syntactical_analysis = await asyncio.gather(
            client.fetch_response_suggestions(sentence),
            client.fetch_literal_translations(sentence),
            client.fetch_syntactical_analysis(sentence, translation.language_code),
            return_exceptions=True
        )

    except ApplicationException as e:
        await reply(update, f"Something went wrong when fetching the syntactical analysis: {e.error_message}")
        return

    analysis_rendered = coalesce_analyses(literal_translations, syntactical_analysis)
    await reply(update, analysis_rendered)
    await reply(update, stringify_suggestions(suggestions))


async def reply(update: Update, message: str, html: bool = True):
    parse_mode = telegram.constants.ParseMode.HTML if html else None
    await update.message.reply_text(message, parse_mode=parse_mode)


def stringify_translation(sentence: str, translation: Translation) -> str:
    return f"<b>'{sentence}'</b> is <b>{translation.language_name}</b> and translates to " \
           f"<b>'{translation.translation}'</b> in English.\n"
    pass


def stringify_suggestions(suggestions: list[ResponseSuggestion]) -> str:
    response_string = "Here are some <b>suggestions</b> for how you could reply:\n"
    for suggestion in suggestions:
        response_string += f"'<i>{suggestion.suggestion}</i>'\n"
        response_string += f"{suggestion.translation}\n\n"
    return response_string


def coalesce_analyses(literal_translations: list[LiteralTranslation],
                      syntactical_analysis: Union[list[SyntacticalAnalysis], ApplicationException]) -> str:
    """
    If both a literal translation of the words in the sentence and the syntactical analysis (i.e. part-of-speech
    tagging) are available, they get coalesced in this function, meaning each word gets displayed alongside its
    translation and its morphological features. If only the literal translation is available, the translations
    are displayed. If neither or only the morphological analysis is available, the function returns an error message.

    ATTENTION: asyncio.gather() can return Exceptions. This way, literal translations can be displayed, even when
    the syntactical-analysis endpoints errors (e.g. due to the language model not being available).
    This object gets passed to find_analysis(), which handles this error.
    # todo this is kind of ugly, is there a better mechanism of handling this?
    :param literal_translations:
    :param syntactical_analysis:
    :return:
    """
    response_string = "<b>Vocabulary and Grammar breakdown</b>\n"
    for word in literal_translations:
        word_analysis = find_analysis(word.word, syntactical_analysis)
        response_string += f"<b>{word.word}</b>: {word.translation}"
        if word_analysis:
            response_string += f"; {word_analysis.stringify()}\n"
        else:
            response_string += "\n"
    return response_string


def find_analysis(word: str, syntactical_analyses: Union[list[SyntacticalAnalysis], ApplicationException]) -> \
        Optional[SyntacticalAnalysis]:
    """
    :param word: Word from the literal translation
    :param syntactical_analyses: Set of syntactical analyses for words in the sentence
    :return: The analysis for the word including the lemma, dependencies and morphology, if available.
    """
    if type(syntactical_analyses) == ApplicationException:
        return None
    for analysis in syntactical_analyses:
        if analysis.word == word and analysis.morphology != '':
            return analysis
    return None


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error("Exception while handling an update:", exc_info=context.error)
    await update.message.reply_text(text="An unexpected error occurred. Sorry :(")


async def introduction_handler(update: Update, _):
    await update.message.reply_text(
        "Welcome! I will provide translations for you if you send me a sentence in a non-English language. Try "
        "texting me something like '¿Donde esta la biblioteca?'")


def init_app() -> Application:
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", introduction_handler))
    app.add_handler(MessageHandler(Filters.TEXT, handle_text_message))
    app.add_error_handler(handle_error)
    return app


if __name__ == '__main__':
    client = Client(protocol="http")
    application = init_app()
    logging.info("Starting application")
    application.run_polling()
