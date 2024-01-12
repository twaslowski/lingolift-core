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


@app.route('/translation', methods=['POST'])
def get_translation():
    time.sleep(1)
    response = {
        "translation": "How is it going with you today?",
        "language": "russian",
    }
    return jsonify(response)


@app.route('/literal-translation', methods=['POST'])
def get_literal_translation():
    time.sleep(2)
    response = {
        "literal_translation":
            {
                "words": [
                    {
                        "translation": "How",
                        "word": "Как"
                    },
                    {
                        "translation": "at",
                        "word": "у"
                    },
                    {
                        "translation": "you",
                        "word": "тебя"
                    },
                    {
                        "translation": "today",
                        "word": "сегодня"
                    },
                    {
                        "translation": "matters",
                        "word": "дела"
                    }
                ]
            }
    }
    return jsonify(response)


@app.route('/response-suggestion', methods=['POST'])
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
    time.sleep(1)
    response = {
        "syntactical_analysis": [
            {
                "word": "Как",
                "lemma": "как",
                "morphology": "",
                "dependencies": "тебя",
            },
            {
                "word": "у",
                "lemma": "у",
                "morphology": "",
                "dependencies": "тебя",
            },
            {
                "word": "тебя",
                "lemma": "тебя",
                "morphology": "Case=Gen|Number=Sing|Person=Second",
                "dependencies": "тебя",
            },
            {
                "word": "сегодня",
                "lemma": "сегодня",
                "morphology": "Degree=Pos",
                "dependencies": "дела",
            },
            {
                "word": "дела",
                "lemma": "дело",
                "morphology": "Animacy=Inan|Case=Gen|Gender=Neut|Number=Sing",
                "dependencies": "тебя",
            },
            {
                "word": "?",
                "lemma": "?",
                "morphology": "",
                "dependencies": "тебя",
            }
        ]
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
