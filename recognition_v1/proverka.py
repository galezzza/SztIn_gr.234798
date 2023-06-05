import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
import cv2

directory = "C:/Users/KimD/PycharmProjects/Traktor_V1/Vegetable Images/test"


class VegebatlesRecognizer:

    model = keras.models.load_model("C:/Users/KimD/PycharmProjects/sztin_gr.234798/recognition_v1/mode1.h5")
    def recognize(self, image_path) -> str:
        class_names = ['Broccoli', 'Capsicum', 'Carrot', 'Potato']

        img = cv2.imread(image_path)
        # cv2.imshow("lala", img)
        # cv2.waitKey(0)
        img = (np.expand_dims(img, 0))

        predictions = self.model.predict(img)[0].tolist()

        # print(class_names)
        # print(predictions)
        # print(max(predictions))
        # print(predictions.index(max(predictions)))

        return class_names[predictions.index(max(predictions))]


# image_path = 'C:/Users/KimD/PycharmProjects/Traktor_V1/Vegetable Images/test/Carrot/1001.jpg'
# uio = VegebatlesRecognizer()
# print(uio.recognize(image_path))
