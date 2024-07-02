// possibly better implementation: https://github.com/adc-code/ML_ImageProcessing/blob/master/MNIST_TensorFlowJS/NumPredictor.js

import embed from "vega-embed";
import { TopLevelSpec } from "vega-lite";

import { loadLayersModel, Rank, Tensor, tensor4d } from "@tensorflow/tfjs";


function drawCanvas(divElement: HTMLDivElement) {
  const canvas = document.createElement('canvas');
  canvas.width = 28;
  canvas.height = 28;
  canvas.style.setProperty('width', '100%');
  canvas.style.setProperty('height', '100%');
  divElement.appendChild(canvas);

  const ctx = canvas.getContext('2d')!;
  if (!ctx) throw new Error('Failed to get 2D context');

  ctx.lineWidth = 2;
  ctx.lineCap = 'round';
  ctx.strokeStyle = 'white';

  let isDrawing = false;
  let lastX = 0;
  let lastY = 0;

  function draw(e: MouseEvent) {
    if (!isDrawing) return;

    const x = (canvas.width * (e.clientX - canvas.offsetLeft)) / canvas.clientWidth;
    const y = (canvas.height * (e.clientY - canvas.offsetTop)) / canvas.clientHeight;

    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(x, y);
    ctx.stroke();
    [lastX, lastY] = [x, y];
  }

  canvas.addEventListener('mousedown', (e) => {
    isDrawing = true;

    const x = (canvas.width * (e.clientX - canvas.offsetLeft)) / canvas.clientWidth;
    const y = (canvas.height * (e.clientY - canvas.offsetTop)) / canvas.clientHeight;

    [lastX, lastY] = [x, y];
  });
  canvas.addEventListener('mousemove', draw);
  canvas.addEventListener('mouseup', () => (isDrawing = false));
  canvas.addEventListener('mouseout', () => (isDrawing = false));

  return canvas;
}

function clearCanvas(canvas: HTMLCanvasElement) {
  const ctx = canvas.getContext('2d')!;
  ctx.fillStyle = 'black';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function clearButton(canvasParent: HTMLDivElement, canvas: HTMLCanvasElement, resultParent: HTMLDivElement) {
  const button = document.createElement('button');
  button.textContent = 'Clear';
  button.addEventListener('click', () => {
    const ctx = canvas.getContext('2d')!;
    if (!ctx) throw new Error('Failed to get 2D context');
    clearCanvas(canvas);
    resultParent.innerHTML = '';
  });

  canvasParent.appendChild(button);
  return button;
}

function parseButton(
  parent: HTMLDivElement,
  canvas: HTMLCanvasElement,
  callback: (data: Uint8ClampedArray, width: number, height: number) => void
) {
  const button = document.createElement('button');
  button.textContent = 'Parse';
  button.addEventListener('click', () => {
    const ctx = canvas.getContext('2d')!;
    if (!ctx) throw new Error('Failed to get 2D context');
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    callback(imageData.data, imageData.width, imageData.height);
  });

  parent.appendChild(button);
  return button;
}

/**
 * Function takes a UInt8ClampedArray as input and returns a tfjs tensor of dimension [1, 28, 28, 1]
 * input data: [r,g,b,a,  r,g,b,a,  r,g,b,a, ....]
 */
function uint8ToTensor(data: Uint8ClampedArray, w: number, h: number): Tensor<Rank> {
  const inData = Array.from(data);
  const outData: number[] = [];
  for (let i = 0; i < inData.length; i += 4) {
    const r = inData[i + 0] / 255;
    const a = inData[i + 3] / 255;
    outData.push(r * a);
  }
  return tensor4d(outData, [1, w, h, 1]);
}

async function barchart(parent: HTMLDivElement, barChartData: { label: string; value: number }[]) {
  const spec: TopLevelSpec = {
    $schema: 'https://vega.github.io/schema/vega-lite/v5.json',
    description: 'A simple bar chart with embedded data.',
    data: {
      values: barChartData,
    },
    mark: 'bar',
    encoding: {
      x: { field: 'label', type: 'nominal', axis: { labelAngle: 0 } },
      y: { field: 'value', type: 'quantitative' },
    },
  };
  const result = await embed(parent, spec);
  return result;
}

export async function run() {
  const resultParent = document.getElementById('displayNet') as HTMLDivElement;
  const drawingParent = document.getElementById('displayTraining') as HTMLDivElement;

  const canvas = drawCanvas(drawingParent);
  const pb = parseButton(drawingParent, canvas, (data, w, h) => {
    const inputs = uint8ToTensor(data, w, h);
    const outputs = model.predict(inputs) as Tensor<Rank>;
    const interpretation = (outputs.arraySync() as number[][])[0];
    console.log(interpretation);
    const barChartData = interpretation.map((p, i) => ({ label: `${i}`, value: p }));
    barchart(resultParent, barChartData);
  });
  const cb = clearButton(drawingParent, canvas, resultParent);

  const model = await loadLayersModel('/mnist_trained_model.json');
  console.log(model);
}
