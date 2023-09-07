from dataclasses import dataclass
import ssl
import numpy as np
import pandas as pd
from tqdm import tqdm
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from string import punctuation

from dashboard.model import BaseModel

ssl._create_default_https_context = ssl._create_unverified_context
nltk.download(['stopwords', 'punkt', 'wordnet'])


@dataclass()
class Emotions:
    afraid: float
    angry: float
    happy: float
    sad: float

    def __post_init__(self):
        self.afraid *= 100
        self.angry *= 100
        self.happy *= 100
        self.sad *= 100


class MoodModel(BaseModel):
    def __init__(self, lexicon_file="depecheMood/DepecheMood_english_token_full.tsv"):
        super(MoodModel, self).__init__()
        self.lexicon = self.load_lexicon(lexicon_file)
        self.stopwords = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    @staticmethod
    def load_lexicon(filename, freq_threshold=10):
        unimportant = ['DONT_CARE', 'AMUSED', 'INSPIRED', 'ANNOYED']
        dm_lexer = pd.read_csv(filename, sep='\t', index_col=0)
        dm_lexer = dm_lexer[dm_lexer['freq'] > 10]
        dm_lexer.drop(['freq'] + unimportant, inplace=True, axis=1)
        return dm_lexer

    def pre_process(self, text):
        # Convert text to lowercase
        text = text.lower()

        # Tokenize the text
        tokens = word_tokenize(text)

        # Remove stopwords and punctuation
        tokens = [token for token in tokens if token not in self.stopwords and token not in punctuation]

        # Lemmatize the tokens
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]

        return tokens

    def predict(self, text, **kwargs):
        text = self.pre_process(text)
        ss = np.zeros((len(text), self.lexicon.shape[1]))
        result = pd.DataFrame(ss, columns=self.lexicon.columns, index=text)
        for i, doc in tqdm(enumerate(text)):
            if doc not in self.lexicon.index:
                result.drop([doc], inplace=True)
                continue
            result.loc[[doc]] = self.lexicon.loc[[doc]]
        res_mean_emo = result.mean()
        emo = Emotions(
            afraid=res_mean_emo['AFRAID'],
            angry=res_mean_emo['ANGRY'],
            happy=res_mean_emo['HAPPY'],
            sad=res_mean_emo['SAD'],
        )
        return emo


if __name__ == "__main__":
    model = MoodModel()

    input_text = "I'm feeling happy and excited about the upcoming vacation!"
    emotion_scores = model.predict(input_text)
    print("Emotion Scores:\n\n", emotion_scores)

