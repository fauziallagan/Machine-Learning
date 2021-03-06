# -*- coding: utf-8 -*-
"""Submission ML.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aoWEjOui128celZiuXEIZASGNHvT4jjQ
"""

import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator

!wget --no-check-certificate \\
https://dicodingacademy.blob.core.windows.net/picodiploma/ml_pemula_academy/rockpaperscissors.zip \\
-O /tmp/rockpaperscissors.zip

import zipfile,os
local_zip = '/tmp/rockpaperscissors.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/tmp')
zip_ref.close()

!pip install split_folders

import splitfolders
origin_path = '/tmp/rockpaperscissors/rps-cv-images'
output_path = '/tmp/rockpaperscissors/hasil_split'
splitfolders.ratio(origin_path, output=output_path, seed=1337, ratio=(.8, .2))

base_dir = '/tmp/rockpaperscissors/hasil_split'
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'val')

# Train
train_paper_dir = os.path.join(train_dir, 'paper')
train_scissors_dir = os.path.join(train_dir, 'scissors')
train_rock_dir = os.path.join(train_dir, 'rock')
# Validation
validation_paper_dir = os.path.join(validation_dir, 'paper')
validation_scissors_dir = os.path.join(validation_dir, 'scissors')
validation_rock_dir = os.path.join(validation_dir, 'rock')

train_datagen = ImageDataGenerator(
                    rescale=1/255,
                    rotation_range=20,
                    horizontal_flip=True,
                    shear_range = 0.2,
                    fill_mode = 'nearest')
test_datagen = ImageDataGenerator(
                    rescale=1/255,
                    rotation_range=20,
                    horizontal_flip=True,
                    shear_range = 0.2,
                    fill_mode = 'nearest')

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(150, 150),
    batch_size=4,
    class_mode='categorical')
validation_generator = test_datagen.flow_from_directory(
    validation_dir,
    target_size=(150, 150),
    batch_size=4,
    class_mode='categorical')

model = tf.keras.models.Sequential([
          tf.keras.layers.Conv2D(32, (3,3), padding='same', activation='relu',
                                input_shape=(150, 150, 3)),
          tf.keras.layers.MaxPooling2D(),
          tf.keras.layers.Dropout(0.2),
          tf.keras.layers.Conv2D(32, 3, padding='same', activation='relu'),
          tf.keras.layers.MaxPooling2D(),
          tf.keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
          tf.keras.layers.MaxPooling2D(),
          tf.keras.layers.Dropout(0.2),
          tf.keras.layers.Flatten(),
          tf.keras.layers.Dense(512, activation='relu'),
          tf.keras.layers.Dense(3, activation='softmax')
                                 
])

model.compile(loss='categorical_crossentropy',
              optimizer=tf.optimizers.Adam(),
              metrics=['accuracy', 'mae'])
model.summary()

class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy') > 0.9):
      print('\n====================== Input telah tercapai!! ===========================\n')
      self.model.stop_training = True
callbacks = myCallback()

result = model.fit(
                train_generator,
                steps_per_epoch=45,
                epochs=100,
                validation_data=validation_generator,
                validation_steps=3,
                verbose=2,
                callbacks=[callbacks])

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
from google.colab import files
from keras.preprocessing import image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# %matplotlib inline

uploaded = files.upload()

for fn in uploaded.keys():
  #predic
  path = fn
  img = image.load_img(path, target_size=(150, 150))
  imgplot = plt.imshow(img)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
  images = np.vstack([x])
  classes = model.predict(images, batch_size=10)

  print(fn)
  hasil = np.argmax(classes)
  if classes[0][0]==1:
    print('paper')
  elif classes[0][1]==1:
    print('rock')
  elif classes[0][2]==1:
    print('scissors')
  else:
    print('error!')

print(train_generator.class_indices)

#accuracy
plt.plot(result.history['accuracy'])
plt.title('Model accuracy')
plt.xlabel('Accuracy')
plt.ylabel('Epoch')
plt.legend(['Trainning'], loc='lower right')
plt.show()

#loss
plt.plot(result.history['loss'])
plt.title('Model loss')
plt.xlabel('Loss')
plt.ylabel('Epoch')
plt.legend(['Trainning'], loc='upper right')
plt.show()

#Val_loss
plt.plot(result.history['val_loss'])
plt.title('Model val_loss')
plt.xlabel('Val_loss')
plt.ylabel('Epoch')
plt.legend(['Trainning'], loc='upper right')
plt.show()

#Val_Accuracy
plt.plot(result.history['val_accuracy'])
plt.title('Model val_accuracy')
plt.xlabel('Val_accuracy')
plt.ylabel('Epoch')
plt.legend(['Trainning'], loc='upper right')
plt.show()

#mae
plt.plot(result.history['mae'])
plt.title('Model mae')
plt.xlabel('Mae')
plt.ylabel('Epoch')
plt.legend(['Trainning'], loc='upper right')
plt.show()
