import os.path

from .basicAnalyzer import BasicEmotionDetector


def get_model(name: str = "basic"):
    print(os.system("pwd"))
    if name.lower() == "basic":
        model_path = os.path.join(".", "dashboard", "model", "baseAnalyzer", "model.h5")
        tokenizer_path = os.path.join(".", "dashboard", "model", "baseAnalyzer", "tokenizer.pkl")
        model = BasicEmotionDetector(model_path=model_path, tokenizer_path=tokenizer_path)
        return model

    raise ModuleNotFoundError()


def get_model_initializer(model: str = "basic"):
    return lambda: get_model(name=model)
