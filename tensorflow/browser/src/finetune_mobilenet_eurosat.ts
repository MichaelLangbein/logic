// demo: https://storage.googleapis.com/tfjs-examples/mobilenet/dist/index.html
// load mobilenet: https://github.com/tensorflow/tfjs-examples/blob/master/mobilenet/index.js
// finetuning aka transfer-learning: https://github.com/tensorflow/tfjs-examples/tree/master/webcam-transfer-learning

import * as tf from '@tensorflow/tfjs';
import '@tensorflow/tfjs-backend-webgl';
// import '@tensorflow/tfjs-backend-webgpu';
import * as mobilenet from '@tensorflow-models/mobilenet';

// async function loadTruncatedMobileNet() {
//     const model = await mobilenet.load({version:2, alpha: 0.5});
//     const layer = model.getLayer('conv_pw_13_relu');
//     return tf.model({inputs: model.inputs, outputs: layer.output});
//   }

async function loadNet(nrClasses: number) {
    const mnet = await tf.loadLayersModel(
        'https://storage.googleapis.com/tfjs-models/tfjs/mobilenet_v1_0.25_224/model.json'
    );

    // Return a model that outputs an internal activation.
    const layer = mnet.getLayer('conv_pw_13_relu');
    const truncatedMobileNet = tf.model({ inputs: mnet.inputs, outputs: layer.output });

    // Creates a 2-layer fully connected model. By creating a separate model,
    // rather than adding layers to the mobilenet model, we "freeze" the weights
    // of the mobilenet model, and only train weights from the new model.
    const customHead = tf.sequential({
        layers: [
            // Flattens the input to a vector so we can use it in a dense layer. While
            // technically a layer, this only performs a reshape (and has no training
            // parameters).
            tf.layers.flatten({ inputShape: truncatedMobileNet.outputs[0].shape.slice(1) }),
            // Layer 1.
            tf.layers.dense({
                units: 516,
                activation: 'relu',
                kernelInitializer: 'varianceScaling',
                useBias: true,
            }),
            // Layer 2. The number of units of the last layer should correspond
            // to the number of classes we want to predict.
            tf.layers.dense({
                units: nrClasses,
                kernelInitializer: 'varianceScaling',
                useBias: false,
                activation: 'softmax',
            }),
        ],
    });

    return { truncatedMobileNet, customHead };
}

function train(truncatedMobileNet: tf.LayersModel, customHead: tf.Sequential) {
    // Creates the optimizers which drives training of the model.
    const optimizer = tf.train.adam(0.1);
    // We use categoricalCrossentropy which is the loss function we use for
    // categorical classification which measures the error between our predicted
    // probability distribution over classes (probability that an input is of each
    // class), versus the label (100% probability in the true class)>
    customHead.compile({ optimizer: optimizer, loss: 'categoricalCrossentropy' });

    // We parameterize batch size as a fraction of the entire dataset because the
    // number of examples that are collected depends on how many examples the user
    // collects. This allows us to have a flexible batch size.
    const batchSize = Math.floor(controllerDataset.xs.shape[0] * ui.getBatchSizeFraction());
    if (!(batchSize > 0)) {
        throw new Error(`Batch size is 0 or NaN. Please choose a non-zero fraction.`);
    }

    // Train the model! Model.fit() will shuffle xs & ys so we don't have to.
    customHead.fit(controllerDataset.xs, controllerDataset.ys, {
        batchSize,
        epochs: ui.getEpochs(),
        callbacks: {
            onBatchEnd: async (batch, logs) => {
                ui.trainStatus('Loss: ' + logs.loss.toFixed(5));
            },
        },
    });
}

async function predict(truncatedMobileNet: tf.LayersModel, customHead: tf.Sequential, img: tf.Tensor) {
    // Make a prediction through mobilenet, getting the internal activation of
    // the mobilenet model, i.e., "embeddings" of the input images.
    const embeddings = truncatedMobileNet.predict(img);

    // Make a prediction through our newly-trained model using the embeddings
    // from mobilenet as input.
    const prediction = customHead.predict(embeddings) as tf.Tensor;

    const predictionData = await prediction.data();
    return predictionData;
}

export async function run() {
    // await tf.setBackend("webgpu");
    const img = document.getElementById('image') as HTMLImageElement;
    const model = await mobilenet.load({ version: 2, alpha: 0.5 });
    console.log({ backend: tf.getBackend() });
    const predictions = await model.classify(img);
    console.log(predictions);
}
