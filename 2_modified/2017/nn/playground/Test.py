# ==============================================================================
# Scene:      Test
# Source:     videos/_2017/nn/playground.py (lines 17-138)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/nn/network.py, _2017/nn/part1.py
#
# Run from this folder:
#     manimgl Test.py Test -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Provide package `nn` (network.py with binary-mode pickle fix, mnist_loader.py reading a small synthetic MNIST stand-in) through data_files, since the original mnist.pkl.gz is not in the repo.
#   - Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
#   - Inlined network.py: data files (image_map, pretrained weights) live in the bundled nn/ folder next to the scene.
#   - Remove `from constants import *` (Cairo module; manim_imports_ext already provides the constants).
#   - Python 3: zip()/map()/filter() return iterators, wrap in list() before slicing.
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2017/nn/nn_pkg/mnist_mini.npz (synthetic MNIST stand-in, built from the 100 real digits of image_map by make_nn_support.py)
# ==============================================================================

import sys
import os.path
from functools import reduce
# CHANGE: Remove `from constants import *` (Cairo module; manim_imports_ext already provides the constants).
from manim_imports_ext import *
#### Libraries
# Standard library
import os
import pickle
import random
# Third-party libraries
import numpy as np
# CHANGE: Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
import sys, os.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # CL17-B
from nn.mnist_loader import load_data_wrapper
import warnings
from nn.network import *


# ----- From _2017/nn/playground.py -----

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))



# ----- From _2017/nn/network.py -----

# CHANGE: Inlined network.py: data files (image_map, pretrained weights) live in the bundled nn/ folder next to the scene.
NN_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), "nn")  # CL17-B nndir
# PRETRAINED_DATA_FILE = os.path.join(NN_DIRECTORY, "pretrained_weights_and_biases_80")
# PRETRAINED_DATA_FILE = os.path.join(NN_DIRECTORY, "pretrained_weights_and_biases_ReLU")
PRETRAINED_DATA_FILE = os.path.join(NN_DIRECTORY, "pretrained_weights_and_biases")


# PRETRAINED_DATA_FILE = "/Users/grant/cs/manim/nn/pretrained_weights_and_biases_on_zero"
# DEFAULT_LAYER_SIZES = [28**2, 80, 10]
DEFAULT_LAYER_SIZES = [28**2, 16, 16, 10]


