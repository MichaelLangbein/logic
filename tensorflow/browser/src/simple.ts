import { scaleLinear } from "d3-scale";
import { interpolatePlasma } from "d3-scale-chromatic";
import { select } from "d3-selection";

import {
    getBackend, layers, Logs, losses, ones, randomNormal, randomUniform, Rank, Sequential,
    sequential, sigmoid, Tensor, tensor2d, train
} from "@tensorflow/tfjs";
import { show } from "@tensorflow/tfjs-vis";

import { createArray } from "./utils";


interface DataProvider {
  createDataPoints(batchSize: number): { xs: Tensor<Rank>; ys: Tensor<Rank> };
}

class SigmoidData implements DataProvider {
  readonly w1: Tensor<Rank>;
  readonly w2: Tensor<Rank>;

  /**
   * rows: in
   * columns: out
   */
  constructor(w1Values: number[][], w2Values: number[][]) {
    this.w1 = tensor2d(w1Values);
    this.w2 = tensor2d(w2Values);
  }

  createDataPoints(batchSize: number) {
    const xIn = randomNormal([batchSize, 2], 0, 1, 'float32');
    const y1 = sigmoid(xIn.matMul(this.w1));
    const y2 = sigmoid(y1.matMul(this.w2));
    return { xs: xIn, ys: y2 };
  }
}

class MultData implements DataProvider {
  createDataPoints(batchSize: number) {
    const x1 = randomNormal([batchSize, 1], 0, 1, 'float32');
    const x2 = randomNormal([batchSize, 1], 0, 1, 'float32');
    const xs = x1.concat(x2, 1);
    const ys = x1.add(x2);
    return { xs, ys };
  }
}

class XorData implements DataProvider {
  createDataPoints(batchSize: number): { xs: Tensor<Rank>; ys: Tensor<Rank> } {
    const one = ones([batchSize, 1], 'float32');
    const as = randomUniform([batchSize, 1], 0, 1, 'float32');
    const bs = randomUniform([batchSize, 1], 0, 1, 'float32');
    const sum = as.add(bs).sub(one);
    const abs = sum.abs();
    const xs = as.concat(bs, 1);
    const ys = abs;
    return { xs, ys };
  }
}

function getModel() {
  const model = sequential();

  model.add(
    layers.dense({
      inputShape: [2],
      units: 3,
      activation: 'sigmoid',
      useBias: false,
    })
  );

  model.add(
    layers.dense({
      units: 1,
      activation: 'sigmoid',
      useBias: false,
    })
  );

  const optimizer = train.adagrad(0.1);

  model.compile({ loss: losses.meanSquaredError, optimizer });

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
  const dp = new SigmoidData(
    [
      [1, 1, 0],
      [0, 1, 1],
    ],
    [[0], [1], [1]]
  );
  // const dp = new MultData();
  // const dp = new XorData();
  const model = getModel();
  console.log('backend: ', getBackend());

  // show.layer({ name: 'layer0', tab: 'layers before' }, model.layers[0]);
  // show.layer({ name: 'layer1', tab: 'layers before' }, model.layers[1]);

  // // prediction
  // const testData0 = dp.createDataPoints(1);
  // const predictions0 = predict(model, testData0.xs);
  // console.log({ predicted: predictions0.arraySync(), trueVal: testData0.ys.arraySync() });

  const callbacks = {
    ...show.fitCallbacks(document.getElementById('displayTraining')!, ['loss', 'val_loss']),
    onEpochBegin: (epoch: number, logs: Logs) => {
      const weights0 = model.layers[0].getWeights()[0].arraySync() as number[][];
      const weights1 = model.layers[1].getWeights()[0].arraySync() as number[][];
      drawNet(weights0, weights1);
    },
  };

  // training
  await trainModel(model, dp, callbacks, 50, 5_000, 100, 8);

  const weights0 = model.layers[0].getWeights()[0].arraySync() as number[][];
  const weights1 = model.layers[1].getWeights()[0].arraySync() as number[][];
  drawNet(weights0, weights1);
  // const bias0 = model.layers[0].getWeights()[1].arraySync();
  // const bias1 = model.layers[1].getWeights()[1].arraySync();
  // render.heatmap({ name: 'weights0', tab: 'Weights' }, { values: weights0 as any });
  // render.heatmap({ name: 'weights1', tab: 'Weights' }, { values: weights1 as any });
  // show.layer({ name: 'layer0', tab: 'layers after' }, model.layers[0]);
  // show.layer({ name: 'layer1', tab: 'layers after' }, model.layers[1]);
  console.log({ weights0, weights1 });

  // prediction
  const testData1 = dp.createDataPoints(10);
  const predictions1 = predict(model, testData1.xs) as Tensor<Rank>;
  console.log({
    predicted: predictions1.arraySync(),
    trueVal: testData1.ys.arraySync(),
    difference: predictions1.sub(testData1.ys).abs().arraySync(),
  });
}

