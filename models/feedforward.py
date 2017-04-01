import tflearn
import numpy as np
import tensorflow as tf


# Data
n = 100
X_data = np.random.rand(n, 3)
Y_data = np.dot(X_data, [[1, 1, 1], [1, 1, 0], [1, 1, 1]]) + [1, 1, 1]

# Input
X = tflearn.input_data(shape=[None, 3], name="X")
Y = tflearn.input_data(shape=[None, 3], name="Y")

# Network
Y_pred = tflearn.fully_connected(
    X, 3, weights_init='uniform', bias_init="zeros",
    activation='sigmoid', name="network"
)
Y_pred = tf.identity(Y_pred, name="Y_pred")

# Optimization
net = tflearn.regression(
    Y_pred, optimizer=tflearn.SGD(learning_rate=1), loss="mean_square"
)

# Training
model = tflearn.DNN(net)
model.fit(X_data, Y_data, n_epoch=1)
