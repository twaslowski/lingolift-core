import logging
import os
import time

import openai
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from shared.model.literal_translation import LiteralTranslation
from shared.model.response_suggestion import ResponseSuggestion
from shared.model.syntactical_analysis import SyntacticalAnalysis
from shared.model.translation import Translation

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
        "language_name": "russian",
        "language_code": "RU"
    }
    translation = Translation(**response)
    return jsonify(translation.model_dump())


@app.route('/literal-translation', methods=['POST'])
def get_literal_translation():
    time.sleep(2)
    response = [
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
    literal_translations = [LiteralTranslation(**literal_translation) for literal_translation in response]
    return jsonify([literal_translation.model_dump() for literal_translation in literal_translations])


@app.route('/response-suggestion', methods=['POST'])
def get_responses():
    time.sleep(3)
    response = [
        {
            "suggestion": "У меня все отлично, спасибо! А у тебя?",
            "translation": "I'm doing great, thank you! And you?"
        },
        {
            "suggestion": "Не очень хорошо, но надеюсь, что все наладится. А у тебя как?",
            "translation": "Not very well, but I hope everything will be fine. How about you?"
        }
    ]
    suggestions = [ResponseSuggestion(**suggestion) for suggestion in response]
    return jsonify([suggestion.model_dump() for suggestion in suggestions])


@app.route('/syntactical-analysis', methods=['POST'])
def get_syntactical_analysis():
    time.sleep(1)
    response = [{'word': 'Как', 'morphology': '', 'lemma': 'как', 'pos': 'SCONJ', 'dependency': 'тебя',
                 'pos_explanation': 'Subordinating conjunction'},
                {'word': 'у', 'morphology': '', 'lemma': 'у', 'pos': 'ADP', 'dependency': 'тебя',
                 'pos_explanation': 'Adposition'},
                {'word': 'тебя', 'morphology': 'Case=Gen|Number=Sing|Person=Second', 'lemma': 'тебя', 'pos': 'PRON',
                 'dependency': '', 'pos_explanation': 'Pronoun'},
                {'word': 'сегодня', 'morphology': 'Degree=Pos', 'lemma': 'сегодня', 'pos': 'ADV', 'dependency': 'дела',
                 'pos_explanation': 'Adverb'},
                {'word': 'дела', 'morphology': 'Animacy=Inan|Case=Gen|Gender=Neut|Number=Sing', 'lemma': 'дело',
                 'pos': 'NOUN', 'dependency': 'тебя', 'pos_explanation': 'Noun'},
                {'word': '?', 'morphology': '', 'lemma': '?', 'pos': 'PUNCT', 'dependency': 'тебя',
                 'pos_explanation': 'Punctuation'}]
    analysis = [SyntacticalAnalysis(**syntactical_analysis) for syntactical_analysis in response]
    return jsonify([syntactical_analysis.model_dump() for syntactical_analysis in analysis])


@app.route('/health', methods=['GET'])
def get_health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(debug=True)
