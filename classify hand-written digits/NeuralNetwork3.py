import numpy as np
import pandas as pd
import time
import pickle
import gzip
import sys


class NN:
    def __init__(self):
        # weights and bias
        self.W1 = None
        self.b1 = None
        self.W2 = None
        self.b2 = None
        self.prev_loss = 100

    # activation functions sigmoid relu and softmax
    def sigmoid(self, x):
        """
        Sigmoid function
        """
        return 1 / (1 + np.exp(-x))

    def softmax(self, x):
        """
        Softmax function, xxx[:, None] means add new axis
        """
        return np.exp(x) / np.sum(np.exp(x), axis=1)[:, None]

    def cross_entropy(self, pred_y, real_y):
        """
        Compute cross entropy between pred_y and real_y
        """
        return -np.sum(real_y * np.log(pred_y), axis=1)

    def compute_loss(self, pred_y, real_y):
        """
        compute loss function
        """
        L_sum = np.sum(np.multiply(real_y, np.log(pred_y)))
        m = real_y.shape[0]
        L = -(1. / m) * L_sum

        return L

    def train(self, x_train, y_train, hidden_n=112, epochs=400, beta=0.9, batch_size=100, print_loss=True):
        print("training...")
        start_time = time.time()

        data_size = x_train.shape[0]
        input_feature_size = x_train.shape[1]
        # layer1
        # weights and bias
        self.W1 = np.random.randn(input_feature_size, hidden_n) * np.sqrt(1. / input_feature_size)
        self.b1 = np.zeros((1, hidden_n)) * np.sqrt(1. / input_feature_size)

        # layer2
        # weights and bias
        self.W2 = np.random.randn(hidden_n, 10) * np.sqrt(1. / hidden_n)
        self.b2 = np.zeros((1, 10)) * np.sqrt(1. / hidden_n)

        for i in range(epochs):
            if i < 50:
                learning_rate = 0.01
            if 50 < i < 100:
                learning_rate = 0.005
            if 100 < i < 150:
                learning_rate = 0.005
            if 150 < i < 200:
                learning_rate = 0.005
            if 200 < i < 300:
                learning_rate = 0.005
            if i > 300:
                learning_rate = 0.001
            # shuffle training set
            permutation = np.random.permutation(data_size)
            x_train_shuffled = x_train[permutation, :]
            y_train_shuffled = y_train[permutation, :]

            batches = int(data_size / batch_size)
            for j in range(batches):
                # get mini-batch
                begin = j * batch_size
                end = min(begin + batch_size, data_size - 1)
                x = x_train_shuffled[begin:end, :]
                y = y_train_shuffled[begin:end, :]
                m_batch = end - begin

                # feed forward
                # layer 1
                z1 = np.matmul(x, self.W1) + self.b1
                a1 = self.sigmoid(z1)

                # layer 2
                z2 = np.matmul(a1, self.W2) + self.b2
                a2 = self.softmax(z2)

                # back propagation
                dz2 = (a2 - y)  # dJ/dz2 = dJ/do  * do/dz2 (l2 = l1 * W2 + b2)
                dW2 = np.matmul(a1.T, dz2) / m_batch  # dJ/dW2 = dJ/dz2 * dz2/dW2
                db2 = np.matmul(np.ones(m_batch), dz2) / m_batch  # dJ/db2 = dJ/dz2 * dz2/db2

                da1 = np.matmul(dz2, self.W2.T)  # dJ/da1 = dJ/dz2 * dz2/da1 (l1 = sigmoid(a1))
                dz1 = da1 * (a1 * (1 - a1))  # dJ/da1 = dJ/da1 * da1/da1 (a1 = X * W1 + b1)
                dW1 = np.matmul(x.T, dz1) / m_batch  # dJ/dW1 = dJ/da1 * da1/dW1
                db1 = np.matmul(np.ones(m_batch), dz1) / m_batch  # dJ/db1 = dJ/da1 * da1/db1

                # with momentum
                # dW1 = (beta * dW1 + (1. - beta) * dW1)
                # db1 = (beta * db1 + (1. - beta) * db1)
                # dW2 = (beta * dW2 + (1. - beta) * dW2)
                # db2 = (beta * db2 + (1. - beta) * db2)

                ## gradient descent
                self.W2 = self.W2 - learning_rate * dW2  # w = w - r * dw
                self.b2 = self.b2 - learning_rate * db2
                self.W1 = self.W1 - learning_rate * dW1
                self.b1 = self.b1 - learning_rate * db1

            # loss function
            if print_loss:
                l1 = self.sigmoid(np.matmul(x_train, self.W1) + self.b1)
                l2 = np.matmul(l1, self.W2) + self.b2
                out = self.softmax(l2)
                loss = self.compute_loss(out, y_train)
                print("epoch {} done, loss {}".format(i, loss))
                if loss >= self.prev_loss:
                    print("loss increase with lr {}".format(learning_rate))
                self.prev_loss = loss

        print("training done")
        print('Total duration: ' + str(round((time.time() - start_time), 2)) + 's')

    def test(self, x_test, y_test):
        l1 = self.sigmoid(np.matmul(x_test, self.W1) + self.b1)
        l2 = np.matmul(l1, self.W2) + self.b2
        out = self.softmax(l2)

        data_size = x_test.shape[0]
        correct_cnt = 0
        for i in range(data_size):
            test = y_test[i, :]
            predict = out[i, :]
            if np.argmax(test) == np.argmax(predict):
                correct_cnt += 1
        print("test result {} correct".format(correct_cnt / data_size))

    def predict(self, x_test):
        l1 = self.sigmoid(np.matmul(x_test, self.W1) + self.b1)
        l2 = np.matmul(l1, self.W2) + self.b2
        out = self.softmax(l2)
        data_size = x_test.shape[0]
        result = np.zeros((data_size,), dtype=np.int)
        for i in range(data_size):
            predict = out[i, :]
            number = np.argmax(predict)
            result[i] = number
        return result


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

    tr_img = np.concatenate((training_img, validation_img, test_img))
    tr_label = np.concatenate((training_label, validation_label, test_label))

    tr_label = np.reshape(tr_label, (70000, 1))
    return tr_img, tr_label


