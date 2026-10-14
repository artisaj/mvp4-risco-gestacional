# MVP4 – Classificação de Risco na Gestação

Projeto do MVP da disciplina de Engenharia de Sistemas de Software Inteligentes (PUC-Rio).

Um modelo de machine learning prevê o **nível de risco de uma gestação** (baixo, médio ou alto) a partir de seis sinais clínicos. O modelo é treinado num notebook do Google Colab e servido por uma aplicação full stack.

## Dataset

**Maternal Health Risk** – [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/863/maternal+health+risk)

| Atributo | Descrição |
|---|---|
| Age | Idade da gestante (anos) |
| SystolicBP | Pressão arterial sistólica (mmHg) |
| DiastolicBP | Pressão arterial diastólica (mmHg) |
| BS | Glicemia (mmol/L) |
| BodyTemp | Temperatura corporal (°F) |
| HeartRate | Frequência cardíaca em repouso (bpm) |
| **RiskLevel** | **Classe alvo:** `low risk`, `mid risk`, `high risk` |

Uma cópia do dataset está em [data/maternal_health_risk.csv](data/maternal_health_risk.csv). O notebook a carrega pela URL raw do GitHub.

## Estrutura

```
├── data/        dataset
├── notebook/    notebook do Colab (treino do modelo)
├── api/         back-end Flask + teste PyTest
└── front/       front-end HTML/CSS/JS
```

## Como executar

_(a preencher conforme o projeto avançar)_
