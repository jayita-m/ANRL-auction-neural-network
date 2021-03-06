# -*- coding: utf-8 -*-
"""jay_model_ANRL.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SODont-6r1SaJ4pv72824Tdq8uFM3j7o
"""

import tensorflow as tf
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import pathlib
import io
from keras import models, layers, optimizers, regularizers
import math
import random

import PIL
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from google.colab import files
  
uploaded = files.upload()

df_train = pd.read_csv(io.BytesIO(uploaded['jay_input.csv']), sep=',', index_col=0)
df_train.head(41)

n_test = int(math.ceil(len(df_train) * 0.3))
random.seed(42)
test_ixs = random.sample(list(range(len(df_train))), n_test)
train_ixs = [ix for ix in range(len(df_train)) if ix not in test_ixs]
train = df_train.iloc[train_ixs, :]
test = df_train.iloc[test_ixs, :]
print(len(train))
print(len(test))

features = ['bid_p'] #stuff to train
response = 'chance' #label to train over (chance max)
x_train = train[features]
y_train = train[response]
x_test = test[features]
y_test = test[response]

#Assignment system - decides winner 
hidden_units = 10     # how many neurons in the hidden layer
activation = 'sigmoid'   # activation function for hidden layer
l2 = 0.01             # regularization - how much we penalize large parameter values
learning_rate = 0.01  # how big our steps are in gradient descent
epochs = 5            # how many epochs to train for
batch_size = 3       # how many samples to use for each gradient descent update

# create a sequential model
model = models.Sequential()

# add the hidden layer
model.add(layers.Dense(input_dim=len(features), units=hidden_units, 
                       activation=activation))

# add the output layer
model.add(layers.Dense(input_dim=hidden_units, units=1,
                       activation='sigmoid'))

# define our loss function and optimizer
model.compile(loss='binary_crossentropy',
              # Adam is a kind of gradient descent
              optimizer=optimizers.Adam(lr=learning_rate),
              metrics=['accuracy'])

# train the parameters
history = model.fit(x_train, y_train, epochs=10, batch_size=batch_size)

train_acc = model.evaluate(x_train, y_train, batch_size=32)[1]

test_acc = model.evaluate(x_test, y_test, batch_size=32)[1]

print('Training accuracy: %s' % train_acc)
print('Testing accuracy: %s' % test_acc)

losses = history.history['loss']
plt.plot(range(len(losses)), losses, 'r')
plt.show()

predictions = model.predict([44, 12, 23, 1, 98]) #These are very basic examples of bids 

# Print our model's predictions.
print(predictions)