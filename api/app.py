from flask import redirect
from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI, Tag

from config import MODEL_PATH, RISK_LABELS
from model import load_model, predict_risk
from schemas import PredictionInput, PredictionOutput

info = Info(
    title="API de Risco Gestacional",
    version="1.0.0",
    description="Classifica o risco de uma gestação a partir de sinais clínicos usando um modelo de machine learning.",
)
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Documentação interativa da API (Swagger)")
prediction_tag = Tag(name="Predição", description="Classificação do risco gestacional")

# O modelo é carregado uma única vez, na inicialização (modelo embarcado no back-end).
model = load_model(MODEL_PATH)


@app.get("/", tags=[home_tag])
def home():
    """Redireciona para a documentação interativa da API (Swagger)."""
    return redirect("/openapi/swagger")


@app.post("/predicao", tags=[prediction_tag], responses={200: PredictionOutput})
def predict(body: PredictionInput):
    """Prevê o nível de risco de uma gestante.

    Os dados recebidos não são armazenados.
    """
    predicted_class, probabilities = predict_risk(model, body.to_model_features())
    output = PredictionOutput(
        classe=predicted_class,
        rotulo=RISK_LABELS[predicted_class],
        probabilidades=probabilities,
    )
    return output.model_dump(), 200


if __name__ == "__main__":
    app.run(debug=True)
