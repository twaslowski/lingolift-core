import logging
import os

import openai
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

from gpt.gpt_adapter import generate_translation, generate_syntactical_analysis, generate_responses, \
    generate_word_inflections

# setup
load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

# configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

app = Flask(__name__)
CORS(app)


@app.route('/translate', methods=['POST'])
def get_translation():
    sentence = request.json.get('sentence')
    logging.info(f"Received sentence: {sentence}")
    response = generate_translation(sentence)
    return jsonify(response)


@app.route('/responses', methods=['POST'])
def get_responses():
    sentence = request.json.get('sentence')
    number_suggestions = request.json.get('number_suggestions')
    response = generate_responses(sentence, number_suggestions)
    return jsonify(response)


@app.route('/syntactical-analysis', methods=['POST'])
def get_syntactical_analysis():
    sentence = request.json.get('sentence')
    response = generate_syntactical_analysis(sentence)
    return jsonify(response)


@app.route('/inflections', methods=['POST'])
def get_word_inflections():
    word = request.json.get('word')
    language = request.json.get('language')
    context = request.json.get('context')
    response = generate_word_inflections(language, context, word)
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
