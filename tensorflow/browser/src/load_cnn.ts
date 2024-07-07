import { browser, concat, loadLayersModel, moments, Rank, Tensor } from '@tensorflow/tfjs';

interface Point {
  x: number;
  y: number;
}

function getSamples(container: HTMLImageElement, samplePoints: Point[]): Tensor<Rank> {
  // 1. all data
  const imgData = browser.fromPixels(container);

  const samples = [];
  for (const samplePoint of samplePoints) {
    // 2. window
    let sampleData = imgData.slice([samplePoint.x, samplePoint.y, 0], [64, 64, 3]);

    // 3. mormalize
    const momts = moments(sampleData);
    const mean = momts.mean;
    const stdv = momts.variance.sqrt();
    const sampleDataNormalized = sampleData.sub(mean).div(stdv) as Tensor<Rank>;

    samples.push(sampleDataNormalized.reshape([1, 64, 64, 3]));
  }

  // 4. concat
  const samplesTensor = concat(samples, 0) as Tensor<Rank>;
  return samplesTensor;
}

type NamedPrediction = { [key: string]: number };

function predictionsToLabeled(predictions: number[][]): NamedPrediction[] {
  const namedPredictions: NamedPrediction[] = [];

  const classes = [
    'AnnualCrop',
    'Forest',
    'HerbaceousVegetation',
    'Highway',
    'Industrial',
    'Pasture',
    'PermanentCrop',
    'Residential',
    'River',
    'SeaLake',
  ];

  for (const prediction of predictions) {
    const namedPrediction: NamedPrediction = {};
    for (let i = 0; i < prediction.length; i++) {
      const classPrediction = prediction[i];
      const label = classes[i];
      namedPrediction[label] = classPrediction;
    }

    namedPredictions.push(namedPrediction);
  }

  return namedPredictions;
}

function bestPrediction(pred: NamedPrediction): string {
  let bestPrediction = '';
  let bestScore = 0;
  for (const [key, value] of Object.entries(pred)) {
    if (value > bestScore) {
      bestPrediction = key;
      bestScore = value;
    }
  }
  return bestPrediction;
}

function bestPredictions(pred: NamedPrediction[]): string[] {
  return pred.map((p) => bestPrediction(p));
}

export async function run() {
  const image = document.getElementById('image') as HTMLImageElement;

  const model = await loadLayersModel('/sentinel2_cnn_oldstyle/model.json');
  console.log(model.summary());

  const sampleLocations = [
    { x: 0, y: 0 },
    { x: 62, y: 0 },
    { x: 128, y: 0 },
    { x: 192, y: 0 },
    { x: 156, y: 0 },
    { y: 62, x: 0 },
    { y: 128, x: 0 },
    { y: 192, x: 0 },
    { y: 156, x: 0 },
  ];
  const sample = getSamples(image, sampleLocations);
  const predictionTensor = model.predict(sample) as Tensor<Rank>;
  const predictions = predictionTensor.arraySync() as number[][];
  const labeled = predictionsToLabeled(predictions);
  const best = bestPredictions(labeled);
  console.log(best);
}
