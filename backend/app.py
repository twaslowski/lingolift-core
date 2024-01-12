import logging
import os

import openai
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.service.generate import generate_translation, generate_responses, generate_literal_translations
from backend.service.literal_translation import SentenceTooLongException
from backend.service.spacy_adapter import perform_analysis, LanguageNotAvailableException

# setup
load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

# configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

app = Flask(__name__)
CORS(app)


@app.route('/translation', methods=['POST'])
def get_translation():
    sentence = request.json.get('sentence')
    logging.info(f"Received sentence: {sentence}")
    response = generate_translation(sentence)
    return jsonify(response)


@app.route('/response-suggestion', methods=['POST'])
def get_responses():
    sentence = request.json.get('sentence')
    # number_suggestions = request.json.get('number_suggestions')
    response = generate_responses(sentence)
    return jsonify(response)


@app.route('/literal-translation', methods=['POST'])
def get_literal_translation():
    sentence = request.json.get('sentence')
    try:
        response = generate_literal_translations(sentence)
        return jsonify(response)
    except SentenceTooLongException:
        return jsonify({'error': 'There are too many unique words in the translated sentence.'}), 400


@app.route('/syntactical-analysis', methods=['POST'])
def get_syntactical_analysis():
    sentence = request.json.get('sentence')
    language = request.json.get('language')
    try:
        analysis = perform_analysis(sentence, language)
        return jsonify(analysis)
    except LanguageNotAvailableException:
        return jsonify({'error': 'Grammatical analysis is not available for this language.'}), 400


if __name__ == "__main__":
    app.run(debug=True)
