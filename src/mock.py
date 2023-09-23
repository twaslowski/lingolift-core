import logging
import os
import time

import openai
from dotenv import load_dotenv

from flask import Flask, jsonify
from flask_cors import CORS

# setup
load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

# configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

app = Flask(__name__)
CORS(app)


@app.route('/translate', methods=['POST'])
def get_translation():
    time.sleep(1)
    response = {
        "literal_translation": "How is it going with you today?",
        "natural_translation": "How are you doing today?",
        "original_sentence": "Как у тебя сегодня дела?"
    }
    return jsonify(response)


@app.route('/responses', methods=['POST'])
def get_responses():
    time.sleep(3)
    response = {
        "response_suggestions": [
            {
                "suggestion": "У меня все отлично, спасибо! А у тебя?",
                "translation": "I'm doing great, thank you! And you?"
            },
            {
                "suggestion": "Не очень хорошо, но надеюсь, что все наладится. А у тебя как?",
                "translation": "Not very well, but I hope everything will be fine. How about you?"
            }
        ]
    }
    return jsonify(response)


@app.route('/syntactical-analysis', methods=['POST'])
def get_syntactical_analysis():
    time.sleep(7)
    response = {
        "literal_translation": "How is it going with you today?",
        "original_sentence": "Как у тебя сегодня дела?",
        "syntactical_analysis": [
            {
                "grammatical_context": "interrogative pronoun",
                "translation": "How",
                "word": "Как"
            },
            {
                "grammatical_context": "preposition indicating possession",
                "translation": "at",
                "word": "у"
            },
            {
                "grammatical_context": "pronoun indicating possession",
                "translation": "you",
                "word": "тебя"
            },
            {
                "grammatical_context": "adverb indicating time",
                "translation": "today",
                "word": "сегодня"
            },
            {
                "grammatical_context": "noun",
                "translation": "affairs",
                "word": "дела"
            }
        ]
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
