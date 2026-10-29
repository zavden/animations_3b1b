# ==============================================================================
# Scene:      IntroduceCostFunction
# Source:     videos/_2017/nn/part2.py (lines 585-1121)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/nn/network.py, _2017/nn/part1.py
#
# Run from this folder:
#     manimgl IntroduceCostFunction.py IntroduceCostFunction -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Provide package `nn` (network.py with binary-mode pickle fix, mnist_loader.py reading a small synthetic MNIST stand-in) through data_files, since the original mnist.pkl.gz is not in the repo.
#   - Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
#   - Inlined network.py: data files (image_map, pretrained weights) live in the bundled nn/ folder next to the scene.
#   - Pickle data files must be opened in binary mode in Python 3.
#   - Python 2 integer division used as an index/count -> //.
#   - Python 3: zip()/map()/filter() return iterators, wrap in list() before slicing.
#   - GL ChangingDecimal keeps the decimal in `self.mobject` (no `decimal_number` attribute).
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2017/nn/nn_pkg/mnist_mini.npz (synthetic MNIST stand-in, built from the 100 real digits of image_map by make_nn_support.py)
# ==============================================================================

import sys
import os.path
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


# ----- From _2017/nn/network.py -----

# CHANGE: Inlined network.py: data files (image_map, pretrained weights) live in the bundled nn/ folder next to the scene.
NN_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), "nn")  # CL17-B nndir
IMAGE_MAP_DATA_FILE = os.path.join(NN_DIRECTORY, "image_map")


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


def ReLU(z):
    result = np.array(z)
    result[result < 0] = 0
    return result


def ReLU_prime(z):
    return (np.array(z) > 0).astype('int')


def layer_to_image_array(layer):
    w = int(np.ceil(np.sqrt(len(layer))))
    if len(layer) < w**2:
        layer = np.append(layer, np.zeros(w**2 - len(layer)))
    layer = layer.reshape((w, w))
    # return Image.fromarray((255*layer).astype('uint8'))
    return (255*layer).astype('int')


def get_organized_images():
    # CHANGE: Pickle data files must be opened in binary mode in Python 3.
    data_file = open(IMAGE_MAP_DATA_FILE, mode = 'rb')
    image_map = pickle.load(data_file, encoding='latin1')
    data_file.close()
    return image_map



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


