from keras.utils import pad_sequences
from keras.models import load_model
from joblib import load
import time

from . import BaseModel


class BasicEmotionDetector(BaseModel):
    # KERAS
    SEQUENCE_LENGTH = 300

    # SENTIMENT
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"
    SENTIMENT_THRESHOLDS = (0.4, 0.7)

    def __init__(self, model_path=None, tokenizer_path=None):
        super(BasicEmotionDetector, self).__init__()
        self.model = load_model(model_path)
        self.tokenizer = load(tokenizer_path)

    @staticmethod
    def decode_sentiment(score, include_neutral=True):
        if include_neutral:
            label = BasicEmotionDetector.NEUTRAL
            if score <= BasicEmotionDetector.SENTIMENT_THRESHOLDS[0]:
                label = BasicEmotionDetector.NEGATIVE
            elif score >= BasicEmotionDetector.SENTIMENT_THRESHOLDS[1]:
                label = BasicEmotionDetector.POSITIVE

            return label
        else:
            return BasicEmotionDetector.NEGATIVE if score < 0.5 else BasicEmotionDetector.POSITIVE

    def predict(self, text, include_neutral=True, *args, **kwargs):
        start_at = time.time()
        # Tokenize text
        x_test = pad_sequences(self.tokenizer.texts_to_sequences([text]), maxlen=self.SEQUENCE_LENGTH)
        # Predict
        score = self.model.predict([x_test])[0]
        # Decode sentiment
        label = self.decode_sentiment(score, include_neutral=include_neutral)

        return {"label": label, "score": float(score),
                "elapsed_time": time.time() - start_at}




