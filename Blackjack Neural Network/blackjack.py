# blackjack.py
# A neural network designed to play the blackjack vs the dealer with the options of Hit or Stand

# Import needed packages
import numpy as np
import ipdb
import keras
from keras import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

# Setting the seed
np.random.seed(3520)

# Setting variables
batch_size = 1000
epochs = 1500
learning_rate = 0.001
filename = 'blackjack.h5'

# Loading in the data and labels
training_data = np.loadtxt('TrainingData.txt', dtype=int, delimiter=' ')
training_labels = np.loadtxt('TrainingLabels.txt')
testing_data = np.loadtxt('TestingData.txt', dtype=int)
testing_labels = np.loadtxt('TestingLabels.txt')
testing_labels.shape = (-1, 1)

# Creating the neural network 104-100-100-256-1
model = Sequential()
model.add(Dense(units=100, activation='sigmoid', input_dim=104))
model.add(Dense(units=100, activation='sigmoid'))
model.add(Dense(units=256, activation='sigmoid'))
model.add(Dense(units=1, activation='relu'))
model.summary()
sgd = keras.optimizers.SGD(lr=learning_rate)
model.compile(loss='mean_squared_error', optimizer=sgd, metrics=['accuracy'])

# Training the neural network 104-100-100-1
training = model.fit(training_data, training_labels,
            batch_size=batch_size,
            epochs=epochs,
            verbose=2)

score = model.evaluate(training_data, training_labels, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

# Saving the model
model.save(filename)

pred = model.predict(testing_data, batch_size=100, verbose=2)
Y = np.zeros(pred.shape)
Y[pred < .5] = 0
Y[pred >= .5] = 1

# Confusion matrix
c = confusion_matrix(testing_labels, Y)
print("Confusion matrix")
print(c)

# Plotting accuracy as trained from epochs
plt.title('Training Accuracy vs Epochs')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.plot(training.history['acc'])
plt.show()
