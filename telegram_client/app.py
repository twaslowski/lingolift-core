import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, Application
from telegram.ext import filters as Filters

from telegram_client.lingolift_client import get_all

# setup
load_dotenv()
TOKEN = os.environ.get("TELEGRAM_TOKEN")

# configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def format_response(update: Update, result: dict) -> str:
    return f"'{update.message.text}' is {result['translation']['language']} and translates to " \
           f"'{result['translation']['translation']}' in English.\n"
    pass


async def send_suggestions(update: Update, result: dict) -> None:
    await update.message.reply_text("Here are some suggestions for how you could reply:")
    for suggestion in result["response_suggestions"]:
        await update.message.reply_text(f"'{suggestion['suggestion']}'\n"
                                        f"This translates to: '{suggestion['translation']}'")


async def handle_text_message(update: Update, _) -> None:
    lingolift_result = await get_all(update.message.text)
    logging.info(f"Got result from lingolift: {lingolift_result}")
    await update.message.reply_text(format_response(update, lingolift_result))
    await send_suggestions(update, lingolift_result['response_suggestions'])


def init_app() -> Application:
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(Filters.TEXT, handle_text_message))
    # app.add_error_handler(handle_error)
    return app


if __name__ == '__main__':
    application = init_app()
    logging.info("Starting application")
    application.run_polling()