class NetworkMobject(VGroup):
    CONFIG = {
        "neuron_radius" : 0.15,
        "neuron_to_neuron_buff" : MED_SMALL_BUFF,
        "layer_to_layer_buff" : LARGE_BUFF,
        "neuron_stroke_color" : BLUE,
        "neuron_stroke_width" : 3,
        "neuron_fill_color" : GREEN,
        "edge_color" : GREY_B,
        "edge_stroke_width" : 2,
        "edge_propogation_color" : YELLOW,
        "edge_propogation_time" : 1,
        "max_shown_neurons" : 16,
        "brace_for_large_layers" : True,
        "average_shown_activation_of_large_layer" : True,
        "include_output_labels" : False,
    }
    def __init__(self, neural_network, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.neural_network = neural_network
        self.layer_sizes = neural_network.sizes
        self.add_neurons()
        self.add_edges()

    def add_neurons(self):
        layers = VGroup(*[
            self.get_layer(size)
            for size in self.layer_sizes
        ])
        layers.arrange(RIGHT, buff = self.layer_to_layer_buff)
        self.layers = layers
        self.add(self.layers)
        if self.include_output_labels:
            self.add_output_labels()

    def get_layer(self, size):
        layer = VGroup()
        n_neurons = size
        if n_neurons > self.max_shown_neurons:
            n_neurons = self.max_shown_neurons
        neurons = VGroup(*[
            Circle(
                radius = self.neuron_radius,
                stroke_color = self.neuron_stroke_color,
                stroke_width = self.neuron_stroke_width,
                fill_color = self.neuron_fill_color,
                fill_opacity = 0,
            )
            for x in range(n_neurons)
        ])   
        neurons.arrange(
            DOWN, buff = self.neuron_to_neuron_buff
        )
        for neuron in neurons:
            neuron.edges_in = VGroup()
            neuron.edges_out = VGroup()
        layer.neurons = neurons
        layer.add(neurons)

        if size > n_neurons:
            dots = OldTex("\\vdots")
            dots.move_to(neurons)
            VGroup(*neurons[:len(neurons) // 2]).next_to(
                dots, UP, MED_SMALL_BUFF
            )
            VGroup(*neurons[len(neurons) // 2:]).next_to(
                dots, DOWN, MED_SMALL_BUFF
            )
            layer.dots = dots
            layer.add(dots)
            if self.brace_for_large_layers:
                brace = Brace(layer, LEFT)
                brace_label = brace.get_tex(str(size))
                layer.brace = brace
                layer.brace_label = brace_label
                layer.add(brace, brace_label)

        return layer

    def add_edges(self):
        self.edge_groups = VGroup()
        for l1, l2 in zip(self.layers[:-1], self.layers[1:]):
            edge_group = VGroup()
            for n1, n2 in it.product(l1.neurons, l2.neurons):
                edge = self.get_edge(n1, n2)
                edge_group.add(edge)
                n1.edges_out.add(edge)
                n2.edges_in.add(edge)
            self.edge_groups.add(edge_group)
        self.add_to_back(self.edge_groups)

    def get_edge(self, neuron1, neuron2):
        return Line(
            neuron1.get_center(),
            neuron2.get_center(),
            buff = self.neuron_radius,
            stroke_color = self.edge_color,
            stroke_width = self.edge_stroke_width,
        )

    def get_active_layer(self, layer_index, activation_vector):
        layer = self.layers[layer_index].deepcopy()
        self.activate_layer(layer, activation_vector)
        return layer

    def activate_layer(self, layer, activation_vector):
        n_neurons = len(layer.neurons)
        av = activation_vector
        def arr_to_num(arr):
            return (np.sum(arr > 0.1) / float(len(arr)))**(1./3)

        if len(av) > n_neurons:
            if self.average_shown_activation_of_large_layer:
                indices = np.arange(n_neurons)
                indices *= int(len(av)/n_neurons)
                indices = list(indices)
                indices.append(len(av))
                av = np.array([
                    arr_to_num(av[i1:i2])
                    for i1, i2 in zip(indices[:-1], indices[1:])
                ])
            else:
                av = np.append(
                    av[:n_neurons//2],  # CHANGE: Python 2 integer division used as an index/count -> //.
                    av[-n_neurons//2:],  # CHANGE: Python 2 integer division used as an index/count -> //.
                )
        for activation, neuron in zip(av, layer.neurons):
            neuron.set_fill(
                color = self.neuron_fill_color,
                opacity = activation
            )
        return layer

    def activate_layers(self, input_vector):
        activations = self.neural_network.get_activation_of_all_layers(input_vector)
        for activation, layer in zip(activations, self.layers):
            self.activate_layer(layer, activation)

    def deactivate_layers(self):
        all_neurons = VGroup(*it.chain(*[
            layer.neurons
            for layer in self.layers
        ]))
        all_neurons.set_fill(opacity = 0)
        return self

    def get_edge_propogation_animations(self, index):
        edge_group_copy = self.edge_groups[index].copy()
        edge_group_copy.set_stroke(
            self.edge_propogation_color,
            width = 1.5*self.edge_stroke_width
        )
        return [ShowCreationThenDestruction(
            edge_group_copy, 
            run_time = self.edge_propogation_time,
            lag_ratio = 0.5
        )]

    def add_output_labels(self):
        self.output_labels = VGroup()
        for n, neuron in enumerate(self.layers[-1].neurons):
            label = OldTex(str(n))
            label.set_height(0.75*neuron.get_height())
            label.move_to(neuron)
            label.shift(neuron.get_width()*RIGHT)
            self.output_labels.add(label)
        self.add(self.output_labels)


class NetworkScene(Scene):
    CONFIG = {
        "layer_sizes" : [8, 6, 6, 4],
        "network_mob_config" : {},
    }
    def setup(self):
        self.add_network()

    def add_network(self):
        self.network = Network(sizes = self.layer_sizes)
        self.network_mob = NetworkMobject(
            self.network,
            **self.network_mob_config
        )
        self.add(self.network_mob)

    def feed_forward(self, input_vector, false_confidence = False, added_anims = None):
        if added_anims is None:
            added_anims = []
        activations = self.network.get_activation_of_all_layers(
            input_vector
        )
        if false_confidence:
            i = np.argmax(activations[-1])
            activations[-1] *= 0
            activations[-1][i] = 1.0
        for i, activation in enumerate(activations):
            self.show_activation_of_layer(i, activation, added_anims)
            added_anims = []

    def show_activation_of_layer(self, layer_index, activation_vector, added_anims = None):
        if added_anims is None:
            added_anims = []
        layer = self.network_mob.layers[layer_index]
        active_layer = self.network_mob.get_active_layer(
            layer_index, activation_vector
        )
        anims = [Transform(layer, active_layer)]
        if layer_index > 0:
            anims += self.network_mob.get_edge_propogation_animations(
                layer_index-1
            )
        anims += added_anims
        self.play(*anims)

    def remove_random_edges(self, prop = 0.9):
        for edge_group in self.network_mob.edge_groups:
            for edge in list(edge_group):
                if np.random.random() < prop:
                    edge_group.remove(edge)



# ----- From _2017/nn/part2.py -----

def get_training_image_group(train_in, train_out):
    image = MNistMobject(train_in)
    image.set_height(1)
    arrow = Vector(RIGHT, color = BLUE, buff = 0)
    output = np.argmax(train_out)
    output_tex = OldTex(str(output)).scale(1.5)
    result = Group(image, arrow, output_tex)
    result.arrange(RIGHT)
    result.to_edge(UP)
    return result


class PreviewLearning(NetworkScene):
    CONFIG = {
        "layer_sizes" : DEFAULT_LAYER_SIZES,
        "network_mob_config" : {
            "neuron_to_neuron_buff" : SMALL_BUFF,
            "layer_to_layer_buff" : 2,
            "edge_stroke_width" : 1,
            "neuron_stroke_color" : WHITE,
            "neuron_stroke_width" : 2,
            "neuron_fill_color" : WHITE,
            "average_shown_activation_of_large_layer" : False,
            "edge_propogation_color" : GREEN,
            "edge_propogation_time" : 2,
            "include_output_labels" : True,
        },
        "n_examples" : 15,
        "max_stroke_width" : 3,
        "stroke_width_exp" : 3,
        "eta" : 3.0,
        "positive_edge_color" : BLUE,
        "negative_edge_color" : RED,
        "positive_change_color" : BLUE_C,
        "negative_change_color" : average_color(*2*[RED] + [YELLOW]),
        "default_activate_run_time" : 1.5,
    }
    def construct(self):
        self.initialize_network()
        self.add_training_words()
        self.show_training()

    def initialize_network(self):
        self.network_mob.scale(0.7)
        self.network_mob.to_edge(DOWN)
        self.color_network_edges()

    def add_training_words(self):
        words = OldTexText("Training in \\\\ progress$\\dots$")
        words.scale(1.5)
        words.to_corner(UP+LEFT)

        self.add(words)

    def show_training(self):
        training_data, validation_data, test_data = load_data_wrapper()
        for train_in, train_out in training_data[:self.n_examples]:
            image = get_training_image_group(train_in, train_out)
            self.activate_network(train_in, FadeIn(image))
            self.backprop_one_example(
                train_in, train_out, 
                FadeOut(image), self.network_mob.layers.restore
            )

    def activate_network(self, train_in, *added_anims, **kwargs):
        network_mob = self.network_mob
        layers = network_mob.layers
        layers.save_state()
        activations = self.network.get_activation_of_all_layers(train_in)
        active_layers = [
            self.network_mob.get_active_layer(i, vect)
            for i, vect in enumerate(activations)
        ]
        all_edges = VGroup(*it.chain(*network_mob.edge_groups))
        run_time = kwargs.get("run_time", self.default_activate_run_time)
        edge_animation = LaggedStartMap(
            ShowCreationThenDestruction, 
            all_edges.copy().set_fill(YELLOW),
            run_time = run_time,
            lag_ratio = 0.3,
            remover = True,
        )
        layer_animation = Transform(
            VGroup(*layers), VGroup(*active_layers),
            run_time = run_time,
            lag_ratio = 0.5,
            rate_func=linear,
        )

        self.play(edge_animation, layer_animation, *added_anims)

    def backprop_one_example(self, train_in, train_out, *added_outro_anims):
        network_mob = self.network_mob
        nabla_b, nabla_w = self.network.backprop(train_in, train_out)
        neuron_groups = VGroup(*[
            layer.neurons
            for layer in network_mob.layers[1:]
        ])
        delta_neuron_groups = neuron_groups.copy()
        edge_groups = network_mob.edge_groups
        delta_edge_groups = VGroup(*[
            edge_group.copy()
            for edge_group in edge_groups
        ])
        tups = list(zip(
            it.count(), nabla_b, nabla_w, 
            delta_neuron_groups, neuron_groups,
            delta_edge_groups, edge_groups
        ))
        pc_color = self.positive_change_color
        nc_color = self.negative_change_color
        for i, nb, nw, delta_neurons, neurons, delta_edges, edges in reversed(tups):
            shown_nw = self.get_adjusted_first_matrix(nw)
            if np.max(shown_nw) == 0:
                shown_nw = (2*np.random.random(shown_nw.shape)-1)**5
            max_b = np.max(np.abs(nb))
            max_w = np.max(np.abs(shown_nw))
            for neuron, b in zip(delta_neurons, nb):
                color = nc_color if b > 0 else pc_color
                # neuron.set_fill(color, abs(b)/max_b)
                neuron.set_stroke(color, 3)
            for edge, w in zip(delta_edges.split(), shown_nw.T.flatten()):
                edge.set_stroke(
                    nc_color if w > 0 else pc_color,
                    3*abs(w)/max_w
                )
                edge.rotate(np.pi)
            if i == 2:
                delta_edges.submobjects = [
                    delta_edges[j]
                    for j in np.argsort(shown_nw.T.flatten())
                ]
            network = self.network
            network.weights[i] -= self.eta*nw
            network.biases[i] -= self.eta*nb

            self.play(
                ShowCreation(
                    delta_edges, lag_ratio = 0
                ),
                FadeIn(delta_neurons),
                run_time = 0.5
            )
        edge_groups.save_state()
        self.color_network_edges()
        self.remove(edge_groups)
        self.play(*it.chain(
            [ReplacementTransform(
                edge_groups.saved_state, edge_groups,
            )],
            list(map(FadeOut, [delta_edge_groups, delta_neuron_groups])),
            added_outro_anims,
        ))

    #####

    def get_adjusted_first_matrix(self, matrix):
        n = self.network_mob.max_shown_neurons
        if matrix.shape[1] > n:
            half = matrix.shape[1]//2  # CHANGE: Python 2 integer division used as an index/count -> //.
            return matrix[:,half-n//2:half+n//2]  # CHANGE: Python 2 integer division used as an index/count -> //.
        else:
            return matrix

    def color_network_edges(self):
        layers = self.network_mob.layers
        weight_matrices = self.network.weights
        for layer, matrix in zip(layers[1:], weight_matrices):
            matrix = self.get_adjusted_first_matrix(matrix)
            matrix_max = np.max(matrix)
            for neuron, row in zip(layer.neurons, matrix):
                for edge, w in zip(neuron.edges_in, row):
                    if w > 0:
                        color = self.positive_edge_color
                    else:
                        color = self.negative_edge_color
                    msw = self.max_stroke_width
                    swe = self.stroke_width_exp
                    sw = msw*(abs(w)/matrix_max)**swe
                    sw = min(sw, msw)
                    edge.set_stroke(color, sw)

    def get_edge_animation(self):
        edges = VGroup(*it.chain(*self.network_mob.edge_groups))
        return LaggedStartMap(
            ApplyFunction, edges,
            lambda mob : (
                lambda m : m.rotate(np.pi/12).set_color(YELLOW),
                mob
            ),
            rate_func = wiggle
        )


class ChangingDecimalWithColor(ChangingDecimal):
    def interpolate_mobject(self, alpha):
        ChangingDecimal.interpolate_mobject(self, alpha)
        num = self.number_update_func(alpha)
        # CHANGE: GL ChangingDecimal keeps the decimal in `self.mobject` (no `decimal_number` attribute).
        self.mobject.set_fill(
            interpolate_color(BLACK, WHITE, 0.5+num*0.5), 
            opacity = 1
        )


class IntroduceCostFunction(PreviewLearning):
    CONFIG = {
        "max_stroke_width" : 2,
        "full_edges_exp" : 5,
        "n_training_examples" : 100,
        "bias_color" : MAROON_B
    }
    def construct(self):
        self.network_mob.shift(LEFT)
        self.isolate_one_neuron()
        self.reminder_of_weights_and_bias()
        self.bring_back_rest_of_network()
        self.feed_in_example()
        self.make_fun_of_output()
        self.need_a_cost_function()
        self.fade_all_but_last_layer()
        self.break_down_cost_function()
        self.show_small_cost_output()
        self.average_over_all_training_data()

    def isolate_one_neuron(self):
        network_mob = self.network_mob
        neurons = VGroup(*it.chain(*[
            layer.neurons
            for layer in network_mob.layers[1:]
        ]))
        edges = VGroup(*it.chain(*network_mob.edge_groups))
        neuron = network_mob.layers[1].neurons[7]
        neurons.remove(neuron)
        edges.remove(*neuron.edges_in)
        output_labels = network_mob.output_labels
        kwargs = {
            "lag_ratio" : 0.5,
            "run_time" : 2,
        }
        self.play(
            FadeOut(edges, **kwargs),
            FadeOut(neurons, **kwargs),
            FadeOut(output_labels, **kwargs),
            Animation(neuron),
            neuron.edges_in.set_stroke, None, 2,
        )

        self.neuron = neuron

    def reminder_of_weights_and_bias(self):
        neuron = self.neuron
        layer0 = self.network_mob.layers[0]
        active_layer0 = self.network_mob.get_active_layer(
            0, np.random.random(len(layer0.neurons))
        )
        prev_neurons = layer0.neurons

        weighted_edges = VGroup(*[
            self.color_edge_randomly(edge.copy(), exp = 1)
            for edge in neuron.edges_in
        ])

        formula = OldTex(
            "=", "\\sigma(",
            "w_1", "a_1", "+",
            "w_2", "a_2", "+",
            "\\cdots", "+",
            "w_n", "a_n", "+", "b", ")"
        )
        w_labels = formula.get_parts_by_tex("w_")
        a_labels = formula.get_parts_by_tex("a_")
        b = formula.get_part_by_tex("b")
        sigma = VGroup(
            formula.get_part_by_tex("\\sigma"),
            formula.get_part_by_tex(")"),
        )
        symbols = VGroup(*[
            formula.get_parts_by_tex(tex)
            for tex in ("=", "+", "dots")
        ])

        w_labels.set_color(self.positive_edge_color)
        b.set_color(self.bias_color)
        sigma.set_color(YELLOW)
        formula.next_to(neuron, RIGHT)

        weights_word = OldTexText("Weights")
        weights_word.next_to(neuron.edges_in, RIGHT, aligned_edge = UP)
        weights_word.set_color(self.positive_edge_color)
        weights_arrow_to_edges = Arrow(
            weights_word.get_bottom(),
            neuron.edges_in[0].get_center(),
            color = self.positive_edge_color
        )

        weights_arrow_to_syms = VGroup(*[
            Arrow(
                weights_word.get_bottom(),
                w_label.get_top(),
                color = self.positive_edge_color
            )
            for w_label in w_labels
        ])

        bias_word = OldTexText("Bias")
        bias_arrow = Vector(DOWN, color = self.bias_color)
        bias_arrow.next_to(b, UP, SMALL_BUFF)
        bias_word.next_to(bias_arrow, UP, SMALL_BUFF)
        bias_word.set_color(self.bias_color)

        self.play(
            Transform(layer0, active_layer0),
            neuron.set_fill, None, 0.5,
            FadeIn(formula),
            run_time = 2,
            lag_ratio = 0.5
        )
        self.play(LaggedStartMap(
            ShowCreationThenDestruction, 
            neuron.edges_in.copy().set_stroke(YELLOW, 3),
            run_time = 1.5,
            lag_ratio = 0.7,
            remover = True
        ))
        self.play(
            Write(weights_word),
            *list(map(GrowArrow, weights_arrow_to_syms)),
            run_time = 1
        )
        self.wait()
        self.play(
            ReplacementTransform(
                w_labels.copy(), weighted_edges,
                remover = True
            ),
            Transform(neuron.edges_in, weighted_edges),
            ReplacementTransform(
                weights_arrow_to_syms,
                VGroup(weights_arrow_to_edges),
            )
        )
        self.wait()
        self.play(
            Write(bias_word),
            GrowArrow(bias_arrow),
            run_time = 1
        )
        self.wait(2)

        ## Initialize randomly
        w_random = OldTexText("Initialize randomly")
        w_random.move_to(weights_word, LEFT)
        b_random = w_random.copy()
        b_random.move_to(bias_word, RIGHT)

        self.play(
            Transform(weights_word, w_random),
            Transform(bias_word, b_random),
            *[
                ApplyFunction(self.color_edge_randomly, edge)
                for edge in neuron.edges_in
            ]
        )
        self.play(LaggedStartMap(
            ApplyMethod, neuron.edges_in,
            lambda m : (m.rotate, np.pi/12),
            rate_func = wiggle,
            run_time = 2
        ))
        self.play(*list(map(FadeOut, [
            weights_word, weights_arrow_to_edges,
            bias_word, bias_arrow,
            formula
        ])))

    def bring_back_rest_of_network(self):
        network_mob = self.network_mob
        neurons = VGroup(*network_mob.layers[1].neurons)
        neurons.remove(self.neuron)
        for layer in network_mob.layers[2:]:
            neurons.add(*layer.neurons)
        neurons.add(*network_mob.output_labels)

        edges = VGroup(*network_mob.edge_groups[0])
        edges.remove(*self.neuron.edges_in)
        for edge_group in network_mob.edge_groups[1:]:
            edges.add(*edge_group)

        for edge in edges:
            self.color_edge_randomly(edge, exp = self.full_edges_exp)

        self.play(*[
            LaggedStartMap(
                FadeIn, group,
                run_time = 3,
            )
            for group in (neurons, edges)
        ])

    def feed_in_example(self):
        vect = get_organized_images()[3][5]
        image = PixelsFromVect(vect)
        image.to_corner(UP+LEFT)
        rect = SurroundingRectangle(image, color = BLUE)
        neurons = VGroup(*[
            Circle(
                stroke_width = 1,
                stroke_color = WHITE,
                fill_opacity = pixel.fill_rgb[0],
                fill_color = WHITE,
                radius = pixel.get_height()/2
            ).move_to(pixel)
            for pixel in image
        ])
        layer0= self.network_mob.layers[0]
        n = self.network_mob.max_shown_neurons
        neurons.target = VGroup(*it.chain(
            VGroup(*layer0.neurons[:n//2]).set_fill(opacity = 0),  # CHANGE: Python 2 integer division used as an index/count -> //.
            [
                VectorizedPoint(layer0.dots.get_center())
                for x in range(len(neurons)-n)
            ],
            VGroup(*layer0.neurons[-n//2:]).set_fill(opacity = 0),  # CHANGE: Python 2 integer division used as an index/count -> //.
        ))

        self.play(
            self.network_mob.shift, 0.5*RIGHT,
            ShowCreation(rect),
            LaggedStartMap(DrawBorderThenFill, image),
            LaggedStartMap(DrawBorderThenFill, neurons),
            run_time = 1
        )
        self.play(
            MoveToTarget(
                neurons, lag_ratio = 0.5,
                remover = True
            ),
            layer0.neurons.set_fill, None, 0,
        )
        self.activate_network(vect, run_time = 2)

        self.image = image
        self.image_rect = rect

    def make_fun_of_output(self):
        last_layer = self.network_mob.layers[-1].neurons
        last_layer.add(self.network_mob.output_labels)
        rect = SurroundingRectangle(last_layer)
        words = OldTexText("Utter trash")
        words.next_to(rect, DOWN, aligned_edge = LEFT)
        VGroup(rect, words).set_color(YELLOW)

        self.play(
            ShowCreation(rect),
            Write(words, run_time = 2)
        )
        self.wait()

        self.trash_rect = rect
        self.trash_words = words

    def need_a_cost_function(self):
        vect = np.zeros(10)
        vect[3] = 1
        output_labels = self.network_mob.output_labels
        desired_layer = self.network_mob.get_active_layer(-1, vect)
        layer = self.network_mob.layers[-1]
        layer.add(output_labels)
        desired_layer.add(output_labels.copy())
        desired_layer.shift(2*RIGHT)
        layers = VGroup(layer, desired_layer)

        words = OldTexText(
            "What's the", "``cost''\\\\", "of this difference?",
        )
        words.set_color_by_tex("cost", RED)
        words.next_to(layers, UP)
        words.to_edge(UP)
        words.shift_onto_screen()
        double_arrow = DoubleArrow(
            layer.get_right(),
            desired_layer.get_left(),
            color = RED
        )

        self.play(FadeIn(words))
        self.play(ReplacementTransform(layer.copy(), desired_layer))
        self.play(GrowFromCenter(double_arrow))
        self.wait(2)

        self.desired_last_layer = desired_layer
        self.diff_arrow = double_arrow

    def fade_all_but_last_layer(self):
        network_mob = self.network_mob
        to_fade = VGroup(*it.chain(*list(zip(
            network_mob.layers[:-1],
            network_mob.edge_groups
        ))))

        self.play(LaggedStartMap(FadeOut, to_fade, run_time = 1))

    def break_down_cost_function(self):
        layer = self.network_mob.layers[-1]
        desired_layer = self.desired_last_layer
        decimal_groups = VGroup(*[
            self.num_vect_to_decimals(self.layer_to_num_vect(l))
            for l in (layer, desired_layer)
        ])

        terms = VGroup()
        symbols = VGroup()
        for d1, d2 in zip(*decimal_groups):
            term = OldTex(
                "(", "0.00", "-", "0.00", ")^2", "+",
            )
            term.scale(d1.get_height()/term[1].get_height())
            for d, i in (d1, 1), (d2, 3):
                term.submobjects[i] = d.move_to(term[i])
            terms.add(term)
            symbols.add(*term)
            symbols.remove(d1, d2)
            last_plus = term[-1]
        for mob in terms[-1], symbols:
            mob.remove(last_plus)
        terms.arrange(
            DOWN, buff = SMALL_BUFF,
            aligned_edge = LEFT
        )
        terms.set_height(1.5*layer.get_height())
        terms.next_to(layer, LEFT, buff = 2)

        image_group = Group(self.image, self.image_rect)
        image_group.generate_target()
        image_group.target.scale(0.5)
        cost_of = OldTexText("Cost of").set_color(RED)
        cost_group = VGroup(cost_of, image_group.target)
        cost_group.arrange(RIGHT)
        brace = Brace(terms, LEFT)
        cost_group.next_to(brace, LEFT)

        self.revert_to_original_skipping_status()
        self.play(*[
            ReplacementTransform(
                VGroup(*l.neurons[:10]).copy(), dg
            )
            for l, dg in zip([layer, desired_layer], decimal_groups)
        ])
        self.play(
            FadeIn(symbols),
            MoveToTarget(image_group),
            FadeIn(cost_of),
            GrowFromCenter(brace),
        )
        self.wait()

        self.decimal_groups = decimal_groups
        self.image_group = image_group
        self.cost_group = VGroup(cost_of, image_group)
        self.brace = brace

    def show_small_cost_output(self):
        decimals, desired_decimals = self.decimal_groups
        neurons = self.network_mob.layers[-1].neurons
        brace = self.brace
        cost_group = self.cost_group

        neurons.save_state()
        cost_group.save_state()
        brace.save_state()
        brace.generate_target()

        arrows = VGroup(*[
            Arrow(ORIGIN, LEFT).next_to(d, LEFT, MED_LARGE_BUFF)
            for d in decimals
        ])
        arrows.set_color(WHITE)

        def generate_term_update_func(decimal, desired_decimal):
            return lambda a : (decimal.number - desired_decimal.number)**2

        terms = VGroup()
        term_updates = []
        for arrow, d1, d2 in zip(arrows, *self.decimal_groups):
            term = DecimalNumber(0, num_decimal_places = 4)
            term.set_height(d1.get_height())
            term.next_to(arrow, LEFT)
            term.num_update_func = generate_term_update_func(d1, d2)
            terms.add(term)
            term_updates.append(ChangingDecimalWithColor(
                term, term.num_update_func,
                num_decimal_places = 4
            ))
        brace.target.next_to(terms, LEFT)

        sum_term = DecimalNumber(0)
        sum_term.next_to(brace.target, LEFT)
        sum_term.set_color(RED)
        def sum_update(alpha):
            return sum([
                (d1.number - d2.number)**2
                for d1, d2 in zip(*self.decimal_groups)
            ])
        term_updates.append(ChangingDecimal(sum_term, sum_update))
        for update in term_updates:
            update.interpolate_mobject(0)

        target_vect = 0.1*np.random.random(10)
        target_vect[3] = 0.97

        def generate_decimal_update_func(start, target):
            return lambda a : interpolate(start, target, a)

        update_decimals = [
            ChangingDecimalWithColor(
                decimal, 
                generate_decimal_update_func(decimal.number, t)
            )
            for decimal, t in zip(decimals, target_vect)
        ]

        self.play(
            cost_group.scale, 0.5,
            cost_group.to_corner, UP+LEFT,
            MoveToTarget(brace),
            LaggedStartMap(GrowArrow, arrows),
            LaggedStartMap(FadeIn, terms),
            FadeIn(sum_term),
            Animation(decimals)
        )
        self.play(*it.chain(
            update_decimals,
            term_updates,
            [
                ApplyMethod(neuron.set_fill, None, t)
                for neuron, t in zip(neurons, target_vect)
            ]
        ))
        self.wait()
        self.play(LaggedStartMap(Indicate, decimals, rate_func = there_and_back))
        self.wait()
        for update in update_decimals:
            update.rate_func = lambda a : smooth(1-a)
        self.play(*it.chain(
            update_decimals,
            term_updates,
            [neurons.restore]
        ), run_time = 2)
        self.wait()
        self.play(
            cost_group.restore,
            brace.restore,
            FadeOut(VGroup(terms, sum_term, arrows)),
        )

    def average_over_all_training_data(self):
        image_group = self.image_group
        decimal_groups = self.decimal_groups

        random_neurons = self.network_mob.layers[-1].neurons
        desired_neurons = self.desired_last_layer.neurons

        wait_times = iter(it.chain(
            4*[0.5],
            4*[0.25],
            8*[0.125],
            it.repeat(0.1)
        ))

        words = OldTexText("Average cost of \\\\ all training data...")
        words.set_color(BLUE)
        words.to_corner(UP+LEFT)

        self.play(
            Write(words, run_time = 1),
        )

        training_data, validation_data, test_data = load_data_wrapper()
        for in_vect, out_vect in training_data[:self.n_training_examples]:
            random_v = np.random.random(10)
            new_decimal_groups = VGroup(*[
                self.num_vect_to_decimals(v)
                for v in (random_v, out_vect)
            ])
            for ds, nds in zip(decimal_groups, new_decimal_groups):
                for old_d, new_d in zip(ds, nds):
                    new_d.replace(old_d)
            self.remove(decimal_groups)
            self.add(new_decimal_groups)
            decimal_groups = new_decimal_groups
            for pair in (random_v, random_neurons), (out_vect, desired_neurons):
                for n, neuron in zip(*pair):
                    neuron.set_fill(opacity = n)
            new_image_group = MNistMobject(in_vect)
            new_image_group.replace(image_group)
            self.remove(image_group)
            self.add(new_image_group)
            image_group = new_image_group

            self.wait(next(wait_times))

    ####

    def color_edge_randomly(self, edge, exp = 1):
        r = (2*np.random.random()-1)**exp
        r *= self.max_stroke_width
        pc, nc = self.positive_edge_color, self.negative_edge_color
        edge.set_stroke(
            color = pc if r > 0 else nc,
            width = abs(r),
        )
        return edge

    def layer_to_num_vect(self, layer, n_terms = 10):
        return [
            n.get_fill_opacity()
            for n in layer.neurons
        ][:n_terms]

    def num_vect_to_decimals(self, num_vect):
        return VGroup(*[
            DecimalNumber(n).set_fill(opacity = 0.5*n + 0.5)
            for n in num_vect
        ])

    def num_vect_to_column_vector(self, num_vect, height):
        decimals = VGroup(*[
            DecimalNumber(n).set_fill(opacity = 0.5*n + 0.5)
            for n in num_vect
        ])
        decimals.arrange(DOWN)
        decimals.set_height(height)
        lb, rb = brackets = OldTex("[]")
        brackets.scale(2)
        brackets.stretch_to_fit_height(height + SMALL_BUFF)
        lb.next_to(decimals, LEFT)
        rb.next_to(decimals, RIGHT)
        result = VGroup(brackets, decimals)
        result.brackets = brackets
        result.decimals = decimals
        return result
