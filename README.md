# MVP4 – Classificação de Risco na Gestação

Projeto do MVP da disciplina de Engenharia de Sistemas de Software Inteligentes (PUC-Rio).

Um modelo de machine learning prevê o **nível de risco de uma gestação** (baixo, médio ou alto) a partir de seis sinais clínicos. O modelo é treinado num notebook do Google Colab e servido por uma aplicação full stack: um back-end em Flask carrega o modelo, e um front-end em HTML/CSS/JavaScript recebe os dados e exibe a predição.

- **Notebook (Colab):** [notebook/mvp4_risco_gestacional.ipynb](https://colab.research.google.com/github/artisaj/mvp4-risco-gestacional/blob/main/notebook/mvp4_risco_gestacional.ipynb)
- **Vídeo de apresentação:** _(link a adicionar)_

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

## Modelo

Foram comparados KNN, Árvore de Classificação, Naive Bayes e SVM, com dados originais, padronizados e normalizados, usando pipelines, validação cruzada repetida e otimização de hiperparâmetros. O modelo escolhido foi uma **Árvore de Classificação** (profundidade máxima 5). Resultados no conjunto de teste:

| Métrica | Resultado | Requisito mínimo |
|---|---|---|
| Recall de alto risco | 0,83 | 0,80 |
| Acurácia | 0,75 | 0,70 |
| F1-macro | 0,68 | 0,60 |

## Estrutura

```
├── data/                       dataset
├── notebook/                   notebook do Colab (treino do modelo)
├── api/                        back-end
│   ├── app.py                  rotas da API (Flask + OpenAPI)
│   ├── config.py               caminhos, atributos e requisitos de desempenho
│   ├── model/                  carga do modelo, predição e avaliação
│   ├── schemas/                validação dos dados de entrada e saída
│   ├── ml_model/               modelo exportado (.pkl) e conjunto de teste
│   ├── tests/                  testes PyTest
│   └── requirements.txt
└── front/                      front-end (index.html, styles.css, scripts.js)
```

## Como executar

**Pré-requisito:** Python 3.12 (o modelo foi treinado com scikit-learn 1.6.1, compatível com Python 3.10 a 3.13).

### 1. Back-end

Na raiz do projeto, crie e ative um ambiente virtual e instale as dependências:

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r api/requirements.txt
```

Inicie a API:

```bash
cd api
python app.py
```

A API fica disponível em http://127.0.0.1:5000. Acessando esse endereço, você é redirecionado para a documentação interativa (Swagger), onde é possível testar a rota `POST /predicao`.

### 2. Front-end

Com a API em execução, abra o arquivo [front/index.html](front/index.html) no navegador (duplo clique no arquivo). Preencha os campos, ou use os botões de exemplo, e clique em **Classificar risco**.

### 3. Testes automatizados

Com o ambiente virtual ativado, dentro da pasta `api`:

```bash
pytest -v
```

- [tests/test_model_performance.py](api/tests/test_model_performance.py): verifica se o modelo atende aos requisitos mínimos de desempenho (acurácia, F1-macro e recall de alto risco) no conjunto de teste.
- [tests/test_api.py](api/tests/test_api.py): verifica a rota de predição e a rejeição de dados inválidos.

**Substituição do modelo:** antes de colocar um novo modelo em produção, rode o teste de desempenho apontando para o arquivo candidato. Se algum requisito não for atingido, o teste falha e o modelo não deve ser implantado.

```bash
# Windows (PowerShell)
$env:MODEL_PATH="caminho/do/novo_modelo.pkl"; pytest tests/test_model_performance.py -v
# Linux / macOS
MODEL_PATH=caminho/do/novo_modelo.pkl pytest tests/test_model_performance.py -v
```

## Segurança

Os dados de saúde são dados pessoais sensíveis segundo a LGPD. A reflexão sobre anonimização e boas práticas de segurança está na seção 13 do notebook. Na aplicação, as entradas são validadas no back-end (tipos e faixas plausíveis) e os dados enviados para predição não são armazenados.
