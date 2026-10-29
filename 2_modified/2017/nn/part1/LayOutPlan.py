# ==============================================================================
# Scene:      LayOutPlan
# Source:     videos/_2017/nn/part1.py (lines 619-782)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl LayOutPlan.py LayOutPlan -w -m --fps 15
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


class LayOutPlan(TeacherStudentsScene, NetworkScene):
    def setup(self):
        TeacherStudentsScene.setup(self)
        NetworkScene.setup(self)
        self.remove(self.network_mob)

    def construct(self):
        self.force_skipping()

        self.show_words()
        self.show_network()
        self.show_math()
        self.ask_about_layers()
        self.show_learning()
        self.show_videos()

    def show_words(self):
        words = VGroup(
            OldTexText("Machine", "learning").set_color(GREEN),
            OldTexText("Neural network").set_color(BLUE),
        )
        words.next_to(self.teacher.get_corner(UP+LEFT), UP)
        words[0].save_state()
        words[0].shift(DOWN)
        words[0].fade(1)

        self.play(
            words[0].restore,
            self.teacher.change, "raise_right_hand",
            self.change_students("pondering", "erm", "sassy")
        )
        self.play(
            words[0].shift, MED_LARGE_BUFF*UP,
            FadeIn(words[1]),
        )
        self.play_student_changes(
            *["pondering"]*3,
            look_at = words
        )
        self.play(words.to_corner, UP+RIGHT)

        self.words = words

    def show_network(self):
        network_mob = self.network_mob
        network_mob.next_to(self.students, UP)

        self.play(
            ReplacementTransform(
                VGroup(self.words[1].copy()),
                network_mob.layers
            ),
            self.change_students(
                *["confused"]*3,
                lag_ratio = 0
            ),
            self.teacher.change, "plain",
            run_time = 1
        )
        self.play(ShowCreation(
            network_mob.edge_groups,
            lag_ratio = 0.5,
            run_time = 2,
            rate_func=linear,
        ))
        in_vect = np.random.random(self.network.sizes[0])
        self.feed_forward(in_vect)

    def show_math(self):
        equation = OldTex(
            "\\textbf{a}_{l+1}", "=",  
            "\\sigma(",
                "W_l", "\\textbf{a}_l", "+", "b_l",
            ")"
        )
        equation.set_color_by_tex_to_color_map({
            "\\textbf{a}" : GREEN,
        })
        equation.move_to(self.network_mob.get_corner(UP+RIGHT))
        equation.to_edge(UP)

        self.play(Write(equation, run_time = 2))
        self.wait()

        self.equation = equation

    def ask_about_layers(self):
        self.student_says(
            "Why the layers?",
            index = 2,
            bubble_config = {"direction" : LEFT}
        )
        self.wait()
        self.play(RemovePiCreatureBubble(self.students[2]))

    def show_learning(self):
        word = self.words[0][1].copy()
        rect = SurroundingRectangle(word, color = YELLOW)
        self.network_mob.neuron_fill_color = YELLOW

        layer = self.network_mob.layers[-1]
        activation = np.zeros(len(layer.neurons))
        activation[1] = 1.0
        active_layer = self.network_mob.get_active_layer(
            -1, activation
        )
        word_group = VGroup(word, rect)
        word_group.generate_target()
        word_group.target.move_to(self.equation, LEFT)
        word_group.target[0].set_color(YELLOW)
        word_group.target[1].set_stroke(width = 0)

        self.play(ShowCreation(rect))
        self.play(
            Transform(layer, active_layer),
            FadeOut(self.equation),
            MoveToTarget(word_group),
        )
        for edge_group in reversed(self.network_mob.edge_groups):
            edge_group.generate_target()
            for edge in edge_group.target:
                edge.set_stroke(
                    YELLOW, 
                    width = 4*np.random.random()**2
                )
            self.play(MoveToTarget(edge_group))
        self.wait()

        self.learning_word = word

    def show_videos(self):
        network_mob = self.network_mob
        learning = self.learning_word
        structure = OldTexText("Structure")
        structure.set_color(YELLOW)
        videos = VGroup(*[
            VideoIcon().set_fill(RED)
            for x in range(2)
        ])
        videos.set_height(1.5)
        videos.arrange(RIGHT, buff = LARGE_BUFF)
        videos.next_to(self.students, UP, LARGE_BUFF)

        network_mob.generate_target()
        network_mob.target.set_height(0.8*videos[0].get_height())
        network_mob.target.move_to(videos[0])
        learning.generate_target()
        learning.target.next_to(videos[1], UP)
        structure.next_to(videos[0], UP)
        structure.shift(0.5*SMALL_BUFF*UP)

        self.revert_to_original_skipping_status()
        self.play(
            MoveToTarget(network_mob),
            MoveToTarget(learning)
        )
        self.play(
            DrawBorderThenFill(videos[0]),
            FadeIn(structure),
            self.change_students(*["pondering"]*3)
        )
        self.wait()
        self.play(DrawBorderThenFill(videos[1]))
        self.wait()
