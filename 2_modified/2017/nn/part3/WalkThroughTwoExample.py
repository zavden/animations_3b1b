# ==============================================================================
# Scene:      WalkThroughTwoExample
# Source:     videos/_2017/nn/part3.py (lines 545-1388)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/nn/network.py, _2017/nn/part1.py, _2017/nn/part2.py
#
# Run from this folder:
#     manimgl WalkThroughTwoExample.py WalkThroughTwoExample -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Provide package `nn` (network.py with binary-mode pickle fix, mnist_loader.py reading a small synthetic MNIST stand-in) through data_files, since the original mnist.pkl.gz is not in the repo.
#   - Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
#   - Inlined network.py: data files (image_map, pretrained weights) live in the bundled nn/ folder next to the scene.
#   - Pickle data files must be opened in binary mode in Python 3.
#   - Python 2 integer division used as an index/count -> //.
#   - Python 3: zip()/map()/filter() return iterators, wrap in list() before slicing.
#   - `setup_bases()` never existed in Cairo manim either; call the base class setup explicitly (Cairo called each base's setup).
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2017/nn/nn_pkg/mnist_mini.npz (synthetic MNIST stand-in, built from the 100 real digits of image_map by make_nn_support.py)
# ==============================================================================

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
import sys
import os.path
from manim_imports_ext import *
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



# ----- From _2017/nn/part3.py -----

class ShowAveragingCost(PreviewLearning):
    CONFIG = {
        "network_scale_val" : 0.8,
        "stroke_width_exp" : 1,
        "start_examples_time" : 5,
        "examples_per_adjustment_time" : 2,
        "n_adjustments" : 5,
        "time_per_example" : 1./15,
        "image_height" : 1.2,
    }
    def construct(self):
        self.setup_network()
        self.setup_diff_words()
        self.show_many_examples()

    def setup_network(self):
        self.network_mob.scale(self.network_scale_val)
        self.network_mob.to_edge(DOWN)
        self.network_mob.shift(LEFT)
        self.color_network_edges()

    def setup_diff_words(self):
        last_layer_copy = self.network_mob.layers[-1].deepcopy()
        last_layer_copy.add(self.network_mob.output_labels.copy())
        last_layer_copy.shift(1.5*RIGHT)

        double_arrow = DoubleArrow(
            self.network_mob.output_labels,
            last_layer_copy,
            color = RED
        )
        brace = Brace(
            VGroup(self.network_mob.layers[-1], last_layer_copy), 
            UP
        )
        cost_words = brace.get_text("Cost of \\\\ one example")
        cost_words.set_color(RED)

        self.add(last_layer_copy, double_arrow, brace, cost_words)
        self.set_variables_as_attrs(
            last_layer_copy, double_arrow, brace, cost_words
        )
        self.last_layer_copy = last_layer_copy

    def show_many_examples(self):
        training_data, validation_data, test_data = load_data_wrapper()

        average_words = OldTexText("Average over all training examples")
        average_words.next_to(LEFT, RIGHT)
        average_words.to_edge(UP)
        self.add(average_words)

        n_start_examples = int(self.start_examples_time/self.time_per_example)
        n_examples_per_adjustment = int(self.examples_per_adjustment_time/self.time_per_example)
        for train_in, train_out in training_data[:n_start_examples]:
            self.show_one_example(train_in, train_out)
            self.wait(self.time_per_example)

        #Wiggle all edges
        edges = VGroup(*it.chain(*self.network_mob.edge_groups))
        reversed_edges = VGroup(*reversed(edges))
        self.play(LaggedStartMap(
            ApplyFunction, edges,
            lambda edge : (
                lambda m : m.rotate(np.pi/12).set_color(YELLOW),
                edge,
            ),
            rate_func = lambda t : wiggle(t, 4),
            run_time = 3,
        ))

        #Show all, then adjust
        words = OldTexText(
            "Each step \\\\ uses every \\\\ example\\\\",
            "$\\dots$theoretically",
            alignment = ""
        )
        words.set_color(YELLOW)
        words.scale(0.8)
        words.to_corner(UP+LEFT)

        for x in range(self.n_adjustments):
            if x < 2:
                self.play(FadeIn(words[x]))
            for train_in, train_out in training_data[:n_examples_per_adjustment]:
                self.show_one_example(train_in, train_out)
                self.wait(self.time_per_example)
            self.play(LaggedStartMap(
                ApplyMethod, reversed_edges,
                lambda m : (m.rotate, np.pi),
                run_time = 1,
                lag_ratio = 0.2,
            ))
            if x >= 2:
                self.wait()

    ####

    def show_one_example(self, train_in, train_out):
        if hasattr(self, "curr_image"):
            self.remove(self.curr_image)
        image = MNistMobject(train_in)
        image.set_height(self.image_height)
        image.next_to(
            self.network_mob.layers[0].neurons, UP,
            aligned_edge = LEFT
        )
        self.add(image)
        self.network_mob.activate_layers(train_in)

        index = np.argmax(train_out)
        self.last_layer_copy.neurons.set_fill(opacity = 0)
        self.last_layer_copy.neurons[index].set_fill(WHITE, opacity = 1)
        self.add(self.last_layer_copy)

        self.curr_image = image