class Network(object):
    def __init__(self, sizes, non_linearity = "sigmoid"):
        """The list ``sizes`` contains the number of neurons in the
        respective layers of the network.  For example, if the list
        was [2, 3, 1] then it would be a three-layer network, with the
        first layer containing 2 neurons, the second layer 3 neurons,
        and the third layer 1 neuron.  The biases and weights for the
        network are initialized randomly, using a Gaussian
        distribution with mean 0, and variance 1.  Note that the first
        layer is assumed to be an input layer, and by convention we
        won't set any biases for those neurons, since biases are only
        ever used in computing the outputs from later layers."""
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]
        if non_linearity == "sigmoid":
            self.non_linearity = sigmoid
            self.d_non_linearity = sigmoid_prime
        elif non_linearity == "ReLU":
            self.non_linearity = ReLU
            self.d_non_linearity = ReLU_prime
        else:
            raise Exception("Invalid non_linearity")

    def feedforward(self, a):
        """Return the output of the network if ``a`` is input."""
        for b, w in zip(self.biases, self.weights):
            a = self.non_linearity(np.dot(w, a)+b)
        return a

    def get_activation_of_all_layers(self, input_a, n_layers = None):
        if n_layers is None:
            n_layers = self.num_layers
        activations = [input_a.reshape((input_a.size, 1))]
        for bias, weight in list(zip(self.biases, self.weights))[:n_layers]:  # CHANGE: Python 3: zip()/map()/filter() return iterators, wrap in list() before slicing.
            last_a = activations[-1]
            new_a = self.non_linearity(np.dot(weight, last_a) + bias)
            new_a = new_a.reshape((new_a.size, 1))
            activations.append(new_a)
        return activations

    def SGD(self, training_data, epochs, mini_batch_size, eta,
            test_data=None):
        """Train the neural network using mini-batch stochastic
        gradient descent.  The ``training_data`` is a list of tuples
        ``(x, y)`` representing the training inputs and the desired
        outputs.  The other non-optional parameters are
        self-explanatory.  If ``test_data`` is provided then the
        network will be evaluated against the test data after each
        epoch, and partial progress printed out.  This is useful for
        tracking progress, but slows things down substantially."""
        if test_data: n_test = len(test_data)
        n = len(training_data)
        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches = [
                training_data[k:k+mini_batch_size]
                for k in range(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            if test_data:
                print("Epoch {0}: {1} / {2}".format(
                    j, self.evaluate(test_data), n_test))
            else:
                print("Epoch {0} complete".format(j))

    def update_mini_batch(self, mini_batch, eta):
        """Update the network's weights and biases by applying
        gradient descent using backpropagation to a single mini batch.
        The ``mini_batch`` is a list of tuples ``(x, y)``, and ``eta``
        is the learning rate."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [w-(eta/len(mini_batch))*nw
                        for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b-(eta/len(mini_batch))*nb
                       for b, nb in zip(self.biases, nabla_b)]

    def backprop(self, x, y):
        """Return a tuple ``(nabla_b, nabla_w)`` representing the
        gradient for the cost function C_x.  ``nabla_b`` and
        ``nabla_w`` are layer-by-layer lists of numpy arrays, similar
        to ``self.biases`` and ``self.weights``."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # feedforward
        activation = x
        activations = [x] # list to store all the activations, layer by layer
        zs = [] # list to store all the z vectors, layer by layer
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation)+b
            zs.append(z)
            activation = self.non_linearity(z)
            activations.append(activation)
        # backward pass
        delta = self.cost_derivative(activations[-1], y) * \
            self.d_non_linearity(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        # Note that the variable l in the loop below is used a little
        # differently to the notation in Chapter 2 of the book.  Here,
        # l = 1 means the last layer of neurons, l = 2 is the
        # second-last layer, and so on.  It's a renumbering of the
        # scheme in the book, used here to take advantage of the fact
        # that Python can use negative indices in lists.
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = self.d_non_linearity(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
        return (nabla_b, nabla_w)

    def evaluate(self, test_data):
        """Return the number of test inputs for which the neural
        network outputs the correct result. Note that the neural
        network's output is assumed to be the index of whichever
        neuron in the final layer has the highest activation."""
        test_results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)

    def cost_derivative(self, output_activations, y):
        """Return the vector of partial derivatives \\partial C_x /
        \\partial a for the output activations."""
        return (output_activations-y)


#### Miscellaneous functions
def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+np.exp(-z))


def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
    return sigmoid(z)*(1-sigmoid(z))


def sigmoid_inverse(z):
    # z = 0.998*z + 0.001
    assert(np.max(z) <= 1.0 and np.min(z) >= 0.0)
    z = 0.998*z + 0.001
    return np.log(np.true_divide(
        1.0, (np.true_divide(1.0, z) - 1)
    ))


def ReLU(z):
    result = np.array(z)
    result[result < 0] = 0
    return result


def ReLU_prime(z):
    return (np.array(z) > 0).astype('int')


def get_pretrained_network():
    data_file = open(PRETRAINED_DATA_FILE, 'rb')
    weights, biases = pickle.load(data_file, encoding='latin1')
    sizes = [w.shape[1] for w in weights]
    sizes.append(weights[-1].shape[0])
    network = Network(sizes)
    network.weights = weights
    network.biases = biases
    return network


def layer_to_image_array(layer):
    w = int(np.ceil(np.sqrt(len(layer))))
    if len(layer) < w**2:
        layer = np.append(layer, np.zeros(w**2 - len(layer)))
    layer = layer.reshape((w, w))
    # return Image.fromarray((255*layer).astype('uint8'))
    return (255*layer).astype('int')


def maximizing_input(network, layer_index, layer_vect, n_steps = 100, seed_guess = None):
    pre_sig_layer_vect = sigmoid_inverse(layer_vect)
    weights, biases = network.weights, network.biases
    # guess = np.random.random(weights[0].shape[1])
    if seed_guess is not None:
        pre_sig_guess = sigmoid_inverse(seed_guess.flatten())
    else:
        pre_sig_guess = np.random.randn(weights[0].shape[1])
    norms = []
    for step in range(n_steps):
        activations = network.get_activation_of_all_layers(
            sigmoid(pre_sig_guess), layer_index
        )
        jacobian = np.diag(sigmoid_prime(pre_sig_guess).flatten())
        for W, a, b in zip(weights, activations, biases):
            jacobian = np.dot(W, jacobian)
            a = a.reshape((a.size, 1))
            sp = sigmoid_prime(np.dot(W, a) + b)
            jacobian = np.dot(np.diag(sp.flatten()), jacobian)
        gradient = np.dot(
            np.array(layer_vect).reshape((1, len(layer_vect))),
            jacobian
        ).flatten()
        norm = get_norm(gradient)
        if norm == 0:
            break
        norms.append(norm)
        old_pre_sig_guess = np.array(pre_sig_guess)
        pre_sig_guess += 0.1*gradient
        print(get_norm(old_pre_sig_guess - pre_sig_guess))
    print("")
    return sigmoid(pre_sig_guess)



# ----- From _2017/nn/part1.py -----

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class WrappedImage(Group):
    CONFIG = {
        "rect_kwargs" : {
            "color" : BLUE,
            "buff" : SMALL_BUFF,
        }
    }
    def __init__(self, image_mobject, **kwargs):
        Group.__init__(self, **kwargs)
        rect = SurroundingRectangle(
            image_mobject, **self.rect_kwargs
        )
        self.add(rect, image_mobject)


class PixelsAsSquares(VGroup):
    CONFIG = {
        "height" : 2,
    }
    def __init__(self, image_mobject, **kwargs):
        VGroup.__init__(self, **kwargs)
        for row in image_mobject.pixel_array:
            for rgba in row:
                square = Square(
                    stroke_width = 0, 
                    fill_opacity = rgba[3]/255.0,
                    fill_color = rgba_to_color(rgba/255.0),
                )
                self.add(square)
        self.arrange_in_grid(
            *image_mobject.pixel_array.shape[:2],
            buff = 0
        )
        self.replace(image_mobject)


class PixelsFromVect(PixelsAsSquares):
    def __init__(self, vect, **kwargs):
        PixelsAsSquares.__init__(self,
            ImageMobject(layer_to_image_array(vect)),
            **kwargs
        )


class MNistMobject(WrappedImage):
    def __init__(self, vect, **kwargs):
        WrappedImage.__init__(self, 
            ImageMobject(layer_to_image_array(vect)),
            **kwargs
        )



# ----- From _2017/nn/playground.py -----

class Test(Scene):
    def construct(self):
        network = get_pretrained_network()
        training_data, validation_data, test_data = load_data_wrapper()
        self.show_weight_rows(network, index = 0)
        # self.show_maximizing_inputs(network)
        # self.show_all_activation_images(network, test_data)

        # group = Group()
        # for k in range(10):
        #     v = np.zeros((10, 1))
        #     v[k] = 1
        #     h_group = Group()
        #     for W, b in reversed(zip(network.weights, network.biases)):
        #         h_group.add(MNistMobject(v))
        #         v = np.dot(W.T, sigmoid_inverse(v) - b)
        #         v = sigmoid(v)
        #     h_group.add(MNistMobject(v))
        #     h_group.arrange(LEFT)
        #     group.add(h_group)
        # group.arrange(DOWN)
        # group.set_height(FRAME_HEIGHT - 1)
        # self.add(group)


    def show_random_results(self):
        group = Group(*[
            Group(*[
                MNistMobject(a)
                for a in network.get_activation_of_all_layers(
                    np.random.randn(784, 1)
                )
            ]).arrange(RIGHT)
            for x in range(10)
        ]).arrange(DOWN)
        group.set_height(FRAME_HEIGHT - 1)
        self.add(group)

    def show_weight_rows(self, network, index):
        group = VGroup()
        for row in network.weights[index]:
            mob = PixelsFromVect(np.zeros(row.size))
            for n, pixel in zip(row, mob):
                color = GREEN if n > 0 else RED
                opacity = 2*(sigmoid(abs(n)) - 0.5)
                pixel.set_fill(color, opacity = opacity)
            group.add(mob)
        group.arrange_in_grid()
        group.set_height(FRAME_HEIGHT - 1)
        self.add(group)

    def show_all_activation_images(self, network, test_data):
        image_samples = Group(*[
            self.get_activation_images(digit, network, test_data)
            for digit in range(10)
        ])
        image_samples.arrange_in_grid(
            n_rows = 2, buff = LARGE_BUFF
        )
        image_samples.set_height(FRAME_HEIGHT - 1)
        self.add(image_samples)

    def get_activation_images(self, digit, network, test_data, n_examples = 8):
        input_vectors = [
            data[0] 
            for data in test_data
            if data[1] == digit
        ]
        activation_iamges = Group(*[
            Group(*[
                MNistMobject(a)
                for a in network.get_activation_of_all_layers(vect)
            ]).arrange(RIGHT)
            for vect in input_vectors[:n_examples]
        ]).arrange(DOWN)
        activation_iamges.set_height(FRAME_HEIGHT - 1)
        return activation_iamges

    def show_two_blend(self):
        training_data, validation_data, test_data = load_data_wrapper()
        vects = [
            data[0]
            for data in training_data[:30]
            if np.argmax(data[1]) == 2
        ]
        mean_vect = reduce(op.add, vects)/len(vects)
        self.add(MNistMobject(mean_vect))

    def show_maximizing_inputs(self, network):
        training_data, validation_data, test_data = load_data_wrapper()
        layer = 1
        n_neurons = DEFAULT_LAYER_SIZES[layer]
        groups = Group()
        for k in range(n_neurons):
            out = np.zeros(n_neurons)
            out[k] = 1
            in_vect = maximizing_input(network, layer, out)
            new_out = network.get_activation_of_all_layers(in_vect)[layer]
            group = Group(*list(map(MNistMobject, [in_vect, new_out])))
            group.arrange(DOWN+RIGHT, SMALL_BUFF)
            groups.add(group)
        groups.arrange_in_grid()
        groups.set_height(FRAME_HEIGHT - 1)
        self.add(groups)

    def show_test_input(self, network):
        training_data, validation_data, test_data = load_data_wrapper()
        group = Group(*[
            self.get_set(network, test)
            for test in test_data[3:20]
            if test[1] in [4, 9]
        ])
        group.arrange(DOWN, buff = MED_LARGE_BUFF)
        group.set_height(FRAME_HEIGHT - 1)
        self.play(FadeIn(group))

    def get_set(self, network, test):
        test_in, test_out = test
        activations = network.get_activation_of_all_layers(test_in)
        group = Group(*list(map(MNistMobject, activations)))
        group.arrange(RIGHT, buff = LARGE_BUFF)
        return group
