import numpy as np
import tensorflow as tf
from tensorflow import keras


def normalize(image, label):
    return image / 255, label


directoryTRAIN = "C:/Users/KimD/PycharmProjects/Traktor_V1/Vegetable Images/train"
directoryVALIDATION = "C:/Users/KimD/PycharmProjects/Traktor_V1/Vegetable Images/validation"

train_ds = tf.keras.utils.image_dataset_from_directory(directoryTRAIN,
                                                       seed=123, batch_size=32,
                                                       image_size=(224, 224), color_mode='rgb')

val_ds = tf.keras.utils.image_dataset_from_directory(directoryVALIDATION,
                                                     seed=123, batch_size=32,
                                                     image_size=(224, 224), color_mode='rgb')

train_ds = train_ds.map(normalize)
val_ds = val_ds.map(normalize)

model = keras.Sequential([
    keras.layers.Conv2D(64, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    keras.layers.MaxPool2D((2, 2)),

    keras.layers.Conv2D(128, (3, 3), activation='relu'),
    keras.layers.MaxPool2D((2, 2)),

    keras.layers.Conv2D(256, (3, 3), activation='relu'),
    keras.layers.MaxPool2D((2, 2)),

    keras.layers.Flatten(),
    keras.layers.Dense(1024, activation='relu'),
    keras.layers.Dense(9, activation='softmax')
])

print(model.summary())

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

trainHistory = model.fit(train_ds, epochs=4, validation_data=val_ds)

model = keras.models.load_model("C:/Users/KimD/PycharmProjects/Traktor_V1/mode2.h5")

(loss, accuracy) = model.evaluate(val_ds)
print(loss)
print(accuracy)

# model.save("mode2.h5")
