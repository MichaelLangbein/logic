import * as tf from '@tensorflow/tfjs';
import '@tensorflow/tfjs-backend-webgl';
// import '@tensorflow/tfjs-backend-webgpu';
import * as mobilenet from '@tensorflow-models/mobilenet';

function loadData(trainingDataSize: number): { xs: tf.Tensor[]; ys: tf.Tensor } {
    throw new Error('Function not implemented.');
}

async function loadNet(nrClasses: number) {
    // const model = await mobilenet.load({version:2, alpha: 0.5});
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

async function train(truncatedMobileNet: tf.LayersModel, customHead: tf.Sequential) {
    // Creates the optimizers which drives training of the model.
    const optimizer = tf.train.adam(0.1);

    // We use categoricalCrossentropy which is the loss function we use for
    // categorical classification which measures the error between our predicted
    // probability distribution over classes (probability that an input is of each
    // class), versus the label (100% probability in the true class)>
    customHead.compile({ optimizer: optimizer, loss: 'categoricalCrossentropy' });

    const batchSize = 32;
    const epochs = 30;
    const trainingDataSize = 10_000;

    const { xs, ys } = loadData(trainingDataSize);

    // Train the model! Model.fit() will shuffle xs & ys so we don't have to.
    const history = await customHead.fit(xs, ys, {
        batchSize,
        epochs: epochs,
        callbacks: {
            onBatchEnd: async (batch, logs) => {
                console.log('Loss: ' + logs?.loss.toFixed(5));
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
    const { truncatedMobileNet, customHead } = await loadNet(10);
    console.log({ backend: tf.getBackend() });
    await train(truncatedMobileNet, customHead);
    const prediction = await predict(truncatedMobileNet, customHead, tf.browser.fromPixels(img));
    console.log(prediction);
}
