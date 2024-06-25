import json
import logging
from typing import Tuple

from flask import Flask, jsonify, request
from flask_cors import CORS

from lingolift.core_lambda_handlers import (
    literal_translation_handler,
    response_suggestion_handler,
    translation_handler,
)
from lingolift.nlp_lambda_handlers import (
    syntactical_analysis_handler,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

app = Flask(__name__)
CORS(app)

"""
This defines a simple Flask server that provides a wrapper around the core Lambda handlers.
It emulates the API Gateway and Lambda integration, allowing for local testing of the frontend.
"""


@app.route("/translation", methods=["POST"])
def get_translation():
    sentence = request.json.get("sentence")
    lambda_body = create_lambda_event({"sentence": sentence})
    translation_response = translation_handler(lambda_body, None)
    body, status = parse_lambda_response(translation_response)
    return jsonify(body), status


@app.route("/response-suggestion", methods=["POST"])
def get_response_suggestions():
    sentence = request.json.get("sentence")
    lambda_body = create_lambda_event({"sentence": sentence})
    response_suggestion_response = response_suggestion_handler(lambda_body, None)
    body, status = parse_lambda_response(response_suggestion_response)
    return jsonify(body), status


@app.route("/literal-translation", methods=["POST"])
def get_literal_translation():
    sentence = request.json.get("sentence")
    lambda_body = create_lambda_event({"sentence": sentence})
    literal_translation_response = literal_translation_handler(lambda_body, None)
    body, status = parse_lambda_response(literal_translation_response)
    return jsonify(body), status


@app.route("/syntactical-analysis", methods=["POST"])
def get_syntactical_analysis():
    sentence = request.json.get("sentence")
    lambda_body = create_lambda_event({"sentence": sentence})
    translation_response = syntactical_analysis_handler(lambda_body, None)
    body, status = parse_lambda_response(translation_response)
    return jsonify(body), status


@app.route("/health", methods=["GET"])
def get_health():
    return jsonify({"status": "healthy"}), 200


def create_lambda_event(body: dict) -> dict:
    return {"body": json.dumps(body)}


def parse_lambda_response(response: dict[str, str]) -> Tuple[str, str]:
    status_code = response["statusCode"]
    body = json.loads(response["body"])
    return body, status_code


if __name__ == "__main__":
    app.run(debug=True)
