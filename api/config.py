"""Configurações centralizadas do back-end."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Os caminhos podem ser sobrescritos por variáveis de ambiente, o que permite
# testar um modelo candidato antes de substituir o modelo em produção.
MODEL_PATH = Path(os.getenv("MODEL_PATH", BASE_DIR / "ml_model" / "modelo_risco_gestacional.pkl"))
TEST_DATA_PATH = Path(os.getenv("TEST_DATA_PATH", BASE_DIR / "ml_model" / "dataset_teste.csv"))

# Atributos na ordem e com os nomes usados no treinamento do modelo.
FEATURES = ["Age", "SystolicBP", "DiastolicBP", "BS", "BodyTemp", "HeartRate"]
TARGET = "RiskLevel"
HIGH_RISK = "high risk"

RISK_LABELS = {
    "low risk": "Risco baixo",
    "mid risk": "Risco médio",
    "high risk": "Risco alto",
}

# Requisitos mínimos de desempenho (definidos no notebook, seção 11).
PERFORMANCE_REQUIREMENTS = {
    "acuracia": 0.70,
    "f1_macro": 0.60,
    "recall_alto_risco": 0.80,
}
