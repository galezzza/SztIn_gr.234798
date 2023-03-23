import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
import cv2




directory = "C:/Users/KimD/PycharmProjects/Traktor_V1/Vegetable Images/test"

test_ds = tf.keras.utils.image_dataset_from_directory(directory, validation_split=0.2, image_size=(224, 224),
                                                      subset="validation", seed=123, batch_size=32)

model = keras.models.load_model("C:/Users/KimD/PycharmProjects/Traktor_V1/mode2.h5")
# predictions = model.predict(test_ds.take(32))
class_names = test_ds.class_names


img = cv2.imread('C:/Users/KimD/PycharmProjects/Traktor_V1/Vegetable Images/test/Carrot/1001.jpg')
cv2.imshow("lala", img)
cv2.waitKey(0)
img = (np.expand_dims(img, 0))
print(class_names)
predictions = model.predict(img)
print(predictions)



