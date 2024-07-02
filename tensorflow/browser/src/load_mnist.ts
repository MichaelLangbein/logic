// possibly better implementation: https://github.com/adc-code/ML_ImageProcessing/blob/master/MNIST_TensorFlowJS/NumPredictor.js

import embed from 'vega-embed';
import { TopLevelSpec } from 'vega-lite';

import { browser, image, loadLayersModel, Rank, scalar, Tensor } from '@tensorflow/tfjs';

function drawCanvas(divElement: HTMLDivElement) {
  const canvas = document.createElement('canvas');
  canvas.width = divElement.clientWidth; //28;
  canvas.height = divElement.clientHeight;
  28;
  canvas.style.setProperty('width', '100%');
  canvas.style.setProperty('height', '100%');
  divElement.appendChild(canvas);

  const ctx = canvas.getContext('2d')!;
  if (!ctx) throw new Error('Failed to get 2D context');

  ctx.lineWidth = canvas.width / 10;
  ctx.lineCap = 'round';
  ctx.strokeStyle = 'black';

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
  ctx.fillStyle = 'white';
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

function parseButton(parent: HTMLDivElement, canvas: HTMLCanvasElement, callback: (data: ImageData) => void) {
  const button = document.createElement('button');
  button.textContent = 'Parse';
  button.addEventListener('click', () => {
    const ctx = canvas.getContext('2d')!;
    if (!ctx) throw new Error('Failed to get 2D context');
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    callback(imageData);
  });

  parent.appendChild(button);
  return button;
}

/**
 * Function takes a UInt8ClampedArray as input and returns a tfjs tensor of dimension [1, 28, 28, 1]
 * input data: [r,g,b,a,  r,g,b,a,  r,g,b,a, ....]
 */
function uint8ToTensor(data: ImageData): Tensor<Rank> {
  let img = browser.fromPixels(data);

  // prep the number image so that the CNN can understand what it should do
  // with it...

  // resize the image it so its 28 x 28, while adding padding to the edges
  const paddingFraction = 0.2;
  const padding = Math.floor((28 * paddingFraction) / 2);
  img = image.resizeBilinear(img, [28 - 2 * padding, 28 - 2 * padding]).toFloat();
  img = img.pad(
    [
      [padding, padding],
      [padding, padding],
      [0, 0],
    ],
    255
  );

  // adjust the dimensions so that the image will be accepted by the CNN... note
  // that the CNN requires tensors in the form [ batch number, image x, image y, channel ];
  // so the tensor needs to be resized to [ 1, 28, 28, 1 ]
  img = img.mean(2).toFloat().expandDims(0).expandDims(-1);

  // Finally normalize the data...
  img = img.div(scalar(255.0));

  // and take the 'inverse' of the image since the CNN was trained with white numbers on a
  // black background and we have black numbers on a white background
  img = scalar(1.0).sub(img);

  return img;
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

async function drawTensor(canvas: HTMLCanvasElement, tensor: Tensor<Rank>) {
  canvas.width = 28;
  canvas.height = 28;
  canvas.style.setProperty('margin', '4px');
  const tensor3D = tensor.slice([0, 0, 0, 0], [1, 28, 28, 1]).reshape([28, 28, 1]);
  await browser.toPixels(tensor3D as any, canvas);
}

export async function run() {
  const resultParent = document.getElementById('displayNet') as HTMLDivElement;
  const drawingParent = document.getElementById('displayTraining') as HTMLDivElement;
  const helperCanvas = document.createElement('canvas');
  helperCanvas.style.setProperty('outline', '1px solid black');
  document.body.appendChild(helperCanvas);

  const canvas = drawCanvas(drawingParent);
  const pb = parseButton(drawingParent, canvas, (data) => {
    const inputs = uint8ToTensor(data);
    drawTensor(helperCanvas, inputs);
    const outputs = model.predict(inputs) as Tensor<Rank>;
    const interpretation = (outputs.arraySync() as number[][])[0];
    console.log(interpretation);
    const barChartData = interpretation.map((p, i) => ({ label: `${i}`, value: p }));
    barchart(resultParent, barChartData);
  });
  const cb = clearButton(drawingParent, canvas, resultParent);

  const model = await loadLayersModel('/mnist_conv_2/mnist_trained_model.json');
}
