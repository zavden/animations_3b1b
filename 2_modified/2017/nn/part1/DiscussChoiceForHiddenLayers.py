# ==============================================================================
# Scene:      DiscussChoiceForHiddenLayers
# Source:     videos/_2017/nn/part1.py (lines 1337-1398)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DiscussChoiceForHiddenLayers.py DiscussChoiceForHiddenLayers -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Provide package `nn` (network.py with binary-mode pickle fix, mnist_loader.py reading a small synthetic MNIST stand-in) through data_files, since the original mnist.pkl.gz is not in the repo.
#   - Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
#   - Python 2 integer division used as an index/count -> //.
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2017/nn/nn_pkg/mnist_mini.npz (synthetic MNIST stand-in, built from the 100 real digits of image_map by make_nn_support.py)
# ==============================================================================

import sys
import os.path
from manim_imports_ext import *
import warnings
# CHANGE: Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
import sys, os.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # CL17-B
from nn.network import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


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


class MNistNetworkMobject(NetworkMobject):
    CONFIG = {
        "neuron_to_neuron_buff" : SMALL_BUFF,
        "layer_to_layer_buff" : 1.5,
        "edge_stroke_width" : 1,
        "include_output_labels" : True,
    }

    def __init__(self, **kwargs):
        network = get_pretrained_network()
        NetworkMobject.__init__(self, network, **kwargs)


class DiscussChoiceForHiddenLayers(TeacherStudentsScene):
    def construct(self):
        network_mob = MNistNetworkMobject(
            layer_to_layer_buff = 2.5,
            neuron_stroke_color = WHITE,
        )
        network_mob.set_height(4)
        network_mob.to_edge(UP, buff = LARGE_BUFF)
        layers = VGroup(*network_mob.layers[1:3])
        rects = VGroup(*list(map(SurroundingRectangle, layers)))
        self.add(network_mob)

        two_words = OldTexText("2 hidden layers")
        two_words.set_color(YELLOW)
        sixteen_words = OldTexText("16 neurons each")
        sixteen_words.set_color(MAROON_B)
        for words in two_words, sixteen_words:
            words.next_to(rects, UP)

        neurons_anim = LaggedStartMap(
            Indicate, 
            VGroup(*it.chain(*[layer.neurons for layer in layers])),
            rate_func = there_and_back,
            scale_factor = 2,
            color = MAROON_B,
        )

        self.play(
            ShowCreation(rects),
            Write(two_words, run_time = 1),
            self.teacher.change, "raise_right_hand",
        )
        self.wait()
        self.play(
            FadeOut(rects),
            ReplacementTransform(two_words, sixteen_words),
            neurons_anim
        )
        self.wait()
        self.play(self.teacher.change, "shruggie")
        self.play_student_changes("erm", "confused", "sassy")
        self.wait()
        self.student_says(
            "Why 2 \\\\ layers?",
            index = 1,
            bubble_config = {"direction" : RIGHT},
            run_time = 1,
            target_mode = "raise_left_hand",
        )
        self.play(self.teacher.change, "happy")
        self.wait()
        self.student_says(
            "Why 16?",
            index = 0,
            run_time = 1,
        )
        self.play(neurons_anim, run_time = 3)
        self.play(
            self.teacher.change, "shruggie",
            RemovePiCreatureBubble(self.students[0]),
        )
        self.wait()
