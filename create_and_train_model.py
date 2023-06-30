import tensorflow as tf
import tensorflow.keras as keras
import numpy as np
import matplotlib.pyplot as plt


def create_model(model_type, num_classes=5, input_shape=(32, 32, 3)):
    if model_type == 'CNN_3_layers':
        model = keras.Sequential([
            keras.layers.Conv2D(32, 3, padding='same',
                                activation='relu', input_shape=input_shape),
            keras.layers.MaxPool2D(),
            keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
            keras.layers.MaxPool2D(),
            keras.layers.Conv2D(128, 3, padding='same', activation='relu'),
            keras.layers.MaxPool2D(),
            keras.layers.Flatten(),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dense(num_classes, activation='softmax')
        ])

    elif model_type == 'Dense':
        model = keras.Sequential([
            keras.layers.Flatten(input_shape=input_shape),
            keras.layers.Dense(512, activation='relu',
                               kernel_regularizer=keras.regularizers.L2()),
            keras.layers.Dropout(0.5),
            keras.layers.Dense(64, activation='relu',
                               kernel_regularizer=keras.regularizers.L2()),
            keras.layers.Dropout(0.5),
            keras.layers.Dense(num_classes, activation='softmax',
                               kernel_regularizer=keras.regularizers.L2())
        ])

    return(model)


def train_model(model: keras.Model, epochs):

    train_images = np.load("train_images.npy")/128 - 1
    train_labels = np.load("train_labels.npy")
    val_images = np.load("val_images.npy")/128 - 1
    val_labels = np.load("val_labels.npy")

    return model.fit(train_images, train_labels, epochs=epochs, validation_data=(val_images, val_labels), batch_size=16)


def run(model_name):
    model = create_model(model_type='CNN_3_layers', num_classes=3,
                         input_shape=(32, 32, 3))

    model.compile(optimizer=keras.optimizers.Adam(
        0.0001), loss=keras.losses.SparseCategoricalCrossentropy(), metrics='accuracy')

    model.summary()

    history = train_model(model, epochs=10)

    model.save(rf'models/{model_name}')
    model.save_weights(f'models/{model_name}.h5')
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()

    with open(f'models/{model_name}.tflite', 'wb') as f:
        f.write(tflite_model)
    plt.plot(history.history['accuracy'], label='accuracy')
    plt.plot(history.history['val_accuracy'], label='val_accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.ylim([0, 1])
    plt.legend(loc='lower right')
    plt.show()

    plt.plot(history.history['loss'], label='loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend(loc='lower right')
    plt.show()


if __name__ == '__main__':
    run('CNN_32_64_128_128')
