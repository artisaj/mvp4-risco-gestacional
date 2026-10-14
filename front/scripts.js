const API_URL = "http://127.0.0.1:5000/predicao";

// Classe retornada pela API -> sufixo usado nas classes CSS.
const RISK_STYLES = {
  "low risk": "low",
  "mid risk": "mid",
  "high risk": "high",
};

const RISK_LABELS = {
  "low risk": "Risco baixo",
  "mid risk": "Risco médio",
  "high risk": "Risco alto",
};

// Gestantes reais do conjunto de teste, classificadas corretamente pelo modelo.
const EXAMPLES = {
  low: { idade: 20, pressao_sistolica: 120, pressao_diastolica: 75, glicemia: 7.5, temperatura: 98, frequencia_cardiaca: 70 },
  mid: { idade: 29, pressao_sistolica: 130, pressao_diastolica: 70, glicemia: 7.5, temperatura: 98, frequencia_cardiaca: 78 },
  high: { idade: 50, pressao_sistolica: 140, pressao_diastolica: 90, glicemia: 15, temperatura: 98, frequencia_cardiaca: 90 },
};

const form = document.getElementById("prediction-form");
const submitButton = form.querySelector("button[type=submit]");
const resultSection = document.getElementById("result");
const resultLabel = document.getElementById("result-label");
const probabilitiesDiv = document.getElementById("probabilities");
const errorMessage = document.getElementById("error");
const celsiusHint = document.getElementById("celsius-hint");

const fahrenheitToCelsius = (fahrenheit) => ((fahrenheit - 32) * 5) / 9;

const updateCelsiusHint = () => {
  const fahrenheit = parseFloat(form.temperatura.value);
  celsiusHint.textContent = Number.isNaN(fahrenheit)
    ? "(98 °F ≈ 36,7 °C)"
    : `(≈ ${fahrenheitToCelsius(fahrenheit).toFixed(1).replace(".", ",")} °C)`;
};

const hideMessages = () => {
  resultSection.hidden = true;
  errorMessage.hidden = true;
};

const showError = (message) => {
  resultSection.hidden = true;
  errorMessage.textContent = message;
  errorMessage.hidden = false;
};

const fillExample = (exampleName) => {
  Object.entries(EXAMPLES[exampleName]).forEach(([field, value]) => {
    form.elements[field].value = value;
    form.elements[field].classList.remove("invalid");
  });
  updateCelsiusHint();
  hideMessages();
};

// Valida os campos no navegador usando os limites min/max definidos no HTML.
const validateForm = () => {
  const inputs = [...form.querySelectorAll("input")];
  inputs.forEach((input) => input.classList.toggle("invalid", !input.checkValidity()));

  const invalidInput = inputs.find((input) => !input.checkValidity());
  if (!invalidInput) {
    return true;
  }
  const fieldName = invalidInput.closest("label").firstChild.textContent.trim();
  showError(`Preencha "${fieldName}" com um valor entre ${invalidInput.min} e ${invalidInput.max}.`);
  return false;
};

const readFormData = () =>
  Object.fromEntries([...form.querySelectorAll("input")].map((input) => [input.name, Number(input.value)]));

const renderProbabilities = (probabilities) => {
  probabilitiesDiv.innerHTML = "";
  Object.keys(RISK_LABELS).forEach((riskClass) => {
    const percent = Math.round((probabilities[riskClass] ?? 0) * 100);
    const row = document.createElement("div");
    row.className = "probability-row";
    row.innerHTML = `
      <span>${RISK_LABELS[riskClass]}</span>
      <div class="bar"><div class="bar-fill ${RISK_STYLES[riskClass]}" style="width: ${percent}%"></div></div>
      <span>${percent}%</span>`;
    probabilitiesDiv.appendChild(row);
  });
};

const showResult = ({ classe, rotulo, probabilidades }) => {
  errorMessage.hidden = true;
  resultSection.className = `card result ${RISK_STYLES[classe]}`;
  resultLabel.textContent = rotulo;
  renderProbabilities(probabilidades);
  resultSection.hidden = false;
};

const requestPrediction = async (data) => {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (response.status === 422) {
    throw new Error("A API recusou os dados enviados. Verifique se os valores estão dentro das faixas permitidas.");
  }
  if (!response.ok) {
    throw new Error(`Erro inesperado na API (código ${response.status}).`);
  }
  return response.json();
};

const handleSubmit = async (event) => {
  event.preventDefault();
  hideMessages();
  if (!validateForm()) {
    return;
  }

  submitButton.disabled = true;
  submitButton.textContent = "Classificando...";
  try {
    showResult(await requestPrediction(readFormData()));
  } catch (error) {
    const isNetworkError = error instanceof TypeError;
    showError(isNetworkError
      ? "Não foi possível conectar à API. Verifique se o back-end está em execução."
      : error.message);
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Classificar risco";
  }
};

form.addEventListener("submit", handleSubmit);
form.addEventListener("reset", () => {
  form.querySelectorAll("input").forEach((input) => input.classList.remove("invalid"));
  hideMessages();
  setTimeout(updateCelsiusHint);
});
form.temperatura.addEventListener("input", updateCelsiusHint);
document.querySelectorAll(".btn-example").forEach((button) =>
  button.addEventListener("click", () => fillExample(button.dataset.example)));

updateCelsiusHint();
