# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 00:59:59 2017

@author: Cody Fizette
"""

import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D, BatchNormalization
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import plot_model

image_width = 320
image_height = 240


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




















