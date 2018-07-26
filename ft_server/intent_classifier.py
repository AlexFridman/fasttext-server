import abc
import os


class IntentClassifier:
    @abc.abstractmethod
    def predict(self, X):
        pass


class FastTextIntentClassifier(IntentClassifier):
    def __init__(self, preprocessor=None, label_prefix=None, k=1):
        self._preprocessor = preprocessor
        self._label_prefix = label_prefix
        self._k = k
        self._fast_text_model = None

        self.version = None
        self.lang = None

    def load(self, path):
        import fastText

        self._fast_text_model = fastText.load_model(path)

        model_file_name, _ = os.path.splitext(os.path.basename(path))
        self.lang, self.version = model_file_name.split('_')

        return self

    def predict(self, X, k=None):
        assert isinstance(X, (list, str))

        preprocessed = X

        if self._preprocessor is not None:
            if isinstance(X, list):
                preprocessed = list(map(self._preprocessor, X))
            else:
                preprocessed = self._preprocessor(X)

        labels, probs = self._fast_text_model.predict(preprocessed, k=k or self._k)

        if self._label_prefix:
            if isinstance(X, list):
                labels = [[l.replace(self._label_prefix, '') for l in labels_list] for labels_list in labels]
            else:
                labels = [l.replace(self._label_prefix, '') for l in labels]

        return labels, probs
