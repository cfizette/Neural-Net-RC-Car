# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 21:27:44 2017

@author: Cody Fizette
"""


import numpy as np
import pandas as pd
import os
import uuid


folder = 'track_type2/training_images3'

def move_images(labels = None):
    
    if labels is None:
        labels = np.load(folder + '/labels.npy')
        
    left_dir = folder + '/left'
    right_dir = folder + '/right'
    straight_dir = folder + '/straight'
    
    # Make folders if needed
    if not os.path.exists(left_dir):
        os.makedirs(left_dir)
    
    if not os.path.exists(right_dir):
        os.makedirs(right_dir)
    
    if not os.path.exists(straight_dir):
        os.makedirs(straight_dir)
        
      
    # Move the files
    for file in os.listdir(folder):
        if file.endswith('.jpg'):
            index = int(os.path.splitext(os.path.basename(file))[0])
            #print(index)
          
            if labels[index-1] == 0:
                os.rename(folder + '/' + file, left_dir + '/' + str(uuid.uuid4()) + '.jpg')
                #print(index)
                
            elif labels[index-1] == 1:
               os.rename(folder + '/' + file, right_dir + '/' + str(uuid.uuid4()) + '.jpg')
                #print(index)
                
            elif labels[index-1] == 2:
               os.rename(folder + '/' + file, straight_dir + '/' + str(uuid.uuid4()) + '.jpg')
                #print(index)
              
          
      
    
          

move_images()
