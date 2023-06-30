import numpy as np
import matplotlib.pyplot as plt
from create_and_train_model import create_model

train_images = np.load('train_images.npy')
train_labels = np.load('train_labels.npy')

model = create_model('CNN_3_layers', num_classes=3)

model.load_weights('models/CNN_32_64_128_128.h5')

for i in range(len(train_images)):
    print(train_labels[i], np.argmax(
        model(np.array([train_images[i]])).numpy()[0]))
    plt.imshow(train_images[i])
    plt.show()
