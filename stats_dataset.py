import cv2
import numpy as np
import matplotlib.pyplot as plt

images = np.load('val_images.npy')
labels = np.load('val_labels.npy')

N = len(labels)

print(f"devant : {np.sum(np.where(labels == 0, 1, 0))/N}")
print(f"gauche : {np.sum(np.where(labels == 1, 1, 0))/N}")
print(f"droite : {np.sum(np.where(labels == 2, 1, 0))/N}")
