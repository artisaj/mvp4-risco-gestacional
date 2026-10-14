from pydantic import BaseModel, Field


class PredictionInput(BaseModel):
    """Sinais clínicos de uma gestante.

    Os limites rejeitam valores fisiologicamente implausíveis antes que cheguem ao modelo.
    """
    idade: int = Field(..., ge=10, le=70, description="Idade em anos", examples=[35])
    pressao_sistolica: int = Field(..., ge=60, le=200, description="Pressão sistólica (mmHg)", examples=[140])
    pressao_diastolica: int = Field(..., ge=40, le=140, description="Pressão diastólica (mmHg)", examples=[90])
    glicemia: float = Field(..., ge=3, le=30, description="Glicemia (mmol/L)", examples=[13.0])
    temperatura: float = Field(..., ge=95, le=106, description="Temperatura corporal (°F)", examples=[98.0])
    frequencia_cardiaca: int = Field(..., ge=40, le=200, description="Frequência cardíaca em repouso (bpm)", examples=[70])

    def to_model_features(self) -> dict:
        """Converte para os nomes de atributos usados no treinamento do modelo."""
        return {
            "Age": self.idade,
            "SystolicBP": self.pressao_sistolica,
            "DiastolicBP": self.pressao_diastolica,
            "BS": self.glicemia,
            "BodyTemp": self.temperatura,
            "HeartRate": self.frequencia_cardiaca,
        }


class PredictionOutput(BaseModel):
    """Resultado da classificação de risco."""
    classe: str = Field(description="Classe prevista pelo modelo", examples=["high risk"])
    rotulo: str = Field(description="Classe prevista em português", examples=["Risco alto"])
    probabilidades: dict[str, float] = Field(description="Probabilidade estimada de cada classe")