// Getting hold of container and dimensions
const container = document.getElementById('displayNet')!;
const width = container.clientWidth;
const height = container.clientHeight;
const selection = select(container);
const svg = selection.append('svg');
svg.attr('width', width).attr('height', height);
const tooltip = select('body')
  .append('div')
  .attr('class', 'tooltip')
  .style('opacity', 0)
  .style('position', 'absolute')
  .style('background-color', 'white')
  .style('border', 'solid')
  .style('border-width', '1px')
  .style('border-radius', '5px')
  .style('padding', '5px');

function drawNet(weights0: number[][], weights1: number[][]) {
  // step 1: parse raw data
  const rows0 = weights0.length;
  const cols0 = weights0[0].length;
  const rows1 = weights1.length;
  const cols1 = weights1[0].length;

  const nrPointsIn = rows0;
  const nrPointsMid = cols0;
  const nrPointsOut = cols1;
  const pointsIn = createArray(nrPointsIn, (i) => ({ id: i, x: 0.25 }));
  const pointsMid = createArray(nrPointsMid, (i) => ({ id: i + nrPointsIn, x: 0.5 }));
  const pointsOut = createArray(nrPointsOut, (i) => ({ id: i + nrPointsIn + nrPointsMid, x: 0.75 }));

  const connections = [];
  for (let r = 0; r < rows0; r++) {
    for (let c = 0; c < cols0; c++) {
      connections.push({ from: r, to: c + nrPointsIn, weight: weights0[r][c] });
    }
  }
  for (let r = 0; r < rows1; r++) {
    for (let c = 0; c < cols1; c++) {
      connections.push({ from: r + nrPointsIn, to: c + nrPointsIn + nrPointsMid, weight: weights1[r][c] });
    }
  }

  // step 2: raw data to scaled data
  const xScale = scaleLinear().domain([0, 1]).range([0, width]);
  const yDist = height / 8;
  const yScaleIn = scaleLinear()
    .domain([0, nrPointsIn - 1])
    .range([height / 2 - (yDist * nrPointsIn) / 2, height / 2 + (yDist * nrPointsIn) / 2]);
  const yScaleMid = scaleLinear()
    .domain([0, nrPointsMid - 1])
    .range([height / 2 - (yDist * nrPointsMid) / 2, height / 2 + (yDist * nrPointsMid) / 2]);
  const yScaleOut = scaleLinear()
    .domain([0, nrPointsOut - 1])
    .range([height / 2 - (yDist * nrPointsOut) / 2, height / 2 + (yDist * nrPointsOut) / 2]);
  const weightThicknessScale = scaleLinear().domain([0, 3]).range([3, 10]);
  const weightColorScale = scaleLinear().domain([-3, 3]).range([0, 1]);

  const pointsInScaled = pointsIn.map((p) => ({ ...p, x: xScale(p.x), y: yScaleIn(p.id) }));
  const pointsMidScaled = pointsMid.map((p) => ({
    ...p,
    x: xScale(p.x),
    y: yScaleMid(p.id - nrPointsIn),
  }));
  const pointsOutScaled = pointsOut.map((p) => ({
    ...p,
    x: xScale(p.x),
    y: yScaleOut(p.id - nrPointsIn - nrPointsMid),
  }));
  const pointsScaled = [...pointsInScaled, ...pointsMidScaled, ...pointsOutScaled];

  // step 3: place data on svg
  const connectionsSelection = svg.selectAll('.connection').data(connections, (d: any) => `${d.from}-${d.to}`);
  connectionsSelection
    .enter()
    .append('line')
    .attr('x1', (d) => pointsScaled[d.from].x)
    .attr('y1', (d) => pointsScaled[d.from].y)
    .attr('x2', (d) => pointsScaled[d.to].x)
    .attr('y2', (d) => pointsScaled[d.to].y)
    .attr('stroke', (d) => interpolatePlasma(weightColorScale(d.weight)))
    .attr('stroke-width', (d) => weightThicknessScale(Math.abs(d.weight)))
    .attr('class', 'connection');
  connectionsSelection
    .attr('stroke', (d) => interpolatePlasma(weightColorScale(d.weight)))
    .attr('stroke-width', (d) => weightThicknessScale(Math.abs(d.weight)));
  connectionsSelection.exit().remove();

  // step 4: hovering over lines shows weight in tooltip
  connectionsSelection.on('mouseover', (event, d: any) => {
    tooltip
      .style('left', `${event.pageX}px`)
      .style('top', `${event.pageY}px`)
      .style('opacity', 0.9)
      .text(`weight: ${d.weight}`);
  });
  connectionsSelection.on('mouseout', () => tooltip.style('opacity', 0));

  const pointsSelection = svg.selectAll('.point').data(pointsScaled, (d: any) => d.id);
  pointsSelection
    .enter()
    .append('circle')
    .attr('r', 5)
    .attr('cx', (d) => d.x)
    .attr('cy', (d) => d.y)
    .attr('class', 'point');
  pointsSelection.exit().remove();
}
