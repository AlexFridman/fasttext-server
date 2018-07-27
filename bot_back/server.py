import json
from collections import namedtuple

from flask import Flask
from flask import g
from flask import jsonify
from flask import request

from bot_back.exceptions import BadRequest, IntentClassificationError, LangIsNotSupported
from bot_back.response_builder import ResponseBuilder
from bot_back.utils import load_models

app = Flask(__name__)


@app.before_request
def before_request():
    g.intent_classification_model_registry, g.intent_conf = load_models(app.config['models_path'])


class Request(namedtuple('Request', ['lang', 'query', 'top_n', 'sessionId'])):
    @classmethod
    def validate_request(cls, request):
        missing_fields = []
        for field in cls.__slots__:
            if field not in request:
                missing_fields.append(field)

        if missing_fields:
            raise BadRequest('Invalid request. Some fields ({}) are missing'.format(', '.join(missing_fields)))

        return cls(**{field: request[field] for field in cls.__slots__})


@app.route('/', methods=['POST'])
def index():
    raw_request = json.loads(request.data)
    req = Request.validate_request(raw_request)

    try:
        intent_classification_model = g.intent_classification_model_registry[req.lang]
    except KeyError:
        raise LangIsNotSupported()

    try:
        intent_classification_result = intent_classification_model.predict(req.query.req.top_n)
    except Exception:
        raise IntentClassificationError()

    return jsonify(ResponseBuilder()
                   .set_request(raw_request)
                   .set_message('success')
                   .set_status_code(200)
                   .set_intent_classification_result(intent_classification_result))


@app.errorhandler(Exception)
def handle_error(error):
    try:
        req = json.loads(request.data)
    except ValueError:
        req = None

    message = getattr(error, 'message', 'error')
    status_code = getattr(error, 'status_code', 500)

    return jsonify(ResponseBuilder()
                   .set_request(req)
                   .set_message(message)
                   .set_status_code(status_code)), status_code
