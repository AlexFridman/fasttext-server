import glob
import json
import logging
from itertools import chain

import fastText
import os

from sberbot_nlu_back.intent_classifier import FastTextIntentClassifier

logger = logging.getLogger()


def list_models(models_dir):
    return chain(glob.glob(os.path.join(models_dir, '*.bin')), glob.glob(os.path.join(models_dir, '*.ftz')))


def load_models(models_dir, label_prefix='__label__', preprocessor=None):
    models = {}
    intent_config = json.load(open(os.path.join(models_dir, 'intent_conf.json')))

    for model_path in list_models(models_dir):
        name, _ = os.path.splitext(os.path.basename(model_path))
        lang, version = name.split('_')

        model = FastTextIntentClassifier(fasttext_model=fastText.load_model(model_path),
                                         lang=lang,
                                         version=version,
                                         intent_config=intent_config,
                                         preprocessor=preprocessor,
                                         label_prefix=label_prefix)
        models[model.lang] = model
        logger.debug('Loaded model for lang: {} [{}]'.format(model.lang, model_path))

    return models
