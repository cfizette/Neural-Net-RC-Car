# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 21:27:44 2017

@author: Cody Fizette
"""


import numpy as np
import pandas as pd
import os
import uuid



def move_images(labels = None):
    
    if labels is None:
        labels = np.load('training_images/labels.npy')
        
    left_dir = 'training_images/left'
    right_dir = 'training_images/right'
    straight_dir = 'training_images/straight'
    
    # Make folders if needed
    if not os.path.exists(left_dir):
        os.makedirs(left_dir)
    
    if not os.path.exists(right_dir):
        os.makedirs(right_dir)
    
    if not os.path.exists(straight_dir):
        os.makedirs(straight_dir)
        
      
    # Move the files
    for file in os.listdir('training_images'):
        if file.endswith('.jpg'):
            index = int(os.path.splitext(os.path.basename(file))[0])
            #print(index)
          
            if labels[index-1] == 0:
                os.rename('training_images/' + file, left_dir + '/' + str(uuid.uuid4()) + '.jpg')
                #print(index)
                
            elif labels[index-1] == 1:
               os.rename('training_images/' + file, right_dir + '/' + str(uuid.uuid4()) + '.jpg')
                #print(index)
                
            elif labels[index-1] == 2:
               os.rename('training_images/' + file, straight_dir + '/' + str(uuid.uuid4()) + '.jpg')
                #print(index)
              
          
      
    
          
    
    
