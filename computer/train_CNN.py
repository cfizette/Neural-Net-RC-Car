# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 00:59:59 2017

@author: Cody Fizette
"""
'''
Recommend to use Spyder when running code.
'''

# Import required modules
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

# Image parameters
image_width = 320
image_height = 240

# Build model archetecture
model = Sequential()
# Convolutional layer followed by max pool
model.add(Conv2D(kernel_size=(3,3), filters=32, input_shape=(image_height,image_width,1), activation='relu'))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))
# Convolutional layer followed by max pool
model.add(Conv2D(kernel_size=(3,3), filters=64, activation='relu'))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))
# Dropout layer
model.add(Dropout(0.5))
# Flatten layer to connect to ANN
model.add(Flatten())
# First layer of ANN
model.add(Dense(units=32, activation='relu'))
# Dropout
model.add(Dropout(0.4))
# Output layer
model.add(Dense(units=3, activation='softmax'))
# Compile model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Set up datagenerators
train_dir = 'track_type2/training_images' # Change to own directory
validation_dir = 'track_type2/test_images'
batch_size = 30
train_datagen = ImageDataGenerator(rescale=1./255,
                                   zoom_range=0.2)
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
        steps_per_epoch=128,
        epochs=75,
        verbose=1,
        validation_data=test_set,
        validation_steps=21)

# Plot performance
plt.plot(hist.history['loss'], color='b')
plt.plot(hist.history['val_loss'], color='r')
plt.show()
plt.plot(hist.history['acc'], color='b')
plt.plot(hist.history['val_acc'], color='r')
plt.show()

# Make some predictions
preds = model.predict_generator(test_set,20)
preds = preds.round()

# Test on individual images
model = load_model('test_model_1.h5')
image = io.imread('test_images/straight/0cff6cf9-6544-4c6b-b516-8a4dbc6521f4.jpg', as_grey=True)
image = np.resize(image, (image_height, image_width, 1))
image = np.expand_dims(image, axis=0)
image = image/255
model.predict(image, batch_size=1).round()





