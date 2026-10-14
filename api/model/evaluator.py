import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, recall_score
from sklearn.pipeline import Pipeline

from config import HIGH_RISK


def evaluate(model: Pipeline, X: pd.DataFrame, y: pd.Series) -> dict[str, float]:
    """Calcula as métricas usadas nos requisitos de desempenho do modelo."""
    y_pred = model.predict(X)
    return {
        "acuracia": accuracy_score(y, y_pred),
        "f1_macro": f1_score(y, y_pred, average="macro"),
        "recall_alto_risco": recall_score(y, y_pred, labels=[HIGH_RISK], average="macro"),
    }
