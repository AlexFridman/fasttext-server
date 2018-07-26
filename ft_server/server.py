"""
.. module:: ft_server.server

"""

import json
import time

import os
from flask import Flask
from flask import g
from flask import jsonify
from flask import request

from ft_server.exceptions import BadRequest
from ft_server.utils import load_models, classify_intent
from ft_server import config

app = Flask(__name__)

if os.environ.get("FT_SERVER_ENV") == "development":
    app.config.from_object(config.DevelopmentConfig)
elif os.environ.get("FT_SERVER_ENV") == "test":
    app.config.from_object(config.TestConfig)
else:
    app.config.from_object(config.Config)

if os.environ.get("FT_SERVER_DOCKERIZED") == "True":
    app.config.from_object("config.DockerConfig")

if os.environ.get("FT_SERVER_SETTINGS"):
    app.config.from_envvar("FT_SERVER_SETTINGS")


def validate_classification_request(request):
    missing_fields = []
    for field in ("lang", "query", "top_n", "sessionId"):
        if field not in request:
            missing_fields.append(field)

    if missing_fields:
        raise BadRequest("Invalid request. Some fields ({}) are missing".format(", ".join(missing_fields)))

    if request["lang"] not in g.model_registry:
        raise BadRequest("Language {} is not supported. Supported langs are: {}"
                         .format(request["lang"], ", ".join(g.model_registry)))


@app.route("/classify_intent", methods=["POST"], endpoint="classify_intent")
def classify_intent_endpoint():
    classification_request = json.loads(request.data)
    validate_classification_request(classification_request)

    model = g.model_registry[classification_request["lang"]]

    response = {
        "lang": classification_request["lang"],
        "result": {
            "fulfillment": {
                "speech": classification_request["query"]
            },
            "metadata": classify_intent(classification_request["query"],
                                        model,
                                        classification_request["top_n"],
                                        g.intent_conf),
            "parameters": {},
            "source": model.version,
        },
        "sessionId": classification_request["sessionId"],
        "status": {
            "code": 200,
            "errorType": "success"
        },
        "timestamp": int(time.time())
    }

    return jsonify(response)


@app.before_request
def before_request():
    g.model_registry, g.intent_conf = load_models(app.config["FT_SERVER_MODEL_PATH"])


@app.errorhandler(Exception)
def handle_error(error):
    classification_request = json.loads(request.data)

    error_response = {
        "lang": classification_request.get("lang"),
        "sessionId": classification_request.get("sessionId"),
        "status": {
            "code": error.status_code,
            "errorType": error.message
        },
        "timestamp": int(time.time())
    }

    return jsonify(error_response), error.status_code


if __name__ == "__main__":
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"])
