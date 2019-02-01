"""
Matthew Traino
Handwritten digit recognition
Use a neural network for simple hand written number classification.
Python 3.6.7
"""

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import ipdb

# Loading the data
(training_data, training_labels), (testing_data, testing_labels) = mnist.load_data()

# Setting the seed
np.random.seed(3520)

# Setting variables
num_classes = 10
batch_size = 100
epochs = 100
num_inputs = training_data.shape
learning_rate = 0.02

# Converting the labels from 0-9 to their binary form
training_labels = keras.utils.to_categorical(training_labels)
testing_labels_binary = keras.utils.to_categorical(testing_labels)

# Reshaping the data
training_data.shape = (60000, 784)
testing_data.shape = (10000, 784)

# Creating the neural network
# Adding the layers in a 784-300-10 model with relu for the layer's activations and softmax for the output
model = Sequential()
model.add(Dense(units=300, activation='relu', input_dim=784))
model.add(Dense(units=300, activation='relu'))
model.add(Dense(units=num_classes, activation='softmax'))
model.summary()
sgd = keras.optimizers.SGD(lr=learning_rate)
model.compile(loss='mean_squared_error', optimizer=sgd, metrics=['accuracy'])

# Training the model
training = model.fit(training_data, training_labels,
            batch_size=batch_size,
            epochs=epochs,
            verbose=2,
            validation_data=(testing_data, testing_labels_binary))
score = model.evaluate(training_data, training_labels, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

# Plotting accuracy by epochs
Y = np.arange(0, 1, .05)  # array of all the numbers between 0 and 1 with .05 increments
X = np.arange(0, epochs, 9)  # array of all the numbers between 0 and the number of epochs run incrementing by 10s
plt.title('Accuracy vs Epochs')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.yticks(Y)
plt.xticks(X)
plt.plot(training.history['acc'])
plt.show()

pred = model.predict(testing_data)
pred = np.argmax(pred, axis=1)
b = confusion_matrix(testing_labels, pred)
print("Confusion matrix")
print(b)

#ipdb.set_trace()
