import { getBackend, layers, model } from '@tensorflow/tfjs-node-gpu';

const layer0 = layers.input({ shape: [2] });
const layer1 = layers.dense({ units: 4 }).apply(layer0);
const layer2 = layers.dense({ units: 4 }).apply(layer1);
const layer3 = layers.dense({ units: 2 }).apply(layer2);
const mdl = model({ inputs: layer0, outputs: layer3 as any });

console.log(mdl.summary());
console.log(getBackend());
