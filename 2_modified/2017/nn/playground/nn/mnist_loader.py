"""Small synthetic stand-in for the MNIST loader (see make_nn_support.py).
Same interface as the original `mnist_loader` (load_data, load_data_wrapper, vectorized_result)."""
import os

import numpy as np

_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "mnist_mini.npz")


def load_data():
    d = np.load(_FILE)
    f = lambda x: x.astype(np.float32) / 255.0
    return (
        (f(d["tr_x"]), d["tr_y"]),
        (f(d["va_x"]), d["va_y"]),
        (f(d["te_x"]), d["te_y"]),
    )


def load_data_wrapper():
    tr_d, va_d, te_d = load_data()
    training_data = list(zip([np.reshape(x, (784, 1)) for x in tr_d[0]], [vectorized_result(y) for y in tr_d[1]]))
    validation_data = list(zip([np.reshape(x, (784, 1)) for x in va_d[0]], va_d[1]))
    test_data = list(zip([np.reshape(x, (784, 1)) for x in te_d[0]], te_d[1]))
    return (training_data, validation_data, test_data)


def vectorized_result(j):
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e
