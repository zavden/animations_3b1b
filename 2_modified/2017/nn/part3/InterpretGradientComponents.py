# ==============================================================================
# Scene:      InterpretGradientComponents
# Source:     videos/_2017/nn/part3.py (lines 55-348)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/nn/network.py, _2017/nn/part1.py, _2017/nn/part2.py
#
# Run from this folder:
#     manimgl InterpretGradientComponents.py InterpretGradientComponents -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Provide package `nn` (network.py with binary-mode pickle fix, mnist_loader.py reading a small synthetic MNIST stand-in) through data_files, since the original mnist.pkl.gz is not in the repo.
#   - Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
#   - Python 2 integer division used as an index/count -> //.
#   - Python 3: zip()/map()/filter() return iterators, wrap in list() before slicing.
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2017/nn/nn_pkg/mnist_mini.npz (synthetic MNIST stand-in, built from the 100 real digits of image_map by make_nn_support.py)
# ==============================================================================

#### Libraries
# Standard library
import os
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

POSITIVE_COLOR = BLUE


NEGATIVE_COLOR = RED


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


def get_decimal_vector(nums, with_dots = True):
    decimals = VGroup()
    for num in nums:
        decimal = DecimalNumber(num)
        if num > 0:
            decimal.set_color(POSITIVE_COLOR)
        else:
            decimal.set_color(NEGATIVE_COLOR)
        decimals.add(decimal)
    contents = VGroup(*decimals)
    if with_dots:
        dots = OldTex("\\vdots")
        contents.submobjects.insert(len(decimals)//2, dots)  # CHANGE: Python 2 integer division used as an index/count -> //.
    contents.arrange(DOWN)
    lb, rb = brackets = OldTex("\\big[", "\\big]")
    brackets.scale(2)
    brackets.stretch_to_fit_height(1.2*contents.get_height())
    lb.next_to(contents, LEFT, SMALL_BUFF)
    rb.next_to(contents, RIGHT, SMALL_BUFF)

    result = VGroup(lb, contents, brackets)
    result.lb = lb
    result.rb = rb
    result.brackets = brackets
    result.decimals = decimals
    result.contents = contents
    if with_dots:
        result.dots = dots
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


class GradientNudging(PreviewLearning):
    CONFIG = {
        "n_steps" : 10,
        "n_decimals" : 8,
    }
    def construct(self):
        self.setup_network_mob()
        self.add_gradient()
        self.change_weights_repeatedly()

    def setup_network_mob(self):
        network_mob = self.network_mob
        self.color_network_edges()
        network_mob.scale(0.7)
        network_mob.to_corner(DOWN+RIGHT)

    def add_gradient(self):
        lhs = OldTex(
            "-", "\\nabla", "C(", "\\dots", ")", "="
        )
        brace = Brace(lhs.get_part_by_tex("dots"), DOWN)
        words = brace.get_text("All weights \\\\ and biases")
        words.scale(0.8, about_point = words.get_top())
        np.random.seed(3)
        nums = 4*(np.random.random(self.n_decimals)-0.5)
        vect = get_decimal_vector(nums)
        vect.next_to(lhs, RIGHT)
        group = VGroup(lhs, brace, words, vect)
        group.to_corner(UP+LEFT)

        self.add(*group)

        self.set_variables_as_attrs(
            grad_lhs = lhs,
            grad_vect = vect,
            grad_arg_words = words,
            grad_arg_brace = brace
        )

    def change_weights_repeatedly(self):
        network_mob = self.network_mob
        edges = VGroup(*reversed(list(
            it.chain(*network_mob.edge_groups)
        )))

        decimals = self.grad_vect.decimals

        words = OldTexText(
            "Change by some small\\\\",
            "multiple of $-\\nabla C(\\dots)$"
        )
        words.next_to(network_mob, UP).to_edge(UP)
        arrows = VGroup(*[
            Arrow(
                words.get_bottom(),
                edge_group.get_top(),
                color = WHITE
            )
            for edge_group in network_mob.edge_groups
        ])

        mover = VGroup(*decimals.family_members_with_points()).copy()
        # mover.set_fill(opacity = 0)
        mover.set_stroke(width = 0)
        target = VGroup(*self.network_mob.edge_groups.family_members_with_points()).copy()
        target.set_fill(opacity = 0)
        ApplyMethod(target.set_stroke, YELLOW, 2).update(0.3)
        self.play(
            ReplacementTransform(mover, target),
            FadeIn(words),
            LaggedStartMap(GrowArrow, arrows, run_time = 1)
        )
        self.play(FadeOut(target))
        self.play(self.get_edge_change_anim(edges))
        self.play(*self.get_decimal_change_anims(decimals))
        for x in range(self.n_steps):
            self.play(self.get_edge_change_anim(edges))
            self.play(*self.get_decimal_change_anims(decimals))
        self.wait()

    ###

    def get_edge_change_anim(self, edges):
        target_nums = 6*(np.random.random(len(edges))-0.5)
        edges.generate_target()
        for edge, target_num in zip(edges.target, target_nums):
            curr_num = edge.get_stroke_width()
            if Color(edge.get_stroke_color()) == Color(self.negative_edge_color):
                curr_num *= -1
            new_num = interpolate(curr_num, target_num, 0.2)
            if new_num > 0:
                new_color = self.positive_edge_color
            else:
                new_color = self.negative_edge_color
            edge.set_stroke(new_color, abs(new_num))
            edge.rotate(np.pi)
        return MoveToTarget(
            edges,
            lag_ratio = 0.5,
            run_time = 1.5
        )

    def get_decimal_change_anims(self, decimals):
        words = OldTexText("Recompute \\\\ gradient")
        words.next_to(decimals, DOWN, MED_LARGE_BUFF)
        def wrf(t):
            if t < 1./3:
                return smooth(3*t)
            elif t < 2./3:
                return 1
            else:
                return smooth(3 - 3*t)

        changes = 0.2*(np.random.random(len(decimals))-0.5)
        def generate_change_func(x, dx):
            return lambda a : interpolate(x, x+dx, a)
        return [
            ChangingDecimal(
                decimal, 
                generate_change_func(decimal.number, change)
            )
            for decimal, change in zip(decimals, changes)
        ] + [
            FadeIn(words, rate_func = wrf, run_time = 1.5, remover = True)
        ]



# ----- From _2017/nn/part3.py -----

class InterpretGradientComponents(GradientNudging):
    CONFIG = {
        "network_mob_config" : {
            "layer_to_layer_buff" : 3,
        },
        "stroke_width_exp" : 2,
        "n_decimals" : 6,
        "n_steps" : 3,
        "start_cost" : 3.48,
        "delta_cost" : -0.21,
    }
    def construct(self):
        self.setup_network()
        self.add_cost()
        self.add_gradient()
        self.change_weights_repeatedly()
        self.ask_about_high_dimensions()
        self.circle_magnitudes()
        self.isolate_particular_weights()
        self.shift_cost_expression()
        self.tweak_individual_weights()

    def setup_network(self):
        self.network_mob.scale(0.55)
        self.network_mob.to_corner(UP+RIGHT)
        self.color_network_edges()

    def add_cost(self):
        rect = SurroundingRectangle(self.network_mob)
        rect.set_color(RED)
        arrow = Vector(DOWN, color = RED)
        arrow.shift(rect.get_bottom())
        cost = DecimalNumber(self.start_cost)
        cost.set_color(RED)
        cost.next_to(arrow, DOWN)

        cost_expression = OldTex(
            "C(", "w_0, w_1, \\dots, w_{13{,}001}", ")", "="
        )
        for tex in "()":
            cost_expression.set_color_by_tex(tex, RED)
        cost_expression.next_to(cost, DOWN)
        cost_group = VGroup(cost_expression, cost)
        cost_group.arrange(RIGHT)
        cost_group.next_to(arrow, DOWN)

        self.add(rect, arrow, cost_group)

        self.set_variables_as_attrs(
            cost, cost_expression, cost_group,
            network_rect = rect
        )

    def change_weights_repeatedly(self):
        decimals = self.grad_vect.decimals
        grad_terms = self.grad_vect.contents
        edges = VGroup(*reversed(list(
            it.chain(*self.network_mob.edge_groups)
        )))
        cost = self.cost

        for x in range(self.n_steps):
            self.move_grad_terms_into_position(
                grad_terms.copy(),
                *self.get_weight_adjustment_anims(edges, cost)
            )
            self.play(*self.get_decimal_change_anims(decimals))

    def ask_about_high_dimensions(self):
        grad_vect = self.grad_vect

        words = OldTexText(
            "Direction in \\\\ ${13{,}002}$ dimensions?!?")
        words.set_color(YELLOW)
        words.move_to(grad_vect).to_edge(DOWN)
        arrow = Arrow(
            words.get_top(),
            grad_vect.get_bottom(),
            buff = SMALL_BUFF
        )

        randy = Randolph()
        randy.scale(0.6)
        randy.next_to(words, LEFT)
        randy.shift_onto_screen()

        self.play(
            Write(words, run_time = 2), 
            GrowArrow(arrow),
        )
        self.play(FadeIn(randy))
        self.play(randy.change, "confused", words)
        self.play(Blink(randy))
        self.wait()
        self.play(*list(map(FadeOut, [randy, words, arrow])))

    def circle_magnitudes(self):
        rects = VGroup()
        for decimal in self.grad_vect.decimals:
            rects.add(SurroundingRectangle(VGroup(*decimal[-8:])))
        rects.set_color(WHITE)

        self.play(LaggedStartMap(ShowCreation, rects))
        self.play(FadeOut(rects))

    def isolate_particular_weights(self):
        vect_contents = self.grad_vect.contents
        w_terms = self.cost_expression[1]

        edges = self.network_mob.edge_groups
        edge1 = self.network_mob.layers[1].neurons[3].edges_in[0].copy()
        edge2 = self.network_mob.layers[1].neurons[9].edges_in[15].copy()
        VGroup(edge1, edge2).set_stroke(width = 4)
        d1 = DecimalNumber(3.2)
        d2 = DecimalNumber(0.1)
        VGroup(edge1, d1).set_color(YELLOW)
        VGroup(edge2, d2).set_color(MAROON_B)
        new_vect_contents = VGroup(
            OldTex("\\vdots"),
            d1, OldTex("\\vdots"),
            d2, OldTex("\\vdots"),
        )
        new_vect_contents.arrange(DOWN)
        new_vect_contents.move_to(vect_contents)

        new_w_terms = OldTex(
            "\\dots", "w_n", "\\dots", "w_k", "\\dots"
        )
        new_w_terms.move_to(w_terms, DOWN)
        new_w_terms[1].set_color(d1.get_color())
        new_w_terms[3].set_color(d2.get_color())

        for d, edge in (d1, edge1), (d2, edge2):
            d.arrow = Arrow(
                d.get_right(), edge.get_center(),
                color = d.get_color()
            )

        self.play(
            FadeOut(vect_contents),
            FadeIn(new_vect_contents),
            FadeOut(w_terms),
            FadeIn(new_w_terms),
            edges.set_stroke, GREY_B, 0.35,
        )
        self.play(GrowArrow(d1.arrow))
        self.play(ShowCreation(edge1))
        self.wait()
        self.play(GrowArrow(d2.arrow))
        self.play(ShowCreation(edge2))
        self.wait(2)

        self.cost_expression.remove(w_terms)
        self.cost_expression.add(new_w_terms)
        self.set_variables_as_attrs(
            edge1, edge2, new_w_terms, 
            new_decimals = VGroup(d1, d2)
        )

    def shift_cost_expression(self):
        self.play(self.cost_group.shift, DOWN+0.5*LEFT)

    def tweak_individual_weights(self):
        cost = self.cost
        cost_num = cost.number
        edges = VGroup(self.edge1, self.edge2)
        decimals = self.new_decimals
        changes = (1.0, 1./32)
        wn = self.new_w_terms[1]
        wk = self.new_w_terms[3]

        number_line_template = NumberLine(
            x_min = -1,
            x_max = 1,
            tick_frequency = 0.25,
            big_tick_numbers = [],
            color = WHITE
        )
        for term in wn, wk, cost:
            term.number_line = number_line_template.copy()
            term.brace = Brace(term.number_line, DOWN, buff = SMALL_BUFF)
            group = VGroup(term.number_line, term.brace)
            group.next_to(term, UP)
            term.dot = Dot()
            term.dot.set_color(term.get_color())
            term.dot.move_to(term.number_line.get_center())
            term.dot.save_state()
            term.dot.move_to(term)
            term.dot.set_fill(opacity = 0)
            term.words = OldTexText("Nudge this weight")
            term.words.scale(0.7)
            term.words.next_to(term.number_line, UP, MED_SMALL_BUFF)

        groups = [
            VGroup(d, d.arrow, edge, w)
            for d, edge, w in zip(decimals, edges, [wn, wk])
        ]
        for group in groups:
            group.save_state()

        for i in range(2):
            group1, group2 = groups[i], groups[1-i]
            change = changes[i]
            edge = edges[i]
            w = group1[-1]
            added_anims = []
            if i == 0:
                added_anims = [
                    GrowFromCenter(cost.brace),
                    ShowCreation(cost.number_line),
                    cost.dot.restore
                ]
            self.play(
                group1.restore,
                group2.fade, 0.7,
                GrowFromCenter(w.brace),
                ShowCreation(w.number_line),
                w.dot.restore,
                Write(w.words, run_time = 1),
                *added_anims
            )
            for x in range(2):
                func = lambda a : interpolate(
                    cost_num, cost_num-change, a
                )
                self.play(
                    ChangingDecimal(cost, func),
                    cost.dot.shift, change*RIGHT,
                    w.dot.shift, 0.25*RIGHT,
                    edge.set_stroke, None, 8,
                    rate_func = lambda t : wiggle(t, 4),
                    run_time = 2,
                )
                self.wait()
            self.play(*list(map(FadeOut, [
                w.dot, w.brace, w.number_line, w.words
            ])))


    ######

    def move_grad_terms_into_position(self, grad_terms, *added_anims):
        cost_expression = self.cost_expression
        w_terms = self.cost_expression[1]
        points = VGroup(*[
            VectorizedPoint()
            for term in grad_terms
        ])
        points.arrange(RIGHT)
        points.replace(w_terms, dim_to_match = 0)

        grad_terms.generate_target()
        # CHANGE: Python 2 integer division used as an index/count -> //.
        grad_terms.target[len(grad_terms)//2].rotate(np.pi/2)
        grad_terms.target.arrange(RIGHT)
        grad_terms.target.set_width(cost_expression.get_width())
        grad_terms.target.next_to(cost_expression, DOWN)

        words = OldTexText("Nudge weights")
        words.scale(0.8)
        words.next_to(grad_terms.target, DOWN)

        self.play(
            MoveToTarget(grad_terms),
            FadeIn(words)
        )
        self.play(
            Transform(
                grad_terms, points,
                remover = True,
                lag_ratio = 0.5,
                run_time = 1
            ),
            FadeOut(words),
            *added_anims
        )

    def get_weight_adjustment_anims(self, edges, cost):
        start_cost = cost.number
        target_cost = start_cost + self.delta_cost
        w_terms = self.cost_expression[1]

        return [
            self.get_edge_change_anim(edges),
            LaggedStartMap(
                Indicate, w_terms,
                rate_func = there_and_back,
                run_time = 1.5,
            ),
            ChangingDecimal(
                cost, 
                lambda a : interpolate(start_cost, target_cost, a),
                run_time = 1.5
            )
        ]
