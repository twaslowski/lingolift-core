import asyncio
import logging
import os

import telegram.constants
from dotenv import load_dotenv
from shared.client import Client
from shared.exception import ApplicationException
from shared.rendering import Stringifier, MarkupLanguage
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, Application, CommandHandler, ContextTypes
from telegram.ext import filters as Filters

# setup
load_dotenv()

# create global-scoped client
protocol = os.environ.get("BACKEND_PROTOCOL")
host = os.environ.get("BACKEND_HOST")
port = os.environ.get("BACKEND_PORT")
client = Client(protocol, host, port)

stringifier = Stringifier(MarkupLanguage.HTML)

# configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

MESSAGE_RECEIVED = "Thanks! I've received your sentence, working on the translation now ..."
TRANSLATION_ERROR = "Sorry, I couldn't translate your sentence: {}"
ANALYSIS_ERROR = "Something went wrong when processing the syntactical analysis: {}"


async def handle_text_message(update: Update, _) -> None:
    sentence = update.message.text
    logging.info(f"Received message: {sentence}")
    await reply(update, MESSAGE_RECEIVED, html=False)

    try:
        translation = await client.fetch_translation(sentence)
    except ApplicationException as e:
        await reply(update, TRANSLATION_ERROR.format(e.error_message))
        return

    translation_response = stringifier.stringify_translation(sentence, translation)
    await reply(update, translation_response)

    await reply(update, "Fetching syntactical analysis for your sentence ...", html=False)

    # perform all other calls concurrently
    suggestions, literal_translations, syntactical_analysis = await gather_calls(sentence, translation)

    if type(literal_translations) is ApplicationException:
        await reply(update, ANALYSIS_ERROR.format(literal_translations.error_message))
        return

    # if literal translation is available; error handling for syntactical analysis is done in find_analysis()
    analysis_rendered = stringifier.coalesce_analyses(literal_translations, syntactical_analysis)
    await reply(update, analysis_rendered)

    if type(suggestions) is ApplicationException:
        await reply(update, ANALYSIS_ERROR.format(suggestions.error_message))
        return

    # else
    await reply(update, stringifier.stringify_suggestions(suggestions))


async def gather_calls(sentence, translation):
    return await asyncio.gather(
        client.fetch_response_suggestions(sentence),
        client.fetch_literal_translations(sentence),
        client.fetch_syntactical_analysis(sentence, translation.language_code),
        return_exceptions=True
    )


async def reply(update: Update, message: str, html: bool = True):
    parse_mode = telegram.constants.ParseMode.HTML if html else None
    await update.message.reply_text(message, parse_mode=parse_mode)


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error("Exception while handling an update:", exc_info=context.error)
    await update.message.reply_text(text="An unexpected error occurred. Sorry :(")


async def introduction_handler(update: Update, _):
    await update.message.reply_text(
        "Welcome! I will provide translations for you if you send me a sentence in a non-English language. "
        "Try texting me something like '¿Donde esta la biblioteca?'")


def init_app() -> Application:
    token = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", introduction_handler))
    app.add_handler(MessageHandler(Filters.TEXT, handle_text_message))
    app.add_error_handler(handle_error)
    return app


if __name__ == '__main__':
    # create app
    application = init_app()
    logging.info("Starting application")
    application.run_polling()
