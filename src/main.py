import logging
import os

import openai
from dotenv import load_dotenv

from src.gpt.gpt_adapter import chat_completion
from src.gpt.message import Message, SYSTEM
from src.gpt.prompts import SYSTEM_PROMPT

from flask import Flask, jsonify
from flask_cors import CORS

# setup
load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

# configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

app = Flask(__name__)
CORS(app)


@app.route('/translate', methods=['GET'])
def get_translation():
    data = {
        "original_sentence": "Как у тебя сегодня дела?",
        "summary": "How are you doing today?",
        "sentence_breakdown": [
            {
                "word": "Как",
                "translation": "How",
                "grammatical_context": "Interrogative pronoun"
            },
            {
                "word": "у",
                "translation": "with",
                "grammatical_context": "Preposition indicating possession"
            },
            {
                "word": "тебя",
                "translation": "you",
                "grammatical_context": "Pronoun in genitive case"
            },
            {
                "word": "сегодня",
                "translation": "today",
                "grammatical_context": "Adverb of time"
            },
            {
                "word": "дела",
                "translation": "affairs, things",
                "grammatical_context": "Noun in plural form"
            }
        ],
        "response_suggestions": [
            {
                "response": "У меня все хорошо, спасибо!",
                "translation": "I'm doing well, thank you!"
            },
            {
                "response": "Не очень, но я стараюсь.",
                "translation": "Not great, but I'm trying."
            }
        ]

    }
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
