"""
Matthew Traino
Naive-Bayes classier
Python 3.6.7
"""
# imports
import numpy as np
import matplotlib.pyplot as plt
import ipdb
from sklearn.metrics import confusion_matrix

# Load data from relevant files
print("loading training data...")
xtrain = np.loadtxt('trainingdata.txt', dtype=int)
print("loading training labels...")
ytrain = np.loadtxt('traininglabels.txt', dtype=int)
print("loading testing data...")
xtest = np.loadtxt('testingdata.txt', dtype=int)
print("loading testing labels...")
ytest = np.loadtxt('testinglabels.txt', dtype=int)
print("loading newsgroups...")
newsgroups = np.loadtxt('newsgroups.txt', dtype=str)
print("loading vocabulary...")
vocabulary = np.loadtxt('vocabulary.txt', dtype=str)

# Change 1-indexing to 0
xtrain[:, 0:2] -= 1
ytrain -= 1
xtest[:, 0:2] -= 1
ytest -= 1

# Extract useful parameters
num_training_documents = len(ytrain)
num_testing_documents = len(ytest)
num_words = len(vocabulary)
num_newsgroups = len(newsgroups)

print("\n=======================")
print("TRAINING")
print("=======================")

# Estimate the prior probabilities
print("Estimating prior probabilities via MLE...")
priors = np.bincount(ytrain) / num_training_documents

# Estimate the class conditional probabilities
print("Estimating class conditional probabilities via MAP...")
class_conditionals = np.zeros((num_words, num_newsgroups))
rows = xtrain[:, 1].tolist()
cols = ytrain[xtrain[:, 0]].tolist()
np.add.at(class_conditionals, (rows, cols), xtrain[:, 2])
alpha = (1 / num_words)
class_conditionals += alpha
class_conditionals /= np.sum(class_conditionals, 0)

print("\n=======================")
print("TESTING")
print("=======================")

# Test the Naive Bayes classifier
print("Applying natural log to prevent underflow...")
log_priors = np.log(priors)
log_class_conditionals = np.log(class_conditionals)

print("Counting words in each document...")
counts = np.zeros((num_testing_documents, num_words))
rows = xtest[:, 0].tolist()
cols = xtest[:, 1].tolist()
np.add.at(counts, (rows, cols), xtest[:, 2])

print("Computing posterior probabilities...")
log_posterior = np.matmul(counts, log_class_conditionals)
log_posterior += log_priors

print("Assigning predictions via argmax...")
pred = np.argmax(log_posterior, 1)

print("\n=======================")
print("PERFORMANCE METRICS")
print("=======================")

# Compute performance metrics
accuracy = np.mean(ytest == pred)
print("Accuracy: {0:d}/{1:d} ({2:0.1f}%)".format(sum(ytest == pred), num_testing_documents, accuracy * 100))
cm = confusion_matrix(ytest, pred)
print("Confusion matrix:")
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in cm]))
