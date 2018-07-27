import abc


class IntentClassificationResult:
    def __init__(self, query, intents, intents_ids, probs, model_version):
        self.query = query
        self.intents = intents
        self.intents_ids = intents_ids
        self.probs = probs
        self.model_version = model_version

    def to_dict(self):
        result = []

        for intent, intent_id, prob in zip(self.intents, self.intents_ids, self.probs):
            result.append({
                'intentId': intent_id,
                'intentName': intent,
                'score': prob
            })

        return list(sorted(result, key=lambda x: x['score'], reverse=True))


class IntentClassifier:
    def __init__(self, version, lang):
        self.version = version
        self.lang = lang

    @abc.abstractmethod
    def predict(self, query):
        pass


class FastTextIntentClassifier(IntentClassifier):
    def __init__(self, fasttext_model, version, lang, intent_config, preprocessor=None, label_prefix=None, k=1):
        super().__init__(version, lang)

        self._preprocessor = preprocessor
        self._label_prefix = label_prefix
        self._k = k
        self._fasttext_model = fasttext_model
        self._intent_config = intent_config

    def predict(self, query, k=None):
        original_query = query

        if self._preprocessor is not None:
            query = self._preprocessor(query)

        intents_ids, probs = self._fasttext_model.predict(query, k=k or self._k)

        if self._label_prefix:
            intents_ids = [intent_id.replace(self._label_prefix, '') for intent_id in intents_ids]

        intents = [self._intent_config[intent_id] for intent_id in intents_ids]

        return IntentClassificationResult(original_query, intents, intents_ids, probs, self.version)
