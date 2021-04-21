import numpy as np
import pandas as pd
import pickle
import gzip
import sys
import time
import matplotlib.cm as cm
import matplotlib.pyplot as plt


class NN:
    def __init__(self):
        self.params = {}

    def sigmoid(self, z):
        """
        sigmoid activation function.

        inputs: z
        outputs: sigmoid(z)
        """
        s = 1. / (1. + np.exp(-z))
        return s

    def compute_loss(self, Y, Y_hat):
        """
        compute loss function
        """
        L_sum = np.sum(np.multiply(Y, np.log(Y_hat)))
        m = Y.shape[1]
        L = -(1. / m) * L_sum

        return L

    def feed_forward(self, X):
        """
        feed forward network: 2 - layer neural net

        inputs:
            params: dictionay a dictionary contains all the weights and biases

        return:
            cache: dictionay a dictionary contains all the fully connected units and activations
        """
        cache = {}

        # Z1 = W1.dot(x) + b1
        cache["Z1"] = np.matmul(self.params["W1"], X) + self.params["b1"]

        # A1 = sigmoid(Z1)
        cache["A1"] = self.sigmoid(cache["Z1"])

        # Z2 = W2.dot(A1) + b2
        cache["Z2"] = np.matmul(self.params["W2"], cache["A1"]) + self.params["b2"]

        # A2 = softmax(Z2)
        cache["A2"] = np.exp(cache["Z2"]) / np.sum(np.exp(cache["Z2"]), axis=0)

        return cache

    def back_propagate(self, X, Y, cache, m_batch):
        """
        back propagation

        inputs:
            params: dictionay a dictionary contains all the weights and biases
            cache: dictionay a dictionary contains all the fully connected units and activations

        return:
            grads: dictionay a dictionary contains the gradients of corresponding weights and biases
        """
        # error at last layer
        dZ2 = cache["A2"] - Y

        # gradients at last layer (Py2 need 1. to transform to float)
        dW2 = (1. / m_batch) * np.matmul(dZ2, cache["A1"].T)
        db2 = (1. / m_batch) * np.sum(dZ2, axis=1, keepdims=True)

        # back propgate through first layer
        dA1 = np.matmul(self.params["W2"].T, dZ2)
        dZ1 = dA1 * self.sigmoid(cache["Z1"]) * (1 - self.sigmoid(cache["Z1"]))

        # gradients at first layer (Py2 need 1. to transform to float)
        dW1 = (1. / m_batch) * np.matmul(dZ1, X.T)
        db1 = (1. / m_batch) * np.sum(dZ1, axis=1, keepdims=True)

        return dW1, db1, dW2, db2

    def train(self, X_train, Y_train, learning_tate=0.005, epochs=50, n_h=200, beta=0.9, batch_size=64):
        start_time = time.time()
        # number of inputs
        n_x = X_train.shape[0]
        data_size = X_train.shape[1]
        self.params = {"W1": np.random.randn(n_h, n_x) * np.sqrt(1. / n_x),
                       "b1": np.zeros((n_h, 1)) * np.sqrt(1. / n_x),
                       "W2": np.random.randn(10, n_h) * np.sqrt(1. / n_h),
                       "b2": np.zeros((10, 1)) * np.sqrt(1. / n_h)}

        for i in range(epochs):
            # shuffle training set
            permutation = np.random.permutation(X_train.shape[1])
            X_train_shuffled = X_train[:, permutation]
            Y_train_shuffled = Y_train[:, permutation]

            batches = int(data_size / batch_size)
            for j in range(batches):
                # get mini-batch
                begin = j * batch_size
                end = min(begin + batch_size, X_train.shape[1] - 1)
                X = X_train_shuffled[:, begin:end]
                Y = Y_train_shuffled[:, begin:end]
                m_batch = end - begin

                # forward and backward
                cache = self.feed_forward(X)
                dW1, db1, dW2, db2 = self.back_propagate(X, Y, cache, m_batch)

                # with momentum (optional)
                dW1 = (beta * dW1 + (1. - beta) * dW1)
                db1 = (beta * db1 + (1. - beta) * db1)
                dW2 = (beta * dW2 + (1. - beta) * dW2)
                db2 = (beta * db2 + (1. - beta) * db2)

                # gradient descent
                self.params["W1"] = self.params["W1"] - learning_tate * dW1
                self.params["b1"] = self.params["b1"] - learning_tate * db1
                self.params["W2"] = self.params["W2"] - learning_tate * dW2
                self.params["b2"] = self.params["b2"] - learning_tate * db2

            # forward pass on training set
            cache = self.feed_forward(X_train)
            train_loss = self.compute_loss(Y_train, cache["A2"])
            print("Epoch {}: training loss = {}".format(
                i + 1, train_loss))

        print('Total duration: ' + str(round((time.time() - start_time), 2)) + 's')

    def test(self, x_test, y_test):
        cache = self.feed_forward(x_test)
        output = cache["A2"]
        data_size = x_test.shape[1]
        correct_cnt = 0
        for i in range(data_size):
            test = y_test[:, i]
            predict = output[:, i]
            if np.argmax(test) == np.argmax(predict):
                correct_cnt += 1

        print("test result {} correct".format(correct_cnt/data_size))


def one_hot_encoding(y):
    """
    one-hot encoding
    :param y:
    :return:
    """
    digits = 10
    examples = y.shape[0]
    y = y.reshape(1, examples)
    Y_new = np.eye(digits)[y.astype('int32')]
    Y_new = Y_new.T.reshape(digits, examples)
    return Y_new


def load_data():
    f = gzip.open('mnist.pkl.gz', 'rb')
    training_data, validation_data, test_data = pickle.load(f, encoding="latin1")
    f.close()

    training_img = np.int32(training_data[0] * 256)
    training_label = np.int32(training_data[1])
    validation_img = np.int32(validation_data[0] * 256)
    validation_label = np.int32(validation_data[1])
    test_img = np.int32(test_data[0] * 256)
    test_label = np.int32(test_data[1])

    tr_img = np.concatenate((training_img, validation_img))
    tr_label = np.concatenate((training_label, validation_label))

    tr_label = np.reshape(tr_label, (60000, 1))
    test_label = np.reshape(test_label, (10000, 1))
    return tr_img, tr_label, test_img, test_label


def main():
    from_cvs = True
    if from_cvs:
        train_image_file_name = sys.argv[1]
        train_label_file_name = sys.argv[2]
        test_image_file_name = sys.argv[3]
        print(train_image_file_name)
        train_image = pd.read_csv(train_image_file_name, sep=',', header=None).to_numpy()
        print(train_image.shape)

        print(train_label_file_name)
        train_label = pd.read_csv(train_label_file_name, sep=',', header=None).to_numpy()
        print(train_label.shape)

        print(test_image_file_name)
        test_image = pd.read_csv(test_image_file_name, sep=',', header=None).to_numpy()
        print(test_image.shape)

    else:
        train_image, train_label, test_image, test_label = load_data()
        # x_train, x_test = train_image, test_image
        # y_train, y_test = train_label, test_label

    new_train_label = one_hot_encoding(train_label)
    train_size = int(train_image.shape[0] * 0.8)
    print("train size: {}".format(train_size))
    X_train, X_test = train_image[:train_size].T, train_image[train_size:].T
    Y_train, Y_test = new_train_label[:, :train_size], new_train_label[:, train_size:]
    print("train-test shape:")
    print(X_train.shape)
    print(Y_train.shape)
    print(X_test.shape)
    print(Y_test.shape)
    model = NN()
    model.train(X_train, Y_train)
    model.test(X_test, Y_test)


if __name__ == "__main__":
    main()