def write_predict(y_predict, file_name="test_predictions.csv"):
    np.savetxt(file_name, y_predict, delimiter=",", fmt="%d")


def one_hot_encoding(label):
    # converting label in one hot encoder representation
    new_label = np.zeros((label.shape[0], 10))
    for col in range(label.shape[0]):
        val = label[col]
        for row in range(10):
            if val == row:
                new_label[col, val] = 1
    return new_label


def main():
    train_image_file_name = sys.argv[1]
    train_label_file_name = sys.argv[2]
    test_image_file_name = sys.argv[3]
    print(train_image_file_name)
    train_image = pd.read_csv(train_image_file_name, sep=',', header=None).values
    print(train_image.shape)

    print(train_label_file_name)
    train_label = pd.read_csv(train_label_file_name, sep=',', header=None).values
    print(train_label.shape)

    print(test_image_file_name)
    test_image = pd.read_csv(test_image_file_name, sep=',', header=None).values
    print(test_image.shape)

    # train_image, train_label = load_data()

    new_train_label = one_hot_encoding(train_label)
    train_size = train_image.shape[0]
    print("train size: {}".format(train_size))
    # x is image
    # x_train, x_test = train_image[:train_size], train_image[train_size:]
    # y is label
    # y_train, y_test = new_train_label[:train_size], new_train_label[train_size:]

    # shuffle training set
    shuffle_index = np.random.permutation(train_size)
    x_train, y_train = train_image[shuffle_index], new_train_label[shuffle_index]
    x_train, y_train = x_train[:10000], y_train[:10000]

    model = NN()
    model.train(x_train, y_train)

    test_label = pd.read_csv("data/test_label.csv", sep=',', header=None).values
    new_test_label = one_hot_encoding(test_label)
    model.test(test_image, new_test_label)

    y_predict = model.predict(test_image)
    write_predict(y_predict)


if __name__ == "__main__":
    main()
