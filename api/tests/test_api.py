"""Testes da rota de predição da API."""
import pytest

from app import app
from config import RISK_LABELS

VALID_INPUT = {
    "idade": 35,
    "pressao_sistolica": 140,
    "pressao_diastolica": 90,
    "glicemia": 13.0,
    "temperatura": 98.0,
    "frequencia_cardiaca": 70,
}


@pytest.fixture
def client():
    return app.test_client()


def test_prediction_returns_a_known_risk_class(client):
    response = client.post("/predicao", json=VALID_INPUT)

    assert response.status_code == 200
    body = response.get_json()
    assert body["classe"] in RISK_LABELS
    assert body["rotulo"] == RISK_LABELS[body["classe"]]
    assert sum(body["probabilidades"].values()) == pytest.approx(1.0)


def test_prediction_rejects_implausible_values(client):
    response = client.post("/predicao", json={**VALID_INPUT, "frequencia_cardiaca": 7})

    assert response.status_code == 422


def test_prediction_rejects_missing_fields(client):
    response = client.post("/predicao", json={"idade": 35})

    assert response.status_code == 422
