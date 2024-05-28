import logging
import os
from asyncio import create_task

import telegram.constants
from dotenv import load_dotenv
from shared.client import Client
from shared.exception import ApplicationException
from shared.rendering import MarkupLanguage, Stringifier
from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
)
from telegram.ext import filters as Filters

# setup
load_dotenv()

# create global-scoped client
host = os.environ.get("API_GATEWAY_HOST")
client = Client(host)

stringifier = Stringifier(MarkupLanguage.HTML)

# configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

MESSAGE_RECEIVED = (
    "Thanks! I've received your sentence, working on the translation now ..."
)


async def handle_text_message(update: Update, _) -> None:
    sentence = update.message.text
    logging.info(f"Received message: {sentence}")
    try:
        await reply(update, MESSAGE_RECEIVED, html=False)

        # send all requests to lingolift
        translation_future = create_task(client.fetch_translation(sentence))
        syntactical_translations_future = create_task(
            client.fetch_syntactical_analysis(sentence)
        )
        literal_translations_future = create_task(
            client.fetch_literal_translations(sentence)
        )

        # receive and send translation
        translation = await translation_future
        translation_response = stringifier.stringify_translation(sentence, translation)
        await reply(update, translation_response)

        # fetch analysis and literal translations
        analysis = await syntactical_translations_future
        literal_translation = await literal_translations_future
        analysis_rendered = stringifier.coalesce_analyses(literal_translation, analysis)
        logging.info(f"Finished rendering analysis for sentence {sentence}")
        await reply(update, analysis_rendered)
    except ApplicationException as e:
        await reply(update, e.error_message)
        return
    except Exception as e:
        logging.error(f"error occurred: {e}")
        await reply(update, "An unexpected error occurred.")


async def reply(update: Update, message: str, html: bool = True):
    parse_mode = telegram.constants.ParseMode.HTML if html else None
    await update.message.reply_text(message, parse_mode=parse_mode)


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error("Exception while handling an update:", exc_info=context.error)
    await update.message.reply_text(text="An unexpected error occurred. Sorry :(")


async def introduction_handler(update: Update, _):
    await update.message.reply_text(
        "Welcome! I will provide translations for you if you send me a sentence in a non-English language. "
        "Try texting me something like '¿Donde esta la biblioteca?'"
    )


def init_app() -> Application:
    token = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", introduction_handler))
    app.add_handler(MessageHandler(Filters.TEXT, handle_text_message))
    app.add_error_handler(handle_error)
    return app


if __name__ == "__main__":
    # create app
    application = init_app()
    logging.info("Starting application")
    application.run_polling()
