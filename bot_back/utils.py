import glob
import json
import logging
from itertools import chain

import os

from bot_back.intent_classifier import FastTextIntentClassifier

logger = logging.getLogger()


def list_models(models_dir):
    return chain(glob.glob(os.path.join(models_dir, '*.bin')), glob.glob(os.path.join(models_dir, '*.ftz')))


def load_models(models_dir, label_prefix='__label__', preprocessor=None):
    models = {}

    for model_path in list_models(models_dir):
        model = FastTextIntentClassifier(preprocessor=preprocessor,
                                         label_prefix=label_prefix).load(model_path)
        models[model.lang] = model
        logger.debug('Loaded model for lang: {} [{}]'.format(model.lang, model_path))

    intent_conf = json.load(open(os.path.join(models_dir, 'intent_conf.json')))

    return models, intent_conf


def classify_intent(text, model, k, intent_conf):
    intent_ids, probs = model.predict(text, k=k)
    result = []

    for prob, intent_id in zip(probs, intent_ids):
        assert intent_id in intent_conf, 'Unknown intent_id ({})'.format(intent_id)

        result.append({
            'intentId': intent_id,
            'score': prob,
            'intentName': intent_conf[intent_id]
        })

    return list(sorted(result, key=lambda x: x['score'], reverse=True))
