# ==============================================================================
# Scene:      SimplestNetworkExample
# Source:     videos/_2017/nn/part3.py (lines 2094-3621)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/nn/network.py, _2017/nn/part1.py, _2017/nn/part2.py
#
# Run from this folder:
#     manimgl SimplestNetworkExample.py SimplestNetworkExample -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Provide package `nn` (network.py with binary-mode pickle fix, mnist_loader.py reading a small synthetic MNIST stand-in) through data_files, since the original mnist.pkl.gz is not in the repo.
#   - Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
#   - Python 2 integer division used as an index/count -> //.
#   - Python 3: zip()/map()/filter() return iterators, wrap in list() before slicing.
#   - The formulas are OldTex (Cairo TexMobject) here: accept both classes.
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

class SimplestNetworkExample(PreviewLearning):
    CONFIG = {
        "random_seed" : 6,
        "z_color" : GREEN,
        "cost_color" : RED,
        "desired_output_color" : YELLOW,
        "derivative_scale_val" : 0.85,
    }
    def construct(self):
        self.seed_random_libraries()
        self.collapse_ordinary_network()
        self.show_weights_and_biases()
        self.focus_just_on_last_two_layers()
        self.label_neurons()
        self.show_desired_output()
        self.show_cost()
        self.show_activation_formula()
        self.introduce_z()
        self.break_into_computational_graph()
        self.show_preceding_layer_in_computational_graph()
        self.show_number_lines()
        self.ask_about_w_sensitivity()
        self.show_derivative_wrt_w()
        self.show_chain_of_events()
        self.show_chain_rule()
        self.name_chain_rule()
        self.indicate_everything_on_screen()
        self.prepare_for_derivatives()
        self.compute_derivatives()
        self.get_lost_in_formulas()
        self.fire_together_wire_together()
        self.organize_chain_rule_rhs()
        self.show_average_derivative()
        self.show_gradient()
        self.transition_to_derivative_wrt_b()
        self.show_derivative_wrt_b()
        self.show_derivative_wrt_a()
        self.show_previous_weight_and_bias()
        self.animate_long_path()

    def seed_random_libraries(self):
        np.random.seed(self.random_seed)
        random.seed(self.random_seed)

    def collapse_ordinary_network(self):
        network_mob = self.network_mob
        config = dict(self.network_mob_config)
        config.pop("include_output_labels")
        config.update({
            "edge_stroke_width" : 3,
            "edge_propogation_color" : YELLOW,
            "edge_propogation_time" : 1,
            "neuron_radius" : 0.3,
        })
        simple_network = Network(sizes = [1, 1, 1, 1])
        simple_network_mob = NetworkMobject(simple_network, **config)
        self.color_network_edges()
        s_edges = simple_network_mob.edge_groups
        for edge, weight_matrix in zip(s_edges, simple_network.weights):
            weight = weight_matrix[0][0]
            width = 2*abs(weight)
            color = BLUE if weight > 0 else RED
            edge.set_stroke(color, width)

        def edge_collapse_anims(edges, left_attachment_target):
            return [
                ApplyMethod(
                    e.put_start_and_end_on_with_projection,
                    left_attachment_target.get_right(), 
                    e.get_end()
                )
                for e in edges
            ]

        neuron = simple_network_mob.layers[0].neurons[0]
        self.play(
            ReplacementTransform(network_mob.layers[0], neuron),
            *edge_collapse_anims(network_mob.edge_groups[0], neuron)
        )
        for i, layer in enumerate(network_mob.layers[1:]):
            neuron = simple_network_mob.layers[i+1].neurons[0]
            prev_edges = network_mob.edge_groups[i]
            prev_edge_target = simple_network_mob.edge_groups[i]
            if i+1 < len(network_mob.edge_groups):
                edges = network_mob.edge_groups[i+1]
                added_anims = edge_collapse_anims(edges, neuron)
            else:
                added_anims = [FadeOut(network_mob.output_labels)]
            self.play(
                ReplacementTransform(layer, neuron),
                ReplacementTransform(prev_edges, prev_edge_target),
                *added_anims
            )
        self.remove(network_mob)
        self.add(simple_network_mob)
        self.network_mob = simple_network_mob
        self.network = self.network_mob.neural_network
        self.feed_forward(np.array([0.5]))
        self.wait()

    def show_weights_and_biases(self):
        network_mob = self.network_mob
        edges = VGroup(*[eg[0] for eg in network_mob.edge_groups])
        neurons = VGroup(*[
            layer.neurons[0] 
            for layer in network_mob.layers[1:]
        ])
        expression = OldTex(
            "C", "(", 
            "w_1", ",", "b_1", ",",
            "w_2", ",", "b_2", ",",
            "w_3", ",", "b_3",
            ")"
        )
        expression.shift(2*UP)
        expression.set_color_by_tex("C", RED)
        w_terms = expression.get_parts_by_tex("w_")
        for w, edge in zip(w_terms, edges):
            w.set_color(edge.get_color())
        b_terms = expression.get_parts_by_tex("b_")
        variables = VGroup(*it.chain(w_terms, b_terms))
        other_terms = VGroup(*[m for m in expression if m not in variables])
        random.shuffle(variables.submobjects)

        self.play(ReplacementTransform(edges.copy(), w_terms))
        self.wait()
        self.play(ReplacementTransform(neurons.copy(), b_terms))
        self.wait()
        self.play(Write(other_terms))
        for x in range(2):
            self.play(LaggedStartMap(
                Indicate, variables,
                rate_func = wiggle,
                run_time = 4,
            ))
        self.wait()
        self.play(
            FadeOut(other_terms),
            ReplacementTransform(w_terms, edges),
            ReplacementTransform(b_terms, neurons),
        )
        self.remove(expression)

    def focus_just_on_last_two_layers(self):
        to_fade = VGroup(*it.chain(*list(zip(
            self.network_mob.layers[:2],
            self.network_mob.edge_groups[:2],
        ))))
        for mob in to_fade:
            mob.save_state()
        self.play(LaggedStartMap(
            ApplyMethod, to_fade,
            lambda m : (m.fade, 0.9)
        ))
        self.wait()

        self.prev_layers = to_fade

    def label_neurons(self):
        neurons = VGroup(*[
            self.network_mob.layers[i].neurons[0]
            for i in (-1, -2)
        ])
        decimals = VGroup()
        a_labels = VGroup()
        a_label_arrows = VGroup()
        superscripts = ["L", "L-1"]
        superscript_rects = VGroup()
        for neuron, superscript in zip(neurons, superscripts):
            decimal = self.get_neuron_activation_decimal(neuron)
            label = OldTex("a^{(%s)}"%superscript)
            label.next_to(neuron, DOWN, buff = LARGE_BUFF)
            superscript_rect = SurroundingRectangle(VGroup(*label[1:]))
            arrow = Arrow(
                label[0].get_top(),
                neuron.get_bottom(),
                buff = SMALL_BUFF,
                color = WHITE
            )

            decimal.save_state()
            decimal.set_fill(opacity = 0)
            decimal.move_to(label)

            decimals.add(decimal)
            a_labels.add(label)
            a_label_arrows.add(arrow)
            superscript_rects.add(superscript_rect)

            self.play(
                Write(label, run_time = 1),
                GrowArrow(arrow),
            )
            self.play(decimal.restore)
            opacity = neuron.get_fill_opacity()
            self.play(
                neuron.set_fill, None, 0,
                ChangingDecimal(
                    decimal, 
                    lambda a : interpolate(opacity, 0.01, a)
                ),
                UpdateFromFunc(
                    decimal,
                    lambda d : d.set_fill(WHITE if d.number < 0.8 else BLACK)
                ),
                run_time = 2,
                rate_func = there_and_back,
            )
            self.wait()

        not_exponents = OldTexText("Not exponents")
        not_exponents.next_to(superscript_rects, DOWN, MED_LARGE_BUFF)
        not_exponents.set_color(YELLOW)

        self.play(
            LaggedStartMap(
                ShowCreation, superscript_rects,
                lag_ratio = 0.8, run_time = 1.5
            ),
            Write(not_exponents, run_time = 2)
        )
        self.wait()
        self.play(*list(map(FadeOut, [not_exponents, superscript_rects])))

        self.set_variables_as_attrs(
            a_labels, a_label_arrows, decimals,
            last_neurons = neurons
        )

    def show_desired_output(self):
        neuron = self.network_mob.layers[-1].neurons[0].copy()
        neuron.shift(2*RIGHT)
        neuron.set_fill(opacity = 1)
        decimal = self.get_neuron_activation_decimal(neuron)

        rect = SurroundingRectangle(neuron)
        words = OldTexText("Desired \\\\ output")
        words.next_to(rect, UP)

        y_label = OldTex("y")
        y_label.next_to(neuron, DOWN, LARGE_BUFF)
        y_label.align_to(self.a_labels, DOWN)
        y_label_arrow = Arrow(
            y_label, neuron, 
            color = WHITE,
            buff = SMALL_BUFF
        )
        VGroup(words, rect, y_label).set_color(self.desired_output_color)

        self.play(*list(map(FadeIn, [neuron, decimal])))
        self.play(
            ShowCreation(rect),
            Write(words, run_time = 1)
        )
        self.wait()
        self.play(
            Write(y_label, run_time = 1),
            GrowArrow(y_label_arrow)
        )
        self.wait()

        self.set_variables_as_attrs(
            y_label, y_label_arrow,
            desired_output_neuron = neuron,
            desired_output_decimal = decimal,
            desired_output_rect = rect,
            desired_output_words = words,
        )

    def show_cost(self):
        pre_a = self.a_labels[0].copy()
        pre_y = self.y_label.copy()

        cost_equation = OldTex(
            "C_0", "(", "\\dots", ")", "=",
            "(", "a^{(L)}", "-", "y", ")", "^2"
        )
        cost_equation.to_corner(UP+RIGHT)
        C0, a, y = [
            cost_equation.get_part_by_tex(tex)
            for tex in ("C_0", "a^{(L)}", "y")
        ]
        y.set_color(YELLOW)

        cost_word = OldTexText("Cost")
        cost_word.next_to(C0[0], LEFT, LARGE_BUFF)
        cost_arrow = Arrow(
            cost_word, C0,
            buff = SMALL_BUFF
        )
        VGroup(C0, cost_word, cost_arrow).set_color(self.cost_color)

        expression = OldTex(
            "\\text{For example: }"
            "(", "0.00", "-", "0.00", ")", "^2"
        )
        numbers = expression.get_parts_by_tex("0.00")
        non_numbers = VGroup(*[m for m in expression if m not in numbers])
        expression.next_to(cost_equation, DOWN, aligned_edge = RIGHT)
        decimals = VGroup(
            self.decimals[0],
            self.desired_output_decimal
        ).copy()
        decimals.generate_target()
        for d, n in zip(decimals.target, numbers):
            d.replace(n, dim_to_match = 1)
            d.set_color(n.get_color())

        self.play(
            ReplacementTransform(pre_a, a),
            ReplacementTransform(pre_y, y),
        )
        self.play(LaggedStartMap(
            FadeIn, VGroup(*[m for m in cost_equation if m not in [a, y]])
        ))
        self.play(
            MoveToTarget(decimals),
            FadeIn(non_numbers)
        )
        self.wait()
        self.play(
            Write(cost_word, run_time = 1),
            GrowArrow(cost_arrow)
        )
        self.play(C0.shift, MED_SMALL_BUFF*UP, rate_func = wiggle)
        self.wait()
        self.play(*list(map(FadeOut, [decimals, non_numbers])))

        self.set_variables_as_attrs(
            cost_equation, cost_word, cost_arrow
        )

    def show_activation_formula(self):
        neuron = self.network_mob.layers[-1].neurons[0]
        edge = self.network_mob.edge_groups[-1][0]
        pre_aL, pre_aLm1 = self.a_labels.copy()

        formula = OldTex(
            "a^{(L)}", "=", "\\sigma", "(",
            "w^{(L)}", "a^{(L-1)}", "+", "b^{(L)}", ")"
        )
        formula.next_to(neuron, UP, MED_LARGE_BUFF, RIGHT)
        aL, equals, sigma, lp, wL, aLm1, plus, bL, rp = formula
        wL.set_color(edge.get_color())
        weight_label = wL.copy()
        bL.set_color(MAROON_B)
        bias_label = bL.copy()
        sigma_group = VGroup(sigma, lp, rp)
        sigma_group.save_state()
        sigma_group.set_fill(opacity = 0)
        sigma_group.shift(DOWN)

        self.play(
            ReplacementTransform(pre_aL, aL),
            Write(equals)
        )
        self.play(ReplacementTransform(
            edge.copy(), wL
        ))
        self.wait()
        self.play(ReplacementTransform(pre_aLm1, aLm1))
        self.wait()
        self.play(Write(VGroup(plus, bL), run_time = 1))
        self.wait()
        self.play(sigma_group.restore)
        self.wait()

        weighted_sum_terms = VGroup(wL, aLm1, plus, bL)
        self.set_variables_as_attrs(
            formula, weighted_sum_terms
        )

    def introduce_z(self):
        terms = self.weighted_sum_terms
        terms.generate_target()
        terms.target.next_to(
            self.formula, UP, 
            buff = MED_LARGE_BUFF,
            aligned_edge = RIGHT
        )
        terms.target.shift(MED_LARGE_BUFF*RIGHT)
        equals = OldTex("=")
        equals.next_to(terms.target[0][0], LEFT)

        z_label = OldTex("z^{(L)}")
        z_label.next_to(equals, LEFT)
        z_label.align_to(terms.target, DOWN)
        z_label.set_color(self.z_color)
        z_label2 = z_label.copy()

        aL_start = VGroup(*self.formula[:4])
        aL_start.generate_target()
        aL_start.target.align_to(z_label, LEFT)
        z_label2.next_to(aL_start.target, RIGHT, SMALL_BUFF)
        z_label2.align_to(aL_start.target[0], DOWN)
        rp = self.formula[-1]
        rp.generate_target()
        rp.target.next_to(z_label2, RIGHT, SMALL_BUFF)
        rp.target.align_to(aL_start.target, DOWN)

        self.play(MoveToTarget(terms))
        self.play(Write(z_label), Write(equals))
        self.play(
            ReplacementTransform(z_label.copy(), z_label2),
            MoveToTarget(aL_start),
            MoveToTarget(rp),
        )
        self.wait()

        zL_formula = VGroup(z_label, equals, *terms)
        aL_formula = VGroup(*list(aL_start) + [z_label2, rp])
        self.set_variables_as_attrs(z_label, zL_formula, aL_formula)

    def break_into_computational_graph(self):
        network_early_layers = VGroup(*it.chain(
            self.network_mob.layers[:2],
            self.network_mob.edge_groups[:2]
        ))

        wL, aL, plus, bL = self.weighted_sum_terms
        top_terms = VGroup(wL, aL, bL).copy()
        zL = self.z_label.copy()
        aL = self.formula[0].copy()
        y = self.y_label.copy()
        C0 = self.cost_equation[0].copy()
        targets = VGroup()
        for mob in top_terms, zL, aL, C0:
            mob.generate_target()
            targets.add(mob.target)
        y.generate_target()
        top_terms.target.arrange(RIGHT, buff = MED_LARGE_BUFF)
        targets.arrange(DOWN, buff = LARGE_BUFF)
        targets.center().to_corner(DOWN+LEFT)
        y.target.next_to(aL.target, LEFT, LARGE_BUFF, DOWN)

        top_lines = VGroup(*[
            Line(
                term.get_bottom(), 
                zL.target.get_top(), 
                buff = SMALL_BUFF
            )
            for term in top_terms.target
        ])
        z_to_a_line, a_to_c_line, y_to_c_line = all_lines = [
            Line(
                m1.target.get_bottom(), 
                m2.target.get_top(), 
                buff = SMALL_BUFF
            )
            for m1, m2 in [
                (zL, aL), 
                (aL, C0), 
                (y, C0)
            ]
        ]
        for mob in [top_lines] + all_lines:
            yellow_copy = mob.copy().set_color(YELLOW)
            mob.flash = ShowCreationThenDestruction(yellow_copy)

        self.play(MoveToTarget(top_terms))
        self.wait()
        self.play(MoveToTarget(zL))
        self.play(
            ShowCreation(top_lines, lag_ratio = 0),
            top_lines.flash
        )
        self.wait()
        self.play(MoveToTarget(aL))
        self.play(
            network_early_layers.fade, 1,
            ShowCreation(z_to_a_line),
            z_to_a_line.flash
        )
        self.wait()
        self.play(MoveToTarget(y))
        self.play(MoveToTarget(C0))
        self.play(*it.chain(*[
            [ShowCreation(line), line.flash]
            for line in (a_to_c_line, y_to_c_line)
        ]))
        self.wait(2)

        comp_graph = VGroup()
        comp_graph.wL, comp_graph.aLm1, comp_graph.bL = top_terms
        comp_graph.top_lines = top_lines
        comp_graph.zL = zL
        comp_graph.z_to_a_line = z_to_a_line
        comp_graph.aL = aL
        comp_graph.y = y
        comp_graph.a_to_c_line = a_to_c_line
        comp_graph.y_to_c_line = y_to_c_line
        comp_graph.C0 = C0
        comp_graph.digest_mobject_attrs()
        self.comp_graph = comp_graph

    def show_preceding_layer_in_computational_graph(self):
        shift_vect = DOWN
        comp_graph = self.comp_graph
        comp_graph.save_state()
        comp_graph.generate_target()
        comp_graph.target.shift(shift_vect)
        rect = SurroundingRectangle(comp_graph.aLm1)

        attrs = ["wL", "aLm1", "bL", "zL"]
        new_terms = VGroup()
        for attr in attrs:
            term = getattr(comp_graph, attr)
            tex = term.get_tex()
            if "L-1" in tex:
                tex = tex.replace("L-1", "L-2")
            else:
                tex = tex.replace("L", "L-1")
            new_term = OldTex(tex)
            new_term.set_color(term.get_color())
            new_term.move_to(term)
            new_terms.add(new_term)
        new_edges = VGroup(
            comp_graph.top_lines.copy(),
            comp_graph.z_to_a_line.copy(),
        )
        new_subgraph = VGroup(new_terms, new_edges)
        new_subgraph.next_to(comp_graph.target, UP, SMALL_BUFF)
        self.wLm1 = new_terms[0]
        self.zLm1 = new_terms[-1]

        prev_neuron = self.network_mob.layers[1]
        prev_neuron.restore()
        prev_edge = self.network_mob.edge_groups[1]
        prev_edge.restore()

        self.play(
            ShowCreation(rect),
            FadeIn(prev_neuron),
            ShowCreation(prev_edge)
        )
        self.play(
            ReplacementTransform(
                VGroup(prev_neuron, prev_edge).copy(),
                new_subgraph
            ),
            UpdateFromAlphaFunc(
                new_terms,
                lambda m, a : m.set_fill(opacity = a)
            ),
            MoveToTarget(comp_graph),
            rect.shift, shift_vect
        )
        self.wait(2)
        self.play(
            FadeOut(new_subgraph),
            FadeOut(prev_neuron),
            FadeOut(prev_edge),
            comp_graph.restore,
            rect.shift, -shift_vect,
            rect.set_stroke, BLACK, 0
        )
        VGroup(prev_neuron, prev_edge).fade(1)
        self.remove(rect)
        self.wait()

        self.prev_comp_subgraph = new_subgraph

    def show_number_lines(self):
        comp_graph = self.comp_graph
        wL, aLm1, bL, zL, aL, C0 = [
            getattr(comp_graph, attr)
            for attr in ["wL", "aLm1", "bL", "zL", "aL", "C0"]
        ]
        wL.val = self.network.weights[-1][0][0]
        aL.val = self.decimals[0].number
        zL.val = sigmoid_inverse(aL.val)
        C0.val = (aL.val - 1)**2

        number_line = UnitInterval(
            unit_size = 2,
            stroke_width = 2,
            tick_size = 0.075,
            color = GREY_B,
        )

        for mob in wL, zL, aL, C0:
            mob.number_line = number_line.deepcopy()
            if mob is wL:
                mob.number_line.next_to(mob, UP, MED_LARGE_BUFF, LEFT)
            else:
                mob.number_line.next_to(mob, RIGHT)
            if mob is C0:
                mob.number_line.x_max = 0.5
                for tick_mark in mob.number_line.tick_marks[1::2]:
                    mob.number_line.tick_marks.remove(tick_mark)
            mob.dot = Dot(color = mob.get_color())
            mob.dot.move_to(
                mob.number_line.number_to_point(mob.val)
            )
            if mob is wL:
                path_arc = 0
                dot_spot = mob.dot.get_bottom()
            else:
                path_arc = -0.7*np.pi
                dot_spot = mob.dot.get_top()
            if mob is C0:
                mob_spot = mob[0].get_corner(UP+RIGHT)
                tip_length = 0.15
            else:
                mob_spot = mob.get_corner(UP+RIGHT)
                tip_length = 0.2
            mob.arrow = Arrow(
                mob_spot, dot_spot,
                path_arc = path_arc,
                tip_length = tip_length,
                buff = SMALL_BUFF,
            )
            mob.arrow.set_color(mob.get_color())
            mob.arrow.set_stroke(width = 5)

            self.play(ShowCreation(
                mob.number_line, 
                lag_ratio = 0.5
            ))
            self.play(
                ShowCreation(mob.arrow),
                ReplacementTransform(
                    mob.copy(), mob.dot,
                    path_arc = path_arc
                )
            )
        self.wait()

    def ask_about_w_sensitivity(self):
        wL, aLm1, bL, zL, aL, C0 = [
            getattr(self.comp_graph, attr)
            for attr in ["wL", "aLm1", "bL", "zL", "aL", "C0"]
        ]
        aLm1_val = self.last_neurons[1].get_fill_opacity()
        bL_val = self.network.biases[-1][0]

        get_wL_val = lambda : wL.number_line.point_to_number(
            wL.dot.get_center()
        )
        get_zL_val = lambda : get_wL_val()*aLm1_val+bL_val
        get_aL_val = lambda : sigmoid(get_zL_val())
        get_C0_val = lambda : (get_aL_val() - 1)**2

        def generate_dot_update(term, val_func):
            def update_dot(dot):
                dot.move_to(term.number_line.number_to_point(val_func()))
                return dot
            return update_dot

        dot_update_anims = [
            UpdateFromFunc(term.dot, generate_dot_update(term, val_func))
            for term, val_func in [
                (zL, get_zL_val),
                (aL, get_aL_val),
                (C0, get_C0_val),
            ]
        ]

        def shake_dot(run_time = 2, rate_func = there_and_back):
            self.play(
                ApplyMethod(
                    wL.dot.shift, LEFT, 
                    rate_func = rate_func, 
                    run_time = run_time
                ),
                *dot_update_anims
            )        

        wL_line = Line(wL.dot.get_center(), wL.dot.get_center()+LEFT)
        del_wL = OldTex("\\partial w^{(L)}")
        del_wL.scale(self.derivative_scale_val)
        del_wL.brace = Brace(wL_line, UP, buff = SMALL_BUFF)
        del_wL.set_color(wL.get_color())
        del_wL.next_to(del_wL.brace, UP, SMALL_BUFF)

        C0_line = Line(C0.dot.get_center(), C0.dot.get_center()+MED_SMALL_BUFF*RIGHT)
        del_C0 = OldTex("\\partial C_0")
        del_C0.scale(self.derivative_scale_val)
        del_C0.brace = Brace(C0_line, UP, buff = SMALL_BUFF)
        del_C0.set_color(C0.get_color())
        del_C0.next_to(del_C0.brace, UP, SMALL_BUFF)

        for sym in del_wL, del_C0:
            self.play(
                GrowFromCenter(sym.brace),
                Write(sym, run_time = 1)
            )
            shake_dot()
        self.wait()

        self.set_variables_as_attrs(
            shake_dot, del_wL, del_C0,
        )

    def show_derivative_wrt_w(self):
        del_wL = self.del_wL
        del_C0 = self.del_C0
        cost_word = self.cost_word
        cost_arrow = self.cost_arrow
        shake_dot = self.shake_dot
        wL = self.comp_graph.wL

        dC_dw = OldTex(
            "{\\partial C_0", "\\over", "\\partial w^{(L)} }"
        )
        dC_dw[0].set_color(del_C0.get_color())
        dC_dw[2].set_color(del_wL.get_color())
        dC_dw.scale(self.derivative_scale_val)
        dC_dw.to_edge(UP, buff = MED_SMALL_BUFF)
        dC_dw.shift(3.5*LEFT)

        full_rect = SurroundingRectangle(dC_dw)
        full_rect_copy = full_rect.copy()
        words = OldTexText("What we want")
        words.next_to(full_rect, RIGHT)
        words.set_color(YELLOW)

        denom_rect = SurroundingRectangle(dC_dw[2])
        numer_rect = SurroundingRectangle(dC_dw[0])

        self.play(
            ReplacementTransform(del_C0.copy(), dC_dw[0]),
            ReplacementTransform(del_wL.copy(), dC_dw[2]),
            Write(dC_dw[1], run_time = 1)
        )
        self.play(
            FadeOut(cost_word),
            FadeOut(cost_arrow),
            ShowCreation(full_rect),
            Write(words, run_time = 1),
        )
        self.wait(2)
        self.play(
            FadeOut(words),
            ReplacementTransform(full_rect, denom_rect)
        )
        self.play(Transform(dC_dw[2].copy(), del_wL, remover = True))
        shake_dot()
        self.play(ReplacementTransform(denom_rect, numer_rect))
        self.play(Transform(dC_dw[0].copy(), del_C0, remover = True))
        shake_dot()
        self.wait()
        self.play(ReplacementTransform(numer_rect, full_rect_copy))
        self.play(FadeOut(full_rect_copy))
        self.wait()

        self.dC_dw = dC_dw

    def show_chain_of_events(self):
        comp_graph = self.comp_graph
        wL, zL, aL, C0 = [
            getattr(comp_graph, attr)
            for attr in ["wL", "zL", "aL", "C0"]
        ]
        del_wL = self.del_wL
        del_C0 = self.del_C0

        zL_line = Line(ORIGIN, MED_LARGE_BUFF*LEFT)
        zL_line.shift(zL.dot.get_center())
        del_zL = OldTex("\\partial z^{(L)}")
        del_zL.set_color(zL.get_color())
        del_zL.brace = Brace(zL_line, DOWN, buff = SMALL_BUFF)

        aL_line = Line(ORIGIN, MED_SMALL_BUFF*LEFT)
        aL_line.shift(aL.dot.get_center())
        del_aL = OldTex("\\partial a^{(L)}")
        del_aL.set_color(aL.get_color())
        del_aL.brace = Brace(aL_line, DOWN, buff = SMALL_BUFF)

        for sym in del_zL, del_aL:
            sym.scale(self.derivative_scale_val)
            sym.brace.stretch_about_point(
                0.5, 1, sym.brace.get_top(),
            )
            sym.shift(
                sym.brace.get_bottom()+SMALL_BUFF*DOWN \
                -sym[0].get_corner(UP+RIGHT)
            )

        syms = [del_wL, del_zL, del_aL, del_C0]
        for s1, s2 in zip(syms, syms[1:]):
            self.play(
                ReplacementTransform(s1.copy(), s2),
                ReplacementTransform(s1.brace.copy(), s2.brace),
            )
            self.shake_dot(run_time = 1.5)
            self.wait(0.5)
        self.wait()

        self.set_variables_as_attrs(del_zL, del_aL)

    def show_chain_rule(self):
        dC_dw = self.dC_dw
        del_syms = [
            getattr(self, attr)
            for attr in ("del_wL", "del_zL", "del_aL", "del_C0")
        ]

        dz_dw = OldTex(
            "{\\partial z^{(L)}", "\\over", "\\partial w^{(L)}}"
        )
        da_dz = OldTex(
            "{\\partial a^{(L)}", "\\over", "\\partial z^{(L)}}"
        )
        dC_da = OldTex(
            "{\\partial C0}", "\\over", "\\partial a^{(L)}}"
        )
        dz_dw[2].set_color(self.del_wL.get_color())
        VGroup(dz_dw[0], da_dz[2]).set_color(self.z_color)
        dC_da[0].set_color(self.cost_color)
        equals = OldTex("=")
        group = VGroup(equals, dz_dw, da_dz, dC_da)
        group.arrange(RIGHT, SMALL_BUFF)
        group.scale(self.derivative_scale_val)
        group.next_to(dC_dw, RIGHT)
        for mob in group[1:]:
            target_y = equals.get_center()[1]
            y = mob[1].get_center()[1]
            mob.shift((target_y - y)*UP)

        self.play(Write(equals, run_time = 1))
        for frac, top_sym, bot_sym in zip(group[1:], del_syms[1:], del_syms):
            self.play(Indicate(top_sym, rate_func = wiggle))
            self.play(
                ReplacementTransform(top_sym.copy(), frac[0]),
                FadeIn(frac[1]),
            )
            self.play(Indicate(bot_sym, rate_func = wiggle))
            self.play(ReplacementTransform(
                bot_sym.copy(), frac[2]
            ))
            self.wait()
        self.shake_dot()
        self.wait()

        self.chain_rule_equation = VGroup(dC_dw, *group)

    def name_chain_rule(self):
        graph_parts = self.get_all_comp_graph_parts()
        equation = self.chain_rule_equation
        rect = SurroundingRectangle(equation)
        group = VGroup(equation, rect)
        group.generate_target()
        group.target.to_corner(UP+LEFT)
        words = OldTexText("Chain rule")
        words.set_color(YELLOW)
        words.next_to(group.target, DOWN)

        self.play(ShowCreation(rect))
        self.play(
            MoveToTarget(group),
            Write(words, run_time = 1),
            graph_parts.scale, 0.7, graph_parts.get_bottom()
        )
        self.wait(2)
        self.play(*list(map(FadeOut, [rect, words])))

    def indicate_everything_on_screen(self):
        everything = VGroup(*self.get_top_level_mobjects())
        everything = VGroup(*[m for m in everything.family_members_with_points() if not m.is_subpath])
        self.play(LaggedStartMap(
            Indicate, everything,
            rate_func = wiggle,
            lag_ratio = 0.2,
            run_time = 5
        ))
        self.wait()

    def prepare_for_derivatives(self):
        zL_formula = self.zL_formula
        aL_formula = self.aL_formula
        az_formulas = VGroup(zL_formula, aL_formula)
        cost_equation = self.cost_equation
        desired_output_words = self.desired_output_words

        az_formulas.generate_target()
        az_formulas.target.to_edge(RIGHT)

        index = 4
        cost_eq = cost_equation[index]
        z_eq = az_formulas.target[0][1]
        x_shift = (z_eq.get_center() - cost_eq.get_center())[0]*RIGHT
        cost_equation.generate_target()
        Transform(
            VGroup(*cost_equation.target[1:index]),
            VectorizedPoint(cost_eq.get_left())
        ).update(1)
        cost_equation.target[0].next_to(cost_eq, LEFT, SMALL_BUFF)
        cost_equation.target.shift(x_shift)

        self.play(
            FadeOut(self.all_comp_graph_parts),
            FadeOut(self.desired_output_words),
            MoveToTarget(az_formulas),
            MoveToTarget(cost_equation)
        )

    def compute_derivatives(self):
        cost_equation = self.cost_equation
        zL_formula = self.zL_formula
        aL_formula = self.aL_formula
        chain_rule_equation = self.chain_rule_equation.copy()
        dC_dw, equals, dz_dw, da_dz, dC_da = chain_rule_equation

        derivs = VGroup(dC_da, da_dz, dz_dw)
        deriv_targets = VGroup()
        for deriv in derivs:
            deriv.generate_target()
            deriv_targets.add(deriv.target)
        deriv_targets.arrange(DOWN, buff = MED_LARGE_BUFF)
        deriv_targets.next_to(dC_dw, DOWN, LARGE_BUFF)
        for deriv in derivs:
            deriv.equals = OldTex("=")
            deriv.equals.next_to(deriv.target, RIGHT)


        #dC_da
        self.play(
            MoveToTarget(dC_da),
            Write(dC_da.equals)
        )
        index = 4
        cost_rhs = VGroup(*cost_equation[index+1:])       
        dC_da.rhs = cost_rhs.copy()
        two = dC_da.rhs[-1]
        two.scale(1.5)
        two.next_to(dC_da.rhs[0], LEFT, SMALL_BUFF)
        dC_da.rhs.next_to(dC_da.equals, RIGHT)
        dC_da.rhs.shift(0.7*SMALL_BUFF*UP)
        cost_equation.save_state()

        self.play(
            cost_equation.next_to, dC_da.rhs,
            DOWN, MED_LARGE_BUFF, LEFT
        )
        self.wait()
        self.play(ReplacementTransform(
            cost_rhs.copy(), dC_da.rhs,
            path_arc = np.pi/2,
        ))
        self.wait()
        self.play(cost_equation.restore)
        self.wait()

        #show_difference
        neuron = self.last_neurons[0]
        decimal = self.decimals[0]
        double_arrow = DoubleArrow(
            neuron.get_right(),
            self.desired_output_neuron.get_left(),
            buff = SMALL_BUFF,
            color = RED
        )

        moving_decimals = VGroup(
            self.decimals[0].copy(),
            self.desired_output_decimal.copy()
        )
        minus = OldTex("-")
        minus.move_to(moving_decimals)
        minus.scale(0.7)
        minus.set_fill(opacity = 0)
        moving_decimals.submobjects.insert(1, minus)
        moving_decimals.generate_target(use_deepcopy = True)
        moving_decimals.target.arrange(RIGHT, buff = SMALL_BUFF)
        moving_decimals.target.scale(1.5)
        moving_decimals.target.next_to(
            dC_da.rhs, DOWN, 
            buff = MED_LARGE_BUFF,
            aligned_edge = RIGHT,
        )
        moving_decimals.target.set_fill(WHITE, 1)

        self.play(ReplacementTransform(
            dC_da.rhs.copy(), double_arrow
        ))
        self.wait()
        self.play(MoveToTarget(moving_decimals))
        opacity = neuron.get_fill_opacity()
        for target_o in 0, opacity:
            self.wait(2)
            self.play(
                neuron.set_fill, None, target_o,
                *[
                    ChangingDecimal(d, lambda a : neuron.get_fill_opacity())
                    for d in (decimal, moving_decimals[0])
                ]
            )
        self.play(*list(map(FadeOut, [double_arrow, moving_decimals])))

        #da_dz
        self.play(
            MoveToTarget(da_dz),
            Write(da_dz.equals)
        )
        a_rhs = VGroup(*aL_formula[2:])
        da_dz.rhs = a_rhs.copy()
        prime = OldTex("'")
        prime.move_to(da_dz.rhs[0].get_corner(UP+RIGHT))
        da_dz.rhs[0].shift(0.5*SMALL_BUFF*LEFT)
        da_dz.rhs.add_to_back(prime)
        da_dz.rhs.next_to(da_dz.equals, RIGHT)
        da_dz.rhs.shift(0.5*SMALL_BUFF*UP)
        aL_formula.save_state()
        self.play(
            aL_formula.next_to, da_dz.rhs,
            DOWN, MED_LARGE_BUFF, LEFT
        )
        self.wait()
        self.play(ReplacementTransform(
            a_rhs.copy(), da_dz.rhs,
        ))
        self.wait()
        self.play(aL_formula.restore)
        self.wait()

        #dz_dw
        self.play(
            MoveToTarget(dz_dw),
            Write(dz_dw.equals)
        )
        z_rhs = VGroup(*zL_formula[2:])
        dz_dw.rhs = z_rhs[1].copy()
        dz_dw.rhs.next_to(dz_dw.equals, RIGHT)
        dz_dw.rhs.shift(SMALL_BUFF*UP)
        zL_formula.save_state()
        self.play(
            zL_formula.next_to, dz_dw.rhs,
                DOWN, MED_LARGE_BUFF, LEFT,
        )
        self.wait()
        rect = SurroundingRectangle(VGroup(*zL_formula[2:4]))
        self.play(ShowCreation(rect))
        self.play(FadeOut(rect))
        self.play(ReplacementTransform(
            z_rhs[1].copy(), dz_dw.rhs,
        ))
        self.wait()
        self.play(zL_formula.restore)
        self.wait()

        self.derivative_equations = VGroup(dC_da, da_dz, dz_dw)

    def get_lost_in_formulas(self):
        randy = Randolph()
        randy.flip()
        randy.scale(0.7)
        randy.to_edge(DOWN)
        randy.shift(LEFT)

        self.play(FadeIn(randy))
        self.play(randy.change, "pleading", self.chain_rule_equation)
        self.play(Blink(randy))
        self.play(randy.change, "maybe")
        self.play(Blink(randy))
        self.play(FadeOut(randy))

    def fire_together_wire_together(self):
        dz_dw = self.derivative_equations[2]
        rhs = dz_dw.rhs
        rhs_copy = rhs.copy()
        del_wL = dz_dw[2].copy()
        rect = SurroundingRectangle(VGroup(dz_dw, dz_dw.rhs))
        edge = self.network_mob.edge_groups[-1][0]
        edge.save_state()
        neuron = self.last_neurons[1]
        decimal = self.decimals[1]

        def get_decimal_anims():
            return [
                ChangingDecimal(decimal, lambda a : neuron.get_fill_opacity()),
                UpdateFromFunc(
                    decimal, lambda m : m.set_color(
                        WHITE if neuron.get_fill_opacity() < 0.8 \
                        else BLACK
                    )
                )
            ]

        self.play(ShowCreation(rect))
        self.play(FadeOut(rect))
        self.play(
            del_wL.next_to, edge, UP, SMALL_BUFF
        )
        self.play(
            edge.set_stroke, None, 10,
            rate_func = wiggle,
            run_time = 3,
        )
        self.wait()
        self.play(rhs.shift, MED_LARGE_BUFF*UP, rate_func = wiggle)
        self.play(
            rhs_copy.move_to, neuron,
            rhs_copy.set_fill, None, 0
        )
        self.remove(rhs_copy)
        self.play(
            neuron.set_fill, None, 0,
            *get_decimal_anims(),
            run_time = 3,
            rate_func = there_and_back
        )
        self.wait()

        #Fire together wire together
        opacity = neuron.get_fill_opacity()
        self.play(
            neuron.set_fill, None, 0.99, 
            *get_decimal_anims()
        )
        self.play(edge.set_stroke, None, 8)
        self.play(
            neuron.set_fill, None, opacity, 
            *get_decimal_anims()
        )
        self.play(edge.restore, FadeOut(del_wL))
        self.wait(3)

    def organize_chain_rule_rhs(self):
        fracs = self.derivative_equations
        equals_group = VGroup(*[frac.equals for frac in fracs])
        rhs_group = VGroup(*[frac.rhs for frac in reversed(fracs)])

        chain_rule_equation = self.chain_rule_equation
        equals = OldTex("=")
        equals.next_to(chain_rule_equation, RIGHT)

        rhs_group.generate_target()
        rhs_group.target.arrange(RIGHT, buff = SMALL_BUFF)
        rhs_group.target.next_to(equals, RIGHT)
        rhs_group.target.shift(SMALL_BUFF*UP)

        right_group = VGroup(
            self.cost_equation, self.zL_formula, self.aL_formula,
            self.network_mob, self.decimals,
            self.a_labels, self.a_label_arrows,
            self.y_label, self.y_label_arrow,
            self.desired_output_neuron,
            self.desired_output_rect,
            self.desired_output_decimal,
        )

        self.play(
            MoveToTarget(rhs_group, path_arc = np.pi/2),
            Write(equals),
            FadeOut(fracs),
            FadeOut(equals_group),
            right_group.to_corner, DOWN+RIGHT
        )
        self.wait()

        rhs_group.add(equals)
        self.chain_rule_rhs = rhs_group

    def show_average_derivative(self):
        dC0_dw = self.chain_rule_equation[0]
        full_derivative = OldTex(
            "{\\partial C", "\\over", "\\partial w^{(L)}}",
            "=", "\\frac{1}{n}", "\\sum_{k=0}^{n-1}",
            "{\\partial C_k", "\\over", "\\partial w^{(L)}}"
        )
        full_derivative.set_color_by_tex_to_color_map({
            "partial C" : self.cost_color,
            "partial w" : self.del_wL.get_color()
        })
        full_derivative.to_edge(LEFT)

        dCk_dw = VGroup(*full_derivative[-3:])
        lhs = VGroup(*full_derivative[:3])
        rhs = VGroup(*full_derivative[4:])
        lhs_brace = Brace(lhs, DOWN)
        lhs_text = lhs_brace.get_text("Derivative of \\\\ full cost function")
        rhs_brace = Brace(rhs, UP)
        rhs_text = rhs_brace.get_text("Average of all \\\\ training examples")
        VGroup(
            full_derivative, lhs_brace, lhs_text, rhs_brace, rhs_text
        ).to_corner(DOWN+LEFT)

        mover = dC0_dw.copy()
        self.play(Transform(mover, dCk_dw))
        self.play(Write(full_derivative, run_time = 2))
        self.remove(mover)
        for brace, text in (rhs_brace, rhs_text), (lhs_brace, lhs_text):
            self.play(
                GrowFromCenter(brace),
                Write(text, run_time = 2),
            )
            self.wait(2)
        self.cycle_through_altnernate_training_examples()
        self.play(*list(map(FadeOut, [
            VGroup(*full_derivative[3:]), 
            lhs_brace, lhs_text,
            rhs_brace, rhs_text,
        ])))

        self.dC_dw = lhs

    def cycle_through_altnernate_training_examples(self):
        neurons = VGroup(
            self.desired_output_neuron, *self.last_neurons
        )
        decimals = VGroup(
            self.desired_output_decimal, *self.decimals
        )
        group = VGroup(neurons, decimals)
        group.save_state()

        for x in range(20):
            for n, d in zip(neurons, decimals):
                o = np.random.random()
                if n is self.desired_output_neuron:
                    o = np.round(o)
                n.set_fill(opacity = o)
                Transform(
                    d, self.get_neuron_activation_decimal(n)
                ).update(1)
            self.wait(0.2)
        self.play(group.restore, run_time = 0.2)

    def show_gradient(self):
        dC_dw = self.dC_dw
        dC_dw.generate_target()
        terms = VGroup(
            OldTex("{\\partial C", "\\over", "\\partial w^{(1)}"),
            OldTex("{\\partial C", "\\over", "\\partial b^{(1)}"),
            OldTex("\\vdots"),
            dC_dw.target,
            OldTex("{\\partial C", "\\over", "\\partial b^{(L)}"),
        )
        for term in terms:
            # CHANGE: The formulas are OldTex (Cairo TexMobject) here: accept both classes.
            if isinstance(term, (Tex, OldTex)):
                term.set_color_by_tex_to_color_map({
                    "partial C" : RED,
                    "partial w" : BLUE,
                    "partial b" : MAROON_B,
                })
        terms.arrange(DOWN, buff = MED_LARGE_BUFF)
        lb, rb = brackets = OldTex("[]")
        brackets.scale(3)
        brackets.stretch_to_fit_height(1.1*terms.get_height())
        lb.next_to(terms, LEFT, buff = SMALL_BUFF)
        rb.next_to(terms, RIGHT, buff = SMALL_BUFF)
        vect = VGroup(lb, terms, rb)
        vect.set_height(5)
        lhs = OldTex("\\nabla C", "=")
        lhs[0].set_color(RED)
        lhs.next_to(vect, LEFT)
        VGroup(lhs, vect).to_corner(DOWN+LEFT, buff = LARGE_BUFF)
        terms.remove(dC_dw.target)

        self.play(
            MoveToTarget(dC_dw),
            Write(vect, run_time = 1)
        )
        terms.add(dC_dw)
        self.play(Write(lhs))
        self.wait(2)
        self.play(FadeOut(VGroup(lhs, vect)))

    def transition_to_derivative_wrt_b(self):
        all_comp_graph_parts = self.all_comp_graph_parts
        all_comp_graph_parts.scale(
            1.3, about_point = all_comp_graph_parts.get_bottom()
        )
        comp_graph = self.comp_graph
        wL, bL, zL, aL, C0 = [
            getattr(comp_graph, attr)
            for attr in ["wL", "bL", "zL", "aL", "C0"]
        ]
        path_to_C = VGroup(wL, zL, aL, C0)

        top_expression = VGroup(
            self.chain_rule_equation,
            self.chain_rule_rhs
        )
        rect = SurroundingRectangle(top_expression)

        self.play(ShowCreation(rect))
        self.play(FadeIn(comp_graph), FadeOut(rect))
        for x in range(2):
            self.play(LaggedStartMap(
                Indicate, path_to_C, 
                rate_func = there_and_back,
                run_time = 1.5,
                lag_ratio = 0.7,
            ))
        self.wait()

    def show_derivative_wrt_b(self):
        comp_graph = self.comp_graph
        dC0_dw = self.chain_rule_equation[0]
        dz_dw = self.chain_rule_equation[2]
        aLm1 = self.chain_rule_rhs[0]
        left_term_group = VGroup(dz_dw, aLm1)
        dz_dw_rect = SurroundingRectangle(dz_dw)

        del_w = dC0_dw[2]
        del_b = OldTex("\\partial b^{(L)}")
        del_b.set_color(MAROON_B)
        del_b.replace(del_w)

        dz_db = OldTex(
            "{\\partial z^{(L)}", "\\over", "\\partial b^{(L)}}"
        )
        dz_db.set_color_by_tex_to_color_map({
            "partial z" : self.z_color,
            "partial b" : MAROON_B
        })
        dz_db.replace(dz_dw)

        one = OldTex("1")
        one.move_to(aLm1, RIGHT)
        arrow = Arrow(
            dz_db.get_bottom(),
            one.get_bottom(),
            path_arc = np.pi/2,
            color = WHITE,
        )
        arrow.set_stroke(width = 2)

        wL, bL, zL, aL, C0 = [
            getattr(comp_graph, attr)
            for attr in ["wL", "bL", "zL", "aL", "C0"]
        ]
        path_to_C = VGroup(bL, zL, aL, C0)
        def get_path_animation():
            return LaggedStartMap(
                Indicate, path_to_C, 
                rate_func = there_and_back,
                run_time = 1.5,
                lag_ratio = 0.7,
            )

        zL_formula = self.zL_formula
        b_in_z_formula = zL_formula[-1]
        z_formula_rect = SurroundingRectangle(zL_formula)
        b_in_z_rect = SurroundingRectangle(b_in_z_formula)

        self.play(get_path_animation())
        self.play(ShowCreation(dz_dw_rect))
        self.play(FadeOut(dz_dw_rect))
        self.play(
            left_term_group.shift, DOWN,
            left_term_group.fade, 1,
        )
        self.remove(left_term_group)
        self.chain_rule_equation.remove(dz_dw)
        self.chain_rule_rhs.remove(aLm1)
        self.play(Transform(del_w, del_b))
        self.play(FadeIn(dz_db))
        self.play(get_path_animation())
        self.wait()
        self.play(ShowCreation(z_formula_rect))
        self.wait()
        self.play(ReplacementTransform(z_formula_rect, b_in_z_rect))
        self.wait()
        self.play(
            ReplacementTransform(b_in_z_formula.copy(), one),
            FadeOut(b_in_z_rect)
        )
        self.play(
            ShowCreation(arrow),
            ReplacementTransform(
                dz_db.copy(), one,
                path_arc = arrow.path_arc
            )
        )
        self.wait(2)
        self.play(*list(map(FadeOut, [dz_db, arrow, one])))

        self.dz_db = dz_db

    def show_derivative_wrt_a(self):
        denom = self.chain_rule_equation[0][2]
        numer = VGroup(*self.chain_rule_equation[0][:2])
        del_aLm1 = OldTex("\\partial a^{(L-1)}")
        del_aLm1.scale(0.8)
        del_aLm1.move_to(denom)
        dz_daLm1 = OldTex(
            "{\\partial z^{(L)}", "\\over", "\\partial a^{(L-1)}}"
        )
        dz_daLm1.scale(0.8)
        dz_daLm1.next_to(self.chain_rule_equation[1], RIGHT, SMALL_BUFF)
        dz_daLm1.shift(0.7*SMALL_BUFF*UP)
        dz_daLm1[0].set_color(self.z_color)
        dz_daLm1_rect = SurroundingRectangle(dz_daLm1)
        wL = self.zL_formula[2].copy()
        wL.next_to(self.chain_rule_rhs[0], LEFT, SMALL_BUFF)

        arrow = Arrow(
            dz_daLm1.get_bottom(), wL.get_bottom(),
            path_arc = np.pi/2,
            color = WHITE,
        )

        comp_graph = self.comp_graph
        path_to_C = VGroup(*[
            getattr(comp_graph, attr)
            for attr in ["aLm1", "zL", "aL", "C0"]
        ])
        def get_path_animation():
            return LaggedStartMap(
                Indicate, path_to_C, 
                rate_func = there_and_back,
                run_time = 1.5,
                lag_ratio = 0.7,
            )

        zL_formula = self.zL_formula
        z_formula_rect = SurroundingRectangle(zL_formula)
        a_in_z_rect = SurroundingRectangle(VGroup(*zL_formula[2:4]))
        wL_in_z = zL_formula[2]

        for x in range(3):
            self.play(get_path_animation())
        self.play(
            numer.shift, SMALL_BUFF*UP,
            Transform(denom, del_aLm1)
        )
        self.play(
            FadeIn(dz_daLm1),
            VGroup(*self.chain_rule_equation[-2:]).shift, SMALL_BUFF*RIGHT,
        )
        self.wait()
        self.play(ShowCreation(dz_daLm1_rect))
        self.wait()
        self.play(ReplacementTransform(
            dz_daLm1_rect, z_formula_rect
        ))
        self.wait()
        self.play(ReplacementTransform(z_formula_rect, a_in_z_rect))
        self.play(
            ReplacementTransform(wL_in_z.copy(), wL),
            FadeOut(a_in_z_rect)
        )
        self.play(
            ShowCreation(arrow),
            ReplacementTransform(
                dz_daLm1.copy(), wL,
                path_arc = arrow.path_arc
            )
        )
        self.wait(2)

        self.chain_rule_rhs.add(wL, arrow)
        self.chain_rule_equation.add(dz_daLm1)

    def show_previous_weight_and_bias(self):
        to_fade = self.chain_rule_rhs
        comp_graph = self.comp_graph
        prev_comp_subgraph = self.prev_comp_subgraph
        prev_comp_subgraph.scale(0.8)
        prev_comp_subgraph.next_to(comp_graph, UP, SMALL_BUFF)

        prev_layer = VGroup(
            self.network_mob.layers[1],
            self.network_mob.edge_groups[1],
        )
        for mob in prev_layer:
            mob.restore()
        prev_layer.next_to(self.last_neurons, LEFT, buff = 0)
        self.remove(prev_layer)

        self.play(LaggedStartMap(FadeOut, to_fade, run_time = 1))
        self.play(
            ShowCreation(prev_comp_subgraph, run_time = 1),
            self.chain_rule_equation.to_edge, RIGHT
        )
        self.play(FadeIn(prev_layer))

        ###
        neuron = self.network_mob.layers[1].neurons[0]
        decimal = self.get_neuron_activation_decimal(neuron)
        a_label = OldTex("a^{(L-2)}")
        a_label.replace(self.a_labels[1])
        arrow = self.a_label_arrows[1].copy()
        VGroup(a_label, arrow).shift(
            neuron.get_center() - self.last_neurons[1].get_center()
        )

        self.play(
            Write(a_label, run_time = 1),
            Write(decimal, run_time = 1),
            GrowArrow(arrow),
        )        

    def animate_long_path(self):
        comp_graph = self.comp_graph
        path_to_C = VGroup(
            self.wLm1, self.zLm1,
            *[
                getattr(comp_graph, attr)
                for attr in ["aLm1", "zL", "aL", "C0"]
            ]
        )
        for x in range(2):
            self.play(LaggedStartMap(
                Indicate, path_to_C, 
                rate_func = there_and_back,
                run_time = 1.5,
                lag_ratio = 0.4,
            ))
        self.wait(2)

    ###

    def get_neuron_activation_decimal(self, neuron):
        opacity = neuron.get_fill_opacity()
        decimal = DecimalNumber(opacity, num_decimal_places = 2)
        decimal.set_width(0.85*neuron.get_width())
        if decimal.number > 0.8:
            decimal.set_fill(BLACK)
        decimal.move_to(neuron)
        return decimal

    def get_all_comp_graph_parts(self):
        comp_graph = self.comp_graph
        result = VGroup(comp_graph)
        for attr in "wL", "zL", "aL", "C0":
            sym = getattr(comp_graph, attr)
            result.add(
                sym.arrow, sym.number_line, sym.dot
            )
            del_sym = getattr(self, "del_" + attr)
            result.add(del_sym, del_sym.brace)

        self.all_comp_graph_parts = result
        return result
