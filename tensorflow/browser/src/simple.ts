import {
    layers, randomNormal, Rank, Sequential, sequential, sigmoid, Tensor, tensor2d, train
} from "@tensorflow/tfjs";
import { render, show } from "@tensorflow/tfjs-vis";


class DataProvider {
  readonly w1: Tensor<Rank>;
  readonly w2: Tensor<Rank>;

  constructor(w1Values: number[][], w2Values: number[][]) {
    this.w1 = tensor2d(w1Values);
    this.w2 = tensor2d(w2Values);
  }

  createDataPoints(batchSize: number) {
    const xIn = randomNormal([2, batchSize], 0, 1, 'float32');
    const y1 = sigmoid(this.w1.matMul(xIn));
    const y2 = sigmoid(this.w2.matMul(y1));
    const xs = xIn.reshape([batchSize, 2]);
    const ys = y2.reshape([batchSize, 1]);
    // console.log(xs.shape, xs.arraySync());
    // console.log(ys.shape, ys.arraySync());
    return { xs, ys };
  }
}

function getModel() {
  const model = sequential();

  model.add(
    layers.dense({
      inputShape: [2],
      units: 2,
      activation: 'sigmoid',
    })
  );

  model.add(
    layers.dense({
      units: 1,
      activation: 'sigmoid',
    })
  );

  const optimizer = train.adam();

  model.compile({ loss: 'meanSquaredError', optimizer });

  return model;
}

async function trainModel(
  model: Sequential,
  dataProvider: DataProvider,
  callbacks?: any,
  batchSize = 4,
  trainingDataSize = 100,
  testingDataSize = 10,
  epochs = 3
) {
  const { xs: trainXs, ys: trainYs } = dataProvider.createDataPoints(trainingDataSize);
  const { xs: testXs, ys: testYs } = dataProvider.createDataPoints(testingDataSize);

  const progress = model.fit(trainXs, trainYs, {
    batchSize,
    epochs,
    validationData: [testXs, testYs],
    shuffle: true,
    callbacks,
  });

  return progress;
}

function predict(model: Sequential, xs: Tensor<Rank>) {
  const predictions = model.predict(xs);
  return predictions;
}

export async function run() {
  // init
  const dp = new DataProvider(
    [
      [0, 0],
      [0, 1],
      [1, 0],
      [1, 1],
    ],
    [[0, 1, 1, 0]]
  );
  const model = getModel();

  // prediction
  const testData0 = dp.createDataPoints(1);
  const predictions0 = predict(model, testData0.xs);
  console.log({ predicted: predictions0.arraySync(), trueVal: testData0.ys.arraySync() });

  // training
  await trainModel(
    model,
    dp,
    show.fitCallbacks({ name: 'Model Training', tab: 'Training' }, ['loss', 'val_loss']),
    20,
    1000,
    100,
    3
  );

  const weights0 = model.layers[0].getWeights().map((w) => w.arraySync());
  const weights1 = model.layers[1].getWeights().map((w) => w.arraySync());
  render.heatmap({ name: 'Model Training', tab: 'Weights' }, { values: weights0 as any });
  render.heatmap({ name: 'Model Training', tab: 'Weights' }, { values: weights1 as any });

  console.log({ weights0, weights1 });

  // prediction
  const testData1 = dp.createDataPoints(1);
  const predictions1 = predict(model, testData1.xs);
  console.log({ predicted: predictions1.arraySync(), trueVal: testData1.ys.arraySync() });
}
