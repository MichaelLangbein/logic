import { layers, model, Rank, Tensor } from '@tensorflow/tfjs';

function createUpSampleBlock(nrFilters: number, input: Tensor) {
  const relu_1 = layers.activation({ activation: 'relu' }).apply(input);
  const conv_1 = layers.separableConv2d({ filters: nrFilters, kernelSize: 3, padding: 'same' }).apply(relu_1);
  const norm_1 = layers.batchNormalization({}).apply(conv_1);
  const relu_2 = layers.activation({ activation: 'relu' }).apply(norm_1);
  const conv_2 = layers.separableConv2d({ filters: nrFilters, kernelSize: 3, padding: 'same' }).apply(relu_2);
  const norm_2 = layers.batchNormalization({}).apply(conv_2);
  const maxp_1 = layers.maxPool2d({ poolSize: 3, strides: 2, padding: 'same' }).apply(norm_2);
  const residual = layers.conv2d({ filters: nrFilters, kernelSize: 1, strides: 2, padding: 'same' }).apply(input);
  const output = layers.add({}).apply([residual, maxp_1] as Tensor<Rank>[]);
  return output;
}

function createDownSampleBlock(nrFilters: number, input: Tensor) {
  const relu_1 = layers.activation({ activation: 'relu' }).apply(input);
  const conv_1 = layers.conv2dTranspose({ filters: nrFilters, kernelSize: 3, padding: 'same' }).apply(relu_1);
  const norm_1 = layers.batchNormalization({}).apply(conv_1);
  const relu_2 = layers.activation({ activation: 'relu' }).apply(norm_1);
  const conv_2 = layers.conv2dTranspose({ filters: nrFilters, kernelSize: 3, padding: 'same' }).apply(relu_2);
  const norm_2 = layers.batchNormalization({}).apply(conv_2);
  const upsp_1 = layers.upSampling2d({}).apply(norm_2);
  const residual_1 = layers.upSampling2d({}).apply(input);
  const residual_2 = layers.conv2d({ filters: nrFilters, kernelSize: 1, padding: 'same' }).apply(residual_1);
  const output = layers.add({}).apply([residual_2, upsp_1] as Tensor<Rank>[]);
  return output;
}

function createUnet(num_classes: number) {
  const inputs = layers.input({ shape: [256, 256, 3] });

  // Entry block
  const conv_0 = layers.conv2d({ filters: 32, kernelSize: 2, padding: 'same' }).apply(inputs);
  const norm_0 = layers.batchNormalization({}).apply(conv_0);
  const block_0 = layers.activation({ activation: 'relu' }).apply(norm_0);

  // up-sampling
  const block_1 = createUpSampleBlock(64, block_0 as Tensor<Rank>);
  const block_2 = createUpSampleBlock(128, block_1 as Tensor<Rank>);
  const block_3 = createUpSampleBlock(256, block_2 as Tensor<Rank>);

  // down-sampling
  const block_4 = createDownSampleBlock(256, block_3 as Tensor<Rank>);
  const block_5 = createDownSampleBlock(128, block_4 as Tensor<Rank>);
  const block_6 = createDownSampleBlock(64, block_5 as Tensor<Rank>);
  const block_7 = createDownSampleBlock(32, block_6 as Tensor<Rank>);

  // outputs
  const outputs: any = layers
    .conv2d({ filters: num_classes, kernelSize: 3, padding: 'same', activation: 'softmax' })
    .apply(block_7);

  const unet = model({ inputs, outputs });
  return unet;
}

export async function run() {
  const unet = createUnet(5);
  console.log(unet.summary());
}