class WalkThroughTwoExample(ShowAveragingCost):
    CONFIG = {
        "random_seed" : 0,
    }
    def setup(self):
        np.random.seed(self.random_seed)
        random.seed(self.random_seed)
        # CHANGE: `setup_bases()` never existed in Cairo manim either; call the base class setup explicitly (Cairo called each base's setup).
        ShowAveragingCost.setup(self)

    def construct(self):
        self.force_skipping()

        self.setup_network()
        self.setup_diff_words()
        self.show_single_example()
        self.single_example_influencing_weights()
        self.expand_last_layer()
        self.show_activation_formula()
        self.three_ways_to_increase()
        self.note_connections_to_brightest_neurons()
        self.fire_together_wire_together()
        self.show_desired_increase_to_previous_neurons()
        self.only_keeping_track_of_changes()
        self.show_other_output_neurons()
        self.show_recursion()

    def show_single_example(self):
        two_vect = get_organized_images()[2][0]
        two_out = np.zeros(10)
        two_out[2] = 1.0
        self.show_one_example(two_vect, two_out)
        for layer in self.network_mob.layers:
            layer.neurons.set_fill(opacity = 0)

        self.activate_network(two_vect)
        self.wait()

    def single_example_influencing_weights(self):
        two = self.curr_image
        two.save_state()

        edge_groups = self.network_mob.edge_groups
        def adjust_edge_group_anim(edge_group):
            return LaggedStartMap(
                ApplyFunction, edge_group,
                lambda edge : (
                    lambda m : m.rotate(np.pi/12).set_color(YELLOW),
                    edge
                ),
                rate_func = wiggle,
                run_time = 1,
            )

        self.play(
            two.next_to, edge_groups[0].get_corner(DOWN+RIGHT), DOWN,
            adjust_edge_group_anim(edge_groups[0])
        )
        self.play(
            ApplyMethod(
                two.next_to, edge_groups[1].get_corner(UP+RIGHT), UP,
                path_arc = np.pi/6,
            ),
            adjust_edge_group_anim(VGroup(*reversed(edge_groups[1])))
        )
        self.play(
            ApplyMethod(
                two.next_to, edge_groups[2].get_corner(DOWN+RIGHT), DOWN,
                path_arc = -np.pi/6,
            ),
            adjust_edge_group_anim(edge_groups[2])
        )
        self.play(two.restore)
        self.wait()

    def expand_last_layer(self):
        neurons = self.network_mob.layers[-1].neurons
        alt_neurons = self.last_layer_copy.neurons
        output_labels = self.network_mob.output_labels
        alt_output_labels = self.last_layer_copy[-1]
        edges = self.network_mob.edge_groups[-1]

        movers = VGroup(
            neurons, alt_neurons, 
            output_labels, alt_output_labels, 
            *edges
        )
        to_fade = VGroup(self.brace, self.cost_words, self.double_arrow)
        for mover in movers:
            mover.save_state()
            mover.generate_target()
            mover.target.scale(2)
        neurons[2].save_state()

        neurons.target.to_edge(DOWN, MED_LARGE_BUFF)
        output_labels.target.next_to(neurons.target, RIGHT, MED_SMALL_BUFF)
        alt_neurons.target.next_to(neurons.target, RIGHT, buff = 2)
        alt_output_labels.target.next_to(alt_neurons.target, RIGHT, MED_SMALL_BUFF)

        n_pairs = it.product(
            self.network_mob.layers[-2].neurons, 
            neurons.target
        )
        for edge, (n1, n2) in zip(edges, n_pairs):
            r1 = n1.get_width()/2.0
            r2 = n2.get_width()/2.0
            c1 = n1.get_center()
            c2 = n2.get_center()
            vect = c2 - c1
            norm = get_norm(vect)
            unit_vect = vect / norm

            edge.target.put_start_and_end_on(
                c1 + unit_vect*r1,
                c2 - unit_vect*r2
            )

        self.play(
            FadeOut(to_fade),
            *list(map(MoveToTarget, movers))
        )
        self.show_decimals(neurons)
        self.cannot_directly_affect_activations()
        self.show_desired_activation_nudges(neurons, output_labels, alt_output_labels)
        self.focus_on_one_neuron(movers)

    def show_decimals(self, neurons):
        decimals = VGroup()
        for neuron in neurons:
            activation = neuron.get_fill_opacity()
            decimal = DecimalNumber(activation, num_decimal_places = 1)
            decimal.set_width(0.7*neuron.get_width())
            decimal.move_to(neuron)
            if activation > 0.8:
                decimal.set_color(BLACK)
            decimals.add(decimal)

        self.play(Write(decimals, run_time = 2))
        self.wait()
        self.decimals = decimals

    def cannot_directly_affect_activations(self):
        words = OldTexText("You can only adjust weights and biases")
        words.next_to(self.curr_image, RIGHT, MED_SMALL_BUFF, UP)

        edges = VGroup(*self.network_mob.edge_groups.family_members_with_points())
        random.shuffle(edges.submobjects)
        for edge in edges:
            edge.generate_target()
            edge.target.set_stroke(
                random.choice([BLUE, RED]),
                2*random.random()**2,
            )

        self.play(
            LaggedStartMap(
                Transform, edges,
                lambda e : (e, e.target),
                run_time = 4, 
                rate_func = there_and_back,
            ),
            Write(words, run_time = 2)
        )
        self.play(FadeOut(words))

    def show_desired_activation_nudges(self, neurons, output_labels, alt_output_labels):
        arrows = VGroup()
        rects = VGroup()
        for i, neuron, label in zip(it.count(), neurons, alt_output_labels):
            activation = neuron.get_fill_opacity()
            target_val = 1 if i == 2 else 0
            diff = abs(activation - target_val)
            arrow = Arrow(
                ORIGIN, diff*neuron.get_height()*DOWN,
                color = RED,
            )
            arrow.move_to(neuron.get_right())
            arrow.shift(0.175*RIGHT)
            if i == 2:
                arrow.set_color(BLUE)
                arrow.rotate(np.pi)
            arrows.add(arrow)

            rect = SurroundingRectangle(VGroup(neuron, label))
            if i == 2:
                rect.set_color(BLUE)
            else:
                rect.set_color(RED)
            rects.add(rect)

        self.play(
            output_labels.shift, SMALL_BUFF*RIGHT,
            LaggedStartMap(GrowArrow, arrows, run_time = 1)
        )
        self.wait()

        #Show changing activations
        anims = []
        def get_decimal_update(start, end):
            return lambda a : interpolate(start, end, a)
        for i in range(10):
            target = 1.0 if i == 2 else 0.01
            anims += [neurons[i].set_fill, WHITE, target]
            decimal = self.decimals[i]
            anims.append(ChangingDecimal(
                decimal,
                get_decimal_update(decimal.number, target),
                num_decimal_places = 1
            ))
            anims.append(UpdateFromFunc(
                self.decimals[i],
                lambda m : m.set_fill(WHITE if m.number < 0.8 else BLACK)
            ))

        self.play(
            *anims,
            run_time = 3,
            rate_func = there_and_back
        )

        two_rect = rects[2]
        eight_rect = rects[8].copy()
        non_two_rects = VGroup(*[r for r in rects if r is not two_rect])
        self.play(ShowCreation(two_rect))
        self.wait()
        self.remove(two_rect)
        self.play(ReplacementTransform(two_rect.copy(), non_two_rects))
        self.wait()
        self.play(LaggedStartMap(FadeOut, non_two_rects, run_time = 1))
        self.play(LaggedStartMap(
            ApplyFunction, arrows,
            lambda arrow : (
                lambda m : m.scale(0.5).set_color(YELLOW),
                arrow,
            ),
            rate_func = wiggle
        ))
        self.play(ShowCreation(two_rect))
        self.wait()
        self.play(ReplacementTransform(two_rect, eight_rect))
        self.wait()
        self.play(FadeOut(eight_rect))

        self.arrows = arrows

    def focus_on_one_neuron(self, expanded_mobjects):
        network_mob = self.network_mob
        neurons = network_mob.layers[-1].neurons
        labels = network_mob.output_labels
        two_neuron = neurons[2]
        neurons.remove(two_neuron)
        two_label = labels[2]
        labels.remove(two_label)
        expanded_mobjects.remove(*two_neuron.edges_in)
        two_decimal = self.decimals[2]
        self.decimals.remove(two_decimal)
        two_arrow = self.arrows[2]
        self.arrows.remove(two_arrow)

        to_fade = VGroup(*it.chain(
            network_mob.layers[:2],
            network_mob.edge_groups[:2],
            expanded_mobjects,
            self.decimals,
            self.arrows
        ))

        self.play(FadeOut(to_fade))
        self.wait()
        for mob in expanded_mobjects:
            if mob in [neurons, labels]:
                mob.scale(0.5)
                mob.move_to(mob.saved_state)
            else:
                mob.restore()
        for d, a, n in zip(self.decimals, self.arrows, neurons):
            d.scale(0.5)
            d.move_to(n)
            a.scale(0.5)
            a.move_to(n.get_right())
            a.shift(SMALL_BUFF*RIGHT)
        labels.shift(SMALL_BUFF*RIGHT)

        self.set_variables_as_attrs(
            two_neuron, two_label, two_arrow, two_decimal,
        )

    def show_activation_formula(self):
        rhs = OldTex(
            "=", "\\sigma(",
            "w_0", "a_0", "+",
            "w_1", "a_1", "+",
            "\\cdots", "+",
            "w_{n-1}", "a_{n-1}", "+",
            "b", ")"
        )
        equals = rhs[0]
        sigma = VGroup(rhs[1], rhs[-1])
        w_terms = rhs.get_parts_by_tex("w_")
        a_terms = rhs.get_parts_by_tex("a_")
        plus_terms = rhs.get_parts_by_tex("+")
        b = rhs.get_part_by_tex("b", substring = False)
        dots = rhs.get_part_by_tex("dots")

        w_terms.set_color(BLUE)
        b.set_color(MAROON_B)
        sigma.set_color(YELLOW)

        rhs.to_corner(UP+RIGHT)
        sigma.save_state()
        sigma.shift(DOWN)
        sigma.set_fill(opacity = 0)

        prev_neurons = self.network_mob.layers[-2].neurons
        edges = self.two_neuron.edges_in

        neuron_copy = VGroup(
            self.two_neuron.copy(),
            self.two_decimal.copy(),
        )

        self.play(
            neuron_copy.next_to, equals.get_left(), LEFT,
            self.curr_image.to_corner, UP+LEFT,
            Write(equals)
        )
        self.play(
            ReplacementTransform(edges.copy(), w_terms),
            Write(VGroup(*plus_terms[:-1])),
            Write(dots),
            run_time = 1.5
        )
        self.wait()
        self.play(ReplacementTransform(
            prev_neurons.copy(), a_terms,
            path_arc = np.pi/2
        ))
        self.wait()
        self.play(
            Write(plus_terms[-1]),
            Write(b)
        )
        self.wait()
        self.play(sigma.restore)
        self.wait()
        for mob in b, w_terms, a_terms:
            self.play(
                mob.shift, MED_SMALL_BUFF*DOWN,
                rate_func = there_and_back,
                lag_ratio = 0.5,
                run_time = 1.5
            )
        self.wait()

        self.set_variables_as_attrs(
            rhs, w_terms, a_terms, b,
            lhs = neuron_copy
        )

    def three_ways_to_increase(self):
        w_terms = self.w_terms
        a_terms = self.a_terms
        b = self.b
        increase_words = VGroup(
            OldTexText("Increase", "$b$"),
            OldTexText("Increase", "$w_i$"),
            OldTexText("Change", "$a_i$"),
        )
        for words in increase_words:
            words.set_color_by_tex_to_color_map({
                "b" : b.get_color(),
                "w_" : w_terms.get_color(),
                "a_" : a_terms.get_color(),
            })
        increase_words.arrange(
            DOWN, aligned_edge = LEFT,
            buff = LARGE_BUFF
        )
        increase_words.to_edge(LEFT)

        mobs = [b, w_terms[0], a_terms[0]]
        for words, mob in zip(increase_words, mobs):
            self.play(
                Write(words[0], run_time = 1),
                ReplacementTransform(mob.copy(), words[1])
            )
            self.wait()

        self.increase_words = increase_words

    def note_connections_to_brightest_neurons(self):
        w_terms = self.w_terms
        a_terms = self.a_terms
        increase_words = self.increase_words
        prev_neurons = self.network_mob.layers[-2].neurons
        edges = self.two_neuron.edges_in

        prev_activations = np.array([n.get_fill_opacity() for n in prev_neurons])
        sorted_indices = np.argsort(prev_activations.flatten())
        bright_neurons = VGroup()
        dim_neurons = VGroup()
        edges_to_bright_neurons = VGroup()
        for i in sorted_indices[:5]:
            dim_neurons.add(prev_neurons[i])
        for i in sorted_indices[-4:]:
            bright_neurons.add(prev_neurons[i])
            edges_to_bright_neurons.add(edges[i])
        bright_edges = edges_to_bright_neurons.copy()
        bright_edges.set_stroke(YELLOW, 4)

        added_words = OldTexText("in proportion to $a_i$")
        added_words.next_to(
            increase_words[1], DOWN, 
            1.5*SMALL_BUFF, LEFT
        )
        added_words.set_color(YELLOW)

        terms_rect = SurroundingRectangle(
            VGroup(w_terms[0], a_terms[0]),
            color = WHITE
        )

        self.play(LaggedStartMap(
            ApplyFunction, edges,
            lambda edge : (
                lambda m : m.rotate(np.pi/12).set_stroke(YELLOW),
                edge
            ),
            rate_func = wiggle
        ))
        self.wait()
        self.play(
            ShowCreation(bright_edges),
            ShowCreation(bright_neurons)
        )
        self.play(LaggedStartMap(
            ApplyMethod, bright_neurons,
            lambda m : (m.shift, MED_LARGE_BUFF*LEFT),
            rate_func = there_and_back
        ))
        self.wait()
        self.play(
            ReplacementTransform(bright_edges[0].copy(), w_terms[0]),
            ReplacementTransform(bright_neurons[0].copy(), a_terms[0]),
            ShowCreation(terms_rect)
        )
        self.wait()
        for x in range(2):
            self.play(LaggedStartMap(ShowCreationThenDestruction, bright_edges))
        self.play(LaggedStartMap(ShowCreation, bright_edges))
        self.play(LaggedStartMap(
            ApplyMethod, dim_neurons,
            lambda m : (m.shift, MED_LARGE_BUFF*LEFT),
            rate_func = there_and_back
        ))
        self.play(FadeOut(terms_rect))
        self.wait()
        self.play(
            self.curr_image.shift, MED_LARGE_BUFF*RIGHT,
            rate_func = wiggle
        )
        self.wait()
        self.play(Write(added_words))
        self.wait()

        self.set_variables_as_attrs(
            bright_neurons, bright_edges,
            in_proportion_to_a = added_words
        )

    def fire_together_wire_together(self):
        bright_neurons = self.bright_neurons
        bright_edges = self.bright_edges
        two_neuron = self.two_neuron
        two_decimal = self.two_decimal
        two_activation = two_decimal.number

        def get_edge_animation():
            return LaggedStartMap(
                ShowCreationThenDestruction, bright_edges,
                lag_ratio = 0.7
            )
        neuron_arrows = VGroup(*[
            Vector(MED_LARGE_BUFF*RIGHT).next_to(n, LEFT)
            for n in bright_neurons
        ])
        two_neuron_arrow = Vector(MED_LARGE_BUFF*DOWN)
        two_neuron_arrow.next_to(two_neuron, UP)
        VGroup(neuron_arrows, two_neuron_arrow).set_color(YELLOW)

        neuron_rects = VGroup(*list(map(
            SurroundingRectangle, bright_neurons
        )))
        two_neuron_rect = SurroundingRectangle(two_neuron)
        seeing_words = OldTexText("Seeing a 2")
        seeing_words.scale(0.8)
        thinking_words = OldTexText("Thinking about a 2")
        thinking_words.scale(0.8)
        seeing_words.next_to(neuron_rects, UP)
        thinking_words.next_to(two_neuron_arrow, RIGHT)

        morty = Mortimer()
        morty.scale(0.8)
        morty.to_corner(DOWN+RIGHT)
        words = OldTexText("""
            ``Neurons that \\\\
            fire together \\\\
            wire together''
        """)
        words.to_edge(RIGHT)

        self.play(FadeIn(morty))
        self.play(
            Write(words),
            morty.change, "speaking", words
        )
        self.play(Blink(morty))
        self.play(
            get_edge_animation(),
            morty.change, "pondering", bright_edges
        )
        self.play(get_edge_animation())
        self.play(
            LaggedStartMap(GrowArrow, neuron_arrows),
            get_edge_animation(),
        )
        self.play(
            GrowArrow(two_neuron_arrow),
            morty.change, "raise_right_hand", two_neuron
        )
        self.play(
            ApplyMethod(two_neuron.set_fill, WHITE, 1),
            ChangingDecimal(
                two_decimal,
                lambda a : interpolate(two_activation, 1, a),
                num_decimal_places = 1,
            ),
            UpdateFromFunc(
                two_decimal,
                lambda m : m.set_color(WHITE if m.number < 0.8 else BLACK),
            ),
            LaggedStartMap(ShowCreation, bright_edges),
            run_time = 2,
        )
        self.wait()
        self.play(
            LaggedStartMap(ShowCreation, neuron_rects),
            Write(seeing_words, run_time = 2),
            morty.change, "thinking", seeing_words
        )
        self.wait()
        self.play(
            ShowCreation(two_neuron_rect),
            Write(thinking_words, run_time = 2),
            morty.look_at, thinking_words
        )
        self.wait()
        self.play(LaggedStartMap(FadeOut, VGroup(
            neuron_rects, two_neuron_rect,
            seeing_words, thinking_words,
            words, morty,
            neuron_arrows, two_neuron_arrow,
            bright_edges, 
        )))
        self.play(
            ApplyMethod(two_neuron.set_fill, WHITE, two_activation),
            ChangingDecimal(
                two_decimal,
                lambda a : interpolate(1, two_activation, a),
                num_decimal_places = 1,
            ),
            UpdateFromFunc(
                two_decimal,
                lambda m : m.set_color(WHITE if m.number < 0.8 else BLACK),
            ),
        )

    def show_desired_increase_to_previous_neurons(self):
        increase_words = self.increase_words
        two_neuron = self.two_neuron
        two_decimal = self.two_decimal
        edges = two_neuron.edges_in
        prev_neurons = self.network_mob.layers[-2].neurons

        positive_arrows = VGroup()
        negative_arrows = VGroup()
        all_arrows = VGroup()
        positive_edges = VGroup()
        negative_edges = VGroup()
        positive_neurons = VGroup()
        negative_neurons = VGroup()
        for neuron, edge in zip(prev_neurons, edges):
            value = self.get_edge_value(edge)
            arrow = self.get_neuron_nudge_arrow(edge)
            arrow.move_to(neuron.get_left())
            arrow.shift(SMALL_BUFF*LEFT)
            all_arrows.add(arrow)
            if value > 0:
                positive_arrows.add(arrow)
                positive_edges.add(edge)
                positive_neurons.add(neuron)
            else:
                negative_arrows.add(arrow)
                negative_edges.add(edge)
                negative_neurons.add(neuron)
        for s_edges in positive_edges, negative_edges:
            s_edges.alt_position = VGroup(*[
                Line(LEFT, RIGHT, color = s_edge.get_color())
                for s_edge in s_edges
            ])
            s_edges.alt_position.arrange(DOWN, MED_SMALL_BUFF)
            s_edges.alt_position.to_corner(DOWN+RIGHT, LARGE_BUFF)

        added_words = OldTexText("in proportion to $w_i$")
        added_words.set_color(self.w_terms.get_color())
        added_words.next_to(
            increase_words[-1], DOWN,
            SMALL_BUFF, aligned_edge = LEFT
        )

        self.play(LaggedStartMap(
            ApplyFunction, prev_neurons,
            lambda neuron : (
                lambda m : m.scale(0.5).set_color(YELLOW),
                neuron
            ),
            rate_func = wiggle
        ))
        self.wait()
        for positive in [True, False]:
            if positive:
                arrows = positive_arrows
                s_edges = positive_edges
                neurons = positive_neurons
                color = self.positive_edge_color
            else:
                arrows = negative_arrows
                s_edges = negative_edges
                neurons = negative_neurons
                color = self.negative_edge_color
            s_edges.save_state()
            self.play(Transform(s_edges, s_edges.alt_position))
            self.wait(0.5)
            self.play(s_edges.restore)
            self.play(
                LaggedStartMap(GrowArrow, arrows),
                neurons.set_stroke, color
            )
            self.play(ApplyMethod(
                neurons.set_fill, color, 1,
                rate_func = there_and_back,
            ))
        self.wait()
        self.play(
            two_neuron.set_fill, None, 0.8,
            ChangingDecimal(
                two_decimal,
                lambda a : two_neuron.get_fill_opacity()
            ),
            run_time = 3,
            rate_func = there_and_back
        )
        self.wait()
        self.play(*[
            ApplyMethod(
                edge.set_stroke, None, 3*edge.get_stroke_width(),
                rate_func = there_and_back, 
                run_time = 2
            )
            for edge in edges
        ])
        self.wait()
        self.play(Write(added_words, run_time = 1))
        self.play(prev_neurons.set_stroke, WHITE, 2)

        self.set_variables_as_attrs(
            in_proportion_to_w = added_words,
            prev_neuron_arrows = all_arrows,
        )

    def only_keeping_track_of_changes(self):
        arrows = self.prev_neuron_arrows
        prev_neurons = self.network_mob.layers[-2].neurons
        rect = SurroundingRectangle(VGroup(arrows, prev_neurons))

        words1 = OldTexText("No direct influence")
        words1.next_to(rect, UP)
        words2 = OldTexText("Just keeping track")
        words2.move_to(words1)

        edges = self.network_mob.edge_groups[-2]

        self.play(ShowCreation(rect))
        self.play(Write(words1))
        self.play(LaggedStartMap(
            Indicate, prev_neurons,
            rate_func = wiggle
        ))
        self.wait()
        self.play(LaggedStartMap(
            ShowCreationThenDestruction, edges
        ))
        self.play(Transform(words1, words2))
        self.wait()
        self.play(FadeOut(VGroup(words1, rect)))

    def show_other_output_neurons(self):
        two_neuron = self.two_neuron
        two_decimal = self.two_decimal
        two_arrow = self.two_arrow
        two_label = self.two_label
        two_edges = two_neuron.edges_in

        prev_neurons = self.network_mob.layers[-2].neurons
        neurons = self.network_mob.layers[-1].neurons
        prev_neuron_arrows = self.prev_neuron_arrows
        arrows_to_fade = VGroup(prev_neuron_arrows)

        output_labels = self.network_mob.output_labels
        quads = list(zip(neurons, self.decimals, self.arrows, output_labels))

        self.revert_to_original_skipping_status()
        self.play(
            two_neuron.restore,
            two_decimal.scale, 0.5,
            two_decimal.move_to, two_neuron.saved_state,
            two_arrow.scale, 0.5,
            two_arrow.next_to, two_neuron.saved_state, RIGHT, 0.5*SMALL_BUFF,
            two_label.scale, 0.5,
            two_label.next_to, two_neuron.saved_state, RIGHT, 1.5*SMALL_BUFF,
            FadeOut(VGroup(self.lhs, self.rhs)),
            *[e.restore for e in two_edges]
        )
        for neuron, decimal, arrow, label in quads[:2] + quads[2:5]:
            plusses = VGroup()
            new_arrows = VGroup()
            for edge, prev_arrow in zip(neuron.edges_in, prev_neuron_arrows):
                plus = OldTex("+").scale(0.5)
                plus.move_to(prev_arrow)
                plus.shift(2*SMALL_BUFF*LEFT)
                new_arrow = self.get_neuron_nudge_arrow(edge)
                new_arrow.move_to(plus)
                new_arrow.shift(2*SMALL_BUFF*LEFT)
                plusses.add(plus)
                new_arrows.add(new_arrow)

            self.play(
                FadeIn(VGroup(neuron, decimal, arrow, label)),
                LaggedStartMap(ShowCreation, neuron.edges_in),
            )
            self.play(
                ReplacementTransform(neuron.edges_in.copy(), new_arrows),
                Write(plusses, run_time = 2)
            )

            arrows_to_fade.add(new_arrows, plusses)
            prev_neuron_arrows = new_arrows

        all_dots_plus = VGroup()
        for arrow in prev_neuron_arrows:
            dots_plus = OldTex("\\cdots +")
            dots_plus.scale(0.5)
            dots_plus.move_to(arrow.get_center(), RIGHT)
            dots_plus.shift(2*SMALL_BUFF*LEFT)
            all_dots_plus.add(dots_plus)
        arrows_to_fade.add(all_dots_plus)

        self.play(
            LaggedStartMap(
                FadeIn, VGroup(*it.starmap(VGroup, quads[5:])),
            ),
            LaggedStartMap(
                FadeIn, VGroup(*[n.edges_in for n in neurons[5:]])
            ),
            Write(all_dots_plus),
            run_time = 3,
        )
        self.wait(2)

        ##
        words = OldTexText("Propagate backwards")
        words.to_edge(UP)
        words.set_color(BLUE)
        target_arrows = prev_neuron_arrows.copy()
        target_arrows.next_to(prev_neurons, RIGHT, SMALL_BUFF)
        rect = SurroundingRectangle(VGroup(
            self.network_mob.layers[-1],
            self.network_mob.output_labels
        ))
        rect.set_fill(BLACK, 1)
        rect.set_stroke(BLACK, 0)
        self.play(Write(words))
        self.wait()
        self.play(
            FadeOut(self.network_mob.edge_groups[-1]),
            FadeIn(rect),
            ReplacementTransform(arrows_to_fade, VGroup(target_arrows)),
        )
        self.prev_neuron_arrows = target_arrows

    def show_recursion(self):
        network_mob = self.network_mob
        words_to_fade = VGroup(
            self.increase_words,
            self.in_proportion_to_w,
            self.in_proportion_to_a,
        )
        edges = network_mob.edge_groups[1]
        neurons = network_mob.layers[2].neurons
        prev_neurons = network_mob.layers[1].neurons
        for neuron in neurons:
            neuron.edges_in.save_state()

        self.play(
            FadeOut(words_to_fade),
            FadeIn(prev_neurons),
            LaggedStartMap(ShowCreation, edges),
        )
        self.wait()
        for neuron, arrow in zip(neurons, self.prev_neuron_arrows):
            edge_copies = neuron.edges_in.copy()
            for edge in edge_copies:
                edge.set_stroke(arrow.get_color(), 2)
                edge.rotate(np.pi)
            self.play(
                edges.set_stroke, None, 0.15,
                neuron.edges_in.restore,
            )
            self.play(ShowCreationThenDestruction(edge_copies))
            self.remove(edge_copies)


    ####

    def get_neuron_nudge_arrow(self, edge):
        value = self.get_edge_value(edge)
        height = np.sign(value)*0.1 + 0.1*value
        arrow = Vector(height*UP, color = edge.get_color())
        return arrow

    def get_edge_value(self, edge):
        value = edge.get_stroke_width()
        if Color(edge.get_stroke_color()) == Color(self.negative_edge_color):
            value *= -1
        return value
