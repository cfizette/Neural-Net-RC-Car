# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 17:34:47 2017

@author: Cody Fizette
"""

import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D, BatchNormalization
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import plot_model
import matplotlib.pyplot as plt
from scipy import misc
from skimage import io


image_width = 320
image_height = 120

model = Sequential()

model.add(Flatten(input_shape=(image_height,image_width,1)))


model.add(Dense(units=128, activation='relu'))

model.add(Dense(units=32, activation='relu'))

model.add(Dense(units=3, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


# Data Generators
train_dir = 'training_images'
validation_dir = 'test_images'
batch_size = 10

train_datagen = ImageDataGenerator(rescale=1./255)

test_datagen = ImageDataGenerator(rescale=1./255)

training_set = train_datagen.flow_from_directory(train_dir,
                                                 target_size=(image_height,image_width),
                                                 batch_size=batch_size,
                                                 color_mode='grayscale',
                                                 shuffle=True)

test_set = test_datagen.flow_from_directory(validation_dir,
                                                 target_size=(image_height,image_width),
                                                 batch_size=batch_size,
                                                 color_mode='grayscale',
                                                 shuffle=True)


# Start Training
hist = model.fit_generator(
        training_set,
        steps_per_epoch=40,
        epochs=75,
        verbose=1,
        validation_data=test_set,
        validation_steps=10)



# Plot performance
plt.plot(hist.history['loss'], color='b')
plt.plot(hist.history['val_loss'], color='r')
plt.show()
plt.plot(hist.history['acc'], color='b')
plt.plot(hist.history['val_acc'], color='r')
plt.show()


