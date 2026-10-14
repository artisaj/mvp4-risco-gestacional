"""Testes de desempenho do modelo de machine learning.

Garantem que o modelo atende aos requisitos mínimos definidos em
PERFORMANCE_REQUIREMENTS. Se um novo modelo for colocado no lugar do atual
e não atingir algum limite, o teste falha e o modelo não deve ser implantado.
"""
import pandas as pd
import pytest

from config import FEATURES, MODEL_PATH, PERFORMANCE_REQUIREMENTS, TARGET, TEST_DATA_PATH
from model import evaluate, load_model


@pytest.fixture(scope="module")
def metrics():
    model = load_model(MODEL_PATH)
    test_data = pd.read_csv(TEST_DATA_PATH)
    return evaluate(model, test_data[FEATURES], test_data[TARGET])


@pytest.mark.parametrize("metric, threshold", PERFORMANCE_REQUIREMENTS.items())
def test_model_meets_performance_requirement(metrics, metric, threshold):
    assert metrics[metric] >= threshold, (
        f"{metric} = {metrics[metric]:.3f}, abaixo do mínimo exigido de {threshold:.2f}"
    )
