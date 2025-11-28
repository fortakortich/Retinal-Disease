interface Prediction {
  label: string;
  probability: number;
  status: string;
}

const imageUpload = document.getElementById('imageUpload') as HTMLInputElement;
const predictButton = document.getElementById('predictButton') as HTMLButtonElement;
const resultDiv = document.getElementById('result') as HTMLDivElement;
const predictionList = document.getElementById('predictionList') as HTMLUListElement;

const LABELS = ['DR', 'ARMD', 'MH', 'DN', 'MYA', 'BRVO', 'TSLN', 'ERM', 'LS', 'MS', 'CSR', 'ODC', 
                'CRVO', 'TV', 'AH', 'ODP', 'ODE', 'ST', 'AION', 'PT', 'RT', 'RS', 'CRS', 'EDN', 
                'RPEC', 'MHL', 'RP', 'CWS', 'CB', 'ODPM', 'PRH', 'MNF', 'HR', 'CRAO', 'TD', 'CME', 
                'PTCR', 'CF', 'VH', 'MCA', 'VS', 'BRAO', 'PLQ', 'HPED', 'CL'];

predictButton.addEventListener('click', () => {
  const file = imageUpload.files?.[0];
  if (!file) {
    alert('Please upload an image!');
    return;
  }

  const formData = new FormData();
  formData.append('image', file);

  // Здесь бы был API-запрос, но для статического сайта эмулируем предсказание
  const dummyPrediction = simulatePrediction();
  displayResults(dummyPrediction);
});

function simulatePrediction(): Prediction[] {
  // Эмуляция предсказаний (замени на реальные данные с API или локального предикта)
  return LABELS.map(label => ({
    label,
    probability: Math.random(),
    status: Math.random() > 0.5 ? '✅' : ''
  })).sort((a, b) => b.probability - a.probability);
}

function displayResults(predictions: Prediction[]) {
  predictionList.innerHTML = '';
  predictions.forEach(pred => {
    const li = document.createElement('li');
    li.textContent = `${pred.label}: ${pred.probability.toFixed(3)} ${pred.status}`;
    predictionList.appendChild(li);
  });
  resultDiv.classList.remove('hidden');
}