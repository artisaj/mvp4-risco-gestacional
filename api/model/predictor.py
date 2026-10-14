import pandas as pd
from sklearn.pipeline import Pipeline

from config import FEATURES


def predict_risk(model: Pipeline, features: dict) -> tuple[str, dict[str, float]]:
    """Prevê o nível de risco de uma gestante.

    Recebe os atributos com os nomes usados no treinamento e retorna a classe
    prevista e a probabilidade estimada para cada classe.
    """
    sample = pd.DataFrame([features], columns=FEATURES)
    predicted_class = model.predict(sample)[0]
    probabilities = model.predict_proba(sample)[0]
    return predicted_class, dict(zip(model.classes_, probabilities.round(4).tolist()))
