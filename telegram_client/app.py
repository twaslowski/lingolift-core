import asyncio
import logging
import os

import aiohttp
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, Application
from telegram.ext import filters as Filters

from telegram_client.lingolift_client import get_translation, get_suggestions, get_literal_translation, \
    get_syntactical_analysis

# setup
load_dotenv()
TOKEN = os.environ.get("TELEGRAM_TOKEN")

# configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def format_translation(update: Update, result: dict) -> str:
    return f"'{update.message.text}' is {result['language']} and translates to " \
           f"'{result['translation']}' in English.\n"
    pass


async def send_suggestions(update: Update, result: dict) -> None:
    await update.message.reply_text("Here are some suggestions for how you could reply:")
    for suggestion in result["response_suggestions"]:
        await update.message.reply_text(f"'{suggestion['suggestion']}'\n"
                                        f"This translates to: '{suggestion['translation']}'")


def format_literal_translations(literal_translations: list) -> str:
    result = "Here's what those words mean: \n"
    for word in literal_translations:
        result += f"{word['word']}: {word['translation']}\n"
    return result


async def handle_error(update: Update, _):
    await update.message.reply_text(text="An unexpected error occurred. Sorry :(")


def format_syntax_analysis(syntactical_analysis: dict):
    return syntactical_analysis


async def handle_text_message(update: Update, _) -> None:
    sentence = update.message.text
    logging.info(f"Received message: {sentence}")
    await update.message.reply_text("Thanks! I've received your sentence, working on the translation now ...")

    # get the translation first. this is the most relevant part to the user.
    # it additionally contains information on the source sentence's language, which is required by other API calls
    translation_result = await get_translation(sentence)
    logging.info(f"Got translation from lingolift server: {translation_result}")
    await update.message.reply_text(format_translation(update, translation_result))

    # perform all other calls concurrently
    async with aiohttp.ClientSession() as session:
        language = translation_result['language']
        suggestions, literal_translation, syntactical_analysis = await asyncio.gather(
            asyncio.create_task(get_suggestions(session, sentence)),
            asyncio.create_task(get_literal_translation(session, sentence)),
            asyncio.create_task(get_syntactical_analysis(session, sentence, language)))

    # the current pattern is usually to have a function format a string and to send it here
    # however, in this case, we're sending multiple messages from this function for easier end-user copy/paste
    await send_suggestions(update, suggestions)
    await update.message.reply_text(format_literal_translations(literal_translation))
    await update.message.reply_text(format_syntax_analysis(syntactical_analysis))


def init_app() -> Application:
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(Filters.TEXT, handle_text_message))
    # app.add_error_handler(handle_error)
    return app


if __name__ == '__main__':
    application = init_app()
    logging.info("Starting application")
    application.run_polling()
