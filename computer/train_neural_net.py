# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 00:59:59 2017

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

model.add(Conv2D(kernel_size=(5,5), filters=16, input_shape=(image_height,image_width,1), activation='relu'))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))

model.add(Conv2D(kernel_size=(3,3), filters=32, activation='relu'))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))

model.add(Dropout(0.5))

model.add(Flatten())

model.add(Dense(units=16, activation='relu'))

model.add(Dropout(0.5))

model.add(Dense(units=3, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


# Set up datagenerators
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



preds = model.predict_generator(test_set,20)
preds = preds.round()






 


# Test on individual images
model = load_model('test_model_1.h5')

image = io.imread('test_images/straight/0cff6cf9-6544-4c6b-b516-8a4dbc6521f4.jpg', as_grey=True)
image = np.resize(image, (image_height, image_width, 1))
image = np.expand_dims(image, axis=0)
image = image/255
model.predict(image, batch_size=1).round()





