import logging

from flask import Flask, jsonify, request
from flask_cors import CORS

from generative.translation import generate_translation
from generative.response_suggestion import generate_response_suggestions
from generative.literal_translation import generate_literal_translation
from shared.exception import LanguageNotAvailableException, SentenceTooLongException
from nlp.syntactical_analysis import perform_analysis
from nlp.morphologizer import retrieve_all_inflections

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
    response = generate_response_suggestions(sentence)
    return jsonify([r.model_dump() for r in response])


@app.route('/literal-translation', methods=['POST'])
def get_literal_translation():
    sentence = request.json.get('sentence')
    try:
        response = generate_literal_translation(sentence)
        return jsonify([r.model_dump() for r in response])
    except SentenceTooLongException as e:
        return jsonify(e.dict()), 400


@app.route('/syntactical-analysis', methods=['POST'])
def get_syntactical_analysis():
    sentence = request.json.get('sentence')
    try:
        analysis = perform_analysis(sentence)
        return jsonify([a.model_dump() for a in analysis])
    except LanguageNotAvailableException as e:
        return jsonify(e.dict()), 400


@app.route('/inflection', methods=['POST'])
def get_inflections():
    word = request.json.get('word')
    inflections = retrieve_all_inflections(word)
    return jsonify([i.model_dump() for i in inflections])


@app.route('/health', methods=['GET'])
def get_health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(debug=True)
