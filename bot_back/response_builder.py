import time


class ResponseBuilder:
    def __init__(self):
        self._request = None
        self._status_code = None
        self._message = None
        self._intent_classification_result = None
        self._ner_result = None

    def set_request(self, request):
        self._request = request
        return self

    def set_status_code(self, status_code):
        self._status_code = status_code
        return self

    def set_message(self, message):
        self._message = message
        return self

    def set_intent_classification_result(self, intent_classification_result):
        self._intent_classification_result = intent_classification_result
        return self

    def set_ner_result(self, ner_result):
        self._ner_result = ner_result
        return self

    def build(self):
        response = {
            'lang': (self._request or {}).get('lang'),
            'result': {
                'fulfillment': {
                    'speech': (self._request or {}).get('query')
                }
            },
            'sessionId': (self._request or {}).get('sessionId'),
            'status': {
                'code': self._status_code,
                'errorType': self._message
            },
            'timestamp': int(time.time())
        }

        if self._ner_result:
            response['parameters'] = self._ner_result.to_dict()

        if self._intent_classification_result:
            response['metadata'] = self._intent_classification_result
            response['source'] = self._intent_classification_result.model_version

        return response
