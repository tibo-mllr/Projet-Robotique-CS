import cv2
import numpy as np

indices = [552, 1178, 1847, 3075, 4027, 5063, 6672, 7353, 8159, 9242, 11102,
           11896, 12562, 13263, 13742, 15767, 16706, 17607, 18526, 19412, 20175,
           22786, 24759, 25492, 26949, 27572, 28410, 29083, 31088, 31991, 32854,
           34856, 35652, 36326, 37149, 37658, 38485, 40587, 41332, 42097, 43492,
           44914, 45816, 47047]

images = [
    np.load(f'images_{indice}.npy') for indice in indices]
labels = [
    np.load(f'labels_{indice}.npy') for indice in indices]

resized_images = []

for i, image_cluster in enumerate(images):
    print(labels[i][0])
    cv2.imshow(f"cluster_{i}", image_cluster[0])
    for image in image_cluster:
        #image = cv2.resize(image, (32, 32))
        resized_images.append(image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

images = np.stack(resized_images)
labels = np.concatenate(labels)

print(np.shape(images))

np.save('full_sized_images', images / 255)
np.save('full_sized_labels', labels)
