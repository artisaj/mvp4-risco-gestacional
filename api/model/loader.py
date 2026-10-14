from pathlib import Path

import joblib
from sklearn.pipeline import Pipeline


def load_model(path: Path) -> Pipeline:
    """Carrega do disco o pipeline treinado no notebook."""
    if not path.exists():
        raise FileNotFoundError(f"Arquivo do modelo não encontrado: {path}")
    return joblib.load(path)
