import numpy as np

images = np.load("images.npy")
labels = np.load("labels.npy")

n = len(labels)

idx = np.arange(n)
np.random.shuffle(idx)

shuffled_images = images[idx]
shuffled_labels = labels[idx]

train_images = shuffled_images[:int(0.8*n)]
train_labels = shuffled_labels[:int(0.8*n)]

val_images = shuffled_images[int(0.8*n):]
val_labels = shuffled_labels[int(0.8*n):]

np.save("train_images.npy", train_images)
np.save("train_labels.npy", train_labels)
np.save("val_images.npy", val_images)
np.save("val_labels.npy", val_labels)
