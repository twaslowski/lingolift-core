import logging
import os

import openai
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from shared.model.error import ApplicationError

from service.generate import generate_translation, generate_responses, generate_literal_translations, \
    generate_legible_upos
from service.literal_translation import SentenceTooLongException, LITERAL_TRANSLATION_MAX_UNIQUE_WORDS
from service.spacy_adapter import perform_analysis, LanguageNotAvailableException, models

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
    return jsonify(response.model_dump())


@app.route('/response-suggestion', methods=['POST'])
def get_response_suggestions():
    sentence = request.json.get('sentence')
    # number_suggestions = request.json.get('number_suggestions')
    response = generate_responses(sentence)
    return jsonify([r.model_dump() for r in response])


@app.route('/literal-translation', methods=['POST'])
def get_literal_translation():
    sentence = request.json.get('sentence')
    try:
        response = generate_literal_translations(sentence)
        return jsonify([r.model_dump() for r in response])
    except SentenceTooLongException:
        return jsonify(ApplicationError(error_message=f"Too many unique words for literal translation; maximum words "
                                                      f"{LITERAL_TRANSLATION_MAX_UNIQUE_WORDS}").model_dump()), 400


@app.route('/literal-translation/languages', methods=['GET'])
def get_literal_translation_languages():
    return jsonify(list(models.keys())), 200


@app.route('/syntactical-analysis', methods=['POST'])
def get_syntactical_analysis():
    sentence = request.json.get('sentence')
    language = request.json.get('language')
    try:
        analysis = perform_analysis(sentence, language)
        return jsonify([a.model_dump() for a in analysis])
    except LanguageNotAvailableException as e:
        return jsonify(ApplicationError(error_message=e.error_message).model_dump()), 400


@app.route('/syntactical-analysis/upos-explanation', methods=['POST'])
def get_syntactical_analysis_upos():
    upos = request.json.get('upos_feats')
    word = request.json.get('word')
    if not upos or not word:
        return jsonify(ApplicationError(error_message="Missing required parameter").model_dump()), 400
    response = generate_legible_upos(word, upos)
    return jsonify(response.model_dump())


if __name__ == "__main__":
    app.run(debug=True)
