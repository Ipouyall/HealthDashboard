import os.path


def get_model(name: str = None):
    id = name.lower()
    if id == "dep-basic":
        model_path = os.path.join(".", "dashboard", "model", "baseAnalyzer", "model.h5")
        from .basicAnalyzer import BasicEmotionDetector
        tokenizer_path = os.path.join(".", "dashboard", "model", "baseAnalyzer", "tokenizer.pkl")
        model = BasicEmotionDetector(model_path=model_path, tokenizer_path=tokenizer_path)
        return model
    if id == "mood":
        path = os.path.join(".", "dashboard", "model", "depecheMood", "DepecheMood_english_token_full.tsv")
        from .mood import MoodModel
        model = MoodModel(lexicon_file=path)
        return model

    raise ModuleNotFoundError()
