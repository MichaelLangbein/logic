import { browser, loadLayersModel, Rank, Tensor } from '@tensorflow/tfjs';

interface Point {
  x: number;
  y: number;
}

/**
 * Function takes a UInt8ClampedArray as input and returns a tfjs tensor of dimension [1, 28, 28, 1]
 * input data: [r,g,b,a,  r,g,b,a,  r,g,b,a, ....]
 */
function uint8ToTensor(data: HTMLImageElement): Tensor<Rank> {
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

function getSample(container: HTMLImageElement, samplePoint: Point): Tensor<Rank> {
  const imgData = browser.fromPixels(container);
  const sampleData = imgData.slice([samplePoint.x, samplePoint.y, 0], [64, 64, 3]);
  return sampleData.reshape([1, 64, 64, 3]);
}

export async function run() {
  const container1 = document.getElementById('displayNet')!;
  const container2 = document.getElementById('displayTraining')!;
  const image = document.getElementById('image') as HTMLImageElement;

  const model = await loadLayersModel('/sentinel2_cnn_oldstyle/model.json');
  console.log(model.summary());

  const sample = getSample(image, { x: image.width / 2, y: image.height / 2 });
  const prediction = model.predict(sample) as Tensor<Rank>;
  console.log(prediction.arraySync());
}
