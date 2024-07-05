import { loadLayersModel } from '@tensorflow/tfjs';

export async function run() {
  const model = await loadLayersModel('/sentinel2_cnn_oldstyle/model.json');
  console.log(model.summary());
}
