# ==============================================================================
# Scene:      IntroduceWeightMatrix
# Source:     videos/_2017/nn/part1.py (lines 3334-3887)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroduceWeightMatrix.py IntroduceWeightMatrix -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Provide package `nn` (network.py with binary-mode pickle fix, mnist_loader.py reading a small synthetic MNIST stand-in) through data_files, since the original mnist.pkl.gz is not in the repo.
#   - Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
#   - Python 2 integer division used as an index/count -> //.
#   - Cairo mobject slices were lists; GL returns a group, so convert before concatenating with lists.
#   - `map(Tex, ...)` used the NEW GL Tex class; the Cairo code meant TexMobject -> OldTex.
#   - Cairo's `Transform(group, dots).update(1)` left every member of the group as a copy of dots in place; GL's left some members behind (column got 5.8 units wide and the matrix brackets huge). Do it explicitly with become().
#   - Same: explicit become() instead of Transform(...).update(1).
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


class IntroduceWeightMatrix(NetworkScene):
    CONFIG = {
        "network_mob_config" : {
            "neuron_stroke_color" : WHITE,
            "neuron_fill_color" : WHITE,
            "neuron_radius" : 0.35,
            "layer_to_layer_buff" : 2,
        },
        "layer_sizes" : [8, 6],
    }
    def construct(self):
        self.setup_network_mob()
        self.show_weighted_sum()
        self.organize_activations_into_column()
        self.organize_weights_as_matrix()
        self.show_meaning_of_matrix_row()
        self.connect_weighted_sum_to_matrix_multiplication()
        self.add_bias_vector()
        self.apply_sigmoid()
        self.write_clean_final_expression()

    def setup_network_mob(self):
        self.network_mob.to_edge(LEFT, buff = LARGE_BUFF)
        self.network_mob.layers[1].neurons.shift(0.02*RIGHT)

    def show_weighted_sum(self):
        self.fade_many_neurons()
        self.activate_first_layer()
        self.show_first_neuron_weighted_sum()
        self.add_bias()
        self.add_sigmoid()
    ##

    def fade_many_neurons(self):
        anims = []
        neurons = self.network_mob.layers[1].neurons
        for neuron in neurons[1:]:
            neuron.save_state()
            neuron.edges_in.save_state()
            anims += [
                neuron.fade, 0.8,
                neuron.set_fill, None, 0,
                neuron.edges_in.fade, 0.8,
            ]
        anims += [
            Animation(neurons[0]),
            Animation(neurons[0].edges_in),
        ]
        self.play(*anims)

    def activate_first_layer(self):
        layer = self.network_mob.layers[0]
        activations = 0.7*np.random.random(len(layer.neurons))
        active_layer = self.network_mob.get_active_layer(0, activations)
        a_labels = VGroup(*[
            OldTex("a^{(0)}_%d"%d)
            for d in range(len(layer.neurons))
        ])
        for label, neuron in zip(a_labels, layer.neurons):
            label.scale(0.75)
            label.move_to(neuron)

        self.play(
            Transform(layer, active_layer),
            Write(a_labels, run_time = 2)
        )

        self.a_labels = a_labels

    def show_first_neuron_weighted_sum(self):
        neuron = self.network_mob.layers[1].neurons[0]
        a_labels = VGroup(*self.a_labels[:2]).copy()
        a_labels.generate_target()
        w_labels = VGroup(*[
            OldTex("w_{0, %d}"%d)
            for d in range(len(a_labels))
        ])
        weighted_sum = VGroup()
        symbols = VGroup()
        for a_label, w_label in zip(a_labels.target, w_labels):
            a_label.scale(1./0.75)
            plus =  OldTex("+")
            weighted_sum.add(w_label, a_label, plus)
            symbols.add(plus)
        weighted_sum.add(
            OldTex("\\cdots"),
            OldTex("+"),
            OldTex("w_{0, n}"),
            OldTex("a^{(0)}_n"),
        )

        weighted_sum.arrange(RIGHT)
        a1_label = OldTex("a^{(1)}_0")
        a1_label.next_to(neuron, RIGHT)
        equals = OldTex("=").next_to(a1_label, RIGHT)
        weighted_sum.next_to(equals, RIGHT)

        symbols.add(*weighted_sum[-4:-2])
        w_labels.add(weighted_sum[-2])
        a_labels.add(self.a_labels[-1].copy())
        a_labels.target.add(weighted_sum[-1])
        a_labels.add(VGroup(*self.a_labels[2:-1]).copy())
        a_labels.target.add(VectorizedPoint(weighted_sum[-4].get_center()))

        VGroup(a1_label, equals, weighted_sum).scale(
            0.75, about_point = a1_label.get_left()
        )

        w_labels.set_color(GREEN)
        w_labels.shift(0.6*SMALL_BUFF*DOWN)
        a_labels.target.shift(0.5*SMALL_BUFF*UP)

        self.play(
            Write(a1_label), 
            Write(equals),
            neuron.set_fill, None, 0.3,
            run_time = 1
        )
        self.play(MoveToTarget(a_labels, run_time = 1.5))
        self.play(
            Write(w_labels),
            Write(symbols),
        )

        self.a1_label = a1_label
        self.a1_equals = equals
        self.w_labels = w_labels
        self.a_labels_in_sum = a_labels
        self.symbols = symbols
        self.weighted_sum = VGroup(w_labels, a_labels, symbols)

    def add_bias(self):
        weighted_sum = self.weighted_sum
        bias = OldTex("+\\,", "b_0")
        bias.scale(0.75)
        bias.next_to(weighted_sum, RIGHT, SMALL_BUFF)
        bias.shift(0.5*SMALL_BUFF*DOWN)
        name = OldTexText("Bias")
        name.scale(0.75)
        name.next_to(bias, DOWN, MED_LARGE_BUFF)
        arrow = Arrow(name, bias, buff = SMALL_BUFF)
        VGroup(name, arrow, bias).set_color(BLUE)

        self.play(
            FadeIn(name),
            FadeIn(bias),
            GrowArrow(arrow),
        )

        self.weighted_sum.add(bias)

        self.bias = bias
        self.bias_name = VGroup(name, arrow)

    def add_sigmoid(self):
        weighted_sum = self.weighted_sum
        weighted_sum.generate_target()
        sigma, lp, rp = mob = OldTex("\\sigma\\big(\\big)")
        # mob.scale(0.75)
        sigma.move_to(weighted_sum.get_left())
        sigma.shift(0.5*SMALL_BUFF*(DOWN+RIGHT))
        lp.next_to(sigma, RIGHT, SMALL_BUFF)
        weighted_sum.target.next_to(lp, RIGHT, SMALL_BUFF)
        rp.next_to(weighted_sum.target, RIGHT, SMALL_BUFF)

        name = OldTexText("Sigmoid")
        name.next_to(sigma, UP, MED_LARGE_BUFF)
        arrow = Arrow(name, sigma, buff = SMALL_BUFF)
        sigmoid_name = VGroup(name, arrow)
        VGroup(sigmoid_name, mob).set_color(YELLOW)

        self.play(
            FadeIn(mob),
            MoveToTarget(weighted_sum),
            MaintainPositionRelativeTo(self.bias_name, self.bias),
        )
        self.play(FadeIn(sigmoid_name))

        self.sigma = sigma
        self.sigma_parens = VGroup(lp, rp)
        self.sigmoid_name = sigmoid_name

    ##

    def organize_activations_into_column(self):
        a_labels = self.a_labels.copy()
        a_labels.generate_target()
        column = a_labels.target
        a_labels_in_sum = self.a_labels_in_sum

        dots = OldTex("\\vdots")
        mid_as = VGroup(*column[2:-1])
        # CHANGE: Cairo's `Transform(group, dots).update(1)` left every member of the group as a copy of dots in place; GL's left some members behind (column got 5.8 units wide and the matrix brackets huge). Do it explicitly with become().
        for k, mid_a in enumerate(mid_as):
            mid_a.become(dots.copy())
            if k > 0:
                mid_a.set_opacity(0)
        last_a = column[-1]
        new_last_a = OldTex(
            last_a.get_tex().replace("7", "n")
        )
        new_last_a.replace(last_a)
        # CHANGE: Same: explicit become() instead of Transform(...).update(1).
        last_a.become(new_last_a)

        VGroup(
            # CHANGE: Cairo mobject slices were lists; GL returns a group, so convert before concatenating with lists.
            *list(column[:2]) + [mid_as] + [column[-1]]
        ).arrange(DOWN)
        column.shift(DOWN + 3.5*RIGHT)

        pre_brackets = self.get_brackets(a_labels)
        post_bracketes = self.get_brackets(column)
        pre_brackets.set_fill(opacity = 0)

        self.play(FocusOn(self.a_labels[0]))
        self.play(LaggedStartMap(
            Indicate, self.a_labels,
            rate_func = there_and_back,
            run_time = 1
        ))
        self.play(
            MoveToTarget(a_labels),
            Transform(pre_brackets, post_bracketes),
            run_time = 2
        )
        self.wait()
        self.play(*[
            LaggedStartMap(Indicate, mob, rate_func = there_and_back)
            for mob in (a_labels, a_labels_in_sum)
        ])
        self.wait()

        self.a_column = a_labels
        self.a_column_brackets = pre_brackets

    def organize_weights_as_matrix(self):
        a_column = self.a_column
        a_column_brackets = self.a_column_brackets
        w_brackets = a_column_brackets.copy()
        w_brackets.next_to(a_column_brackets, LEFT, SMALL_BUFF)
        lwb, rwb = w_brackets

        w_labels = self.w_labels.copy()
        w_labels.submobjects.insert(
            2, self.symbols[-2].copy()
        )
        w_labels.generate_target()
        w_labels.target.arrange(RIGHT)
        w_labels.target.next_to(a_column[0], LEFT, buff = 0.8)
        lwb.next_to(w_labels.target, LEFT, SMALL_BUFF)
        lwb.align_to(rwb, UP)

        row_1, row_k = [
            VGroup(*list(map(OldTex, [  # CHANGE: map(Tex) -> map(OldTex) (Cairo TexMobject)
                "w_{%s, 0}"%i,
                "w_{%s, 1}"%i,
                "\\cdots",
                "w_{%s, n}"%i,
            ])))
            for i in ("1", "k")
        ]
        dots_row = VGroup(*list(map(OldTex, [  # CHANGE: map(Tex) -> map(OldTex) (Cairo TexMobject)
            "\\vdots", "\\vdots", "\\ddots", "\\vdots"
        ])))

        lower_rows = VGroup(row_1, dots_row, row_k)
        lower_rows.scale(0.75)
        last_row = w_labels.target
        for row in lower_rows:
            for target, mover in zip(last_row, row):
                mover.move_to(target)
                if "w" in mover.get_tex():
                    mover.set_color(GREEN)
            row.next_to(last_row, DOWN, buff = 0.45)
            last_row = row

        self.play(
            MoveToTarget(w_labels),
            Write(w_brackets, run_time = 1)
        )
        self.play(FadeIn(
            lower_rows,
            run_time = 3,
            lag_ratio = 0.5,
        ))
        self.wait()

        self.top_matrix_row = w_labels
        self.lower_matrix_rows = lower_rows
        self.matrix_brackets = w_brackets

    def show_meaning_of_matrix_row(self):
        row = self.top_matrix_row
        edges = self.network_mob.layers[1].neurons[0].edges_in.copy()
        edges.set_stroke(GREEN, 5)
        rect = SurroundingRectangle(row, color = GREEN_B)

        self.play(ShowCreation(rect))
        for x in range(2):
            self.play(LaggedStartMap(
                ShowCreationThenDestruction, edges,
                lag_ratio = 0.8
            ))
        self.wait()

        self.top_row_rect = rect

    def connect_weighted_sum_to_matrix_multiplication(self):
        a_column = self.a_column
        a_brackets = self.a_column_brackets
        top_row_rect = self.top_row_rect

        column_rect = SurroundingRectangle(a_column)

        equals = OldTex("=")
        equals.next_to(a_brackets, RIGHT)
        result_brackets = a_brackets.copy()
        result_terms = VGroup()
        for i in 0, 1, 4, -1:
            a = a_column[i]
            if i == 4:
                mob = OldTex("\\vdots")
            else:
                # mob = Circle(radius = 0.2, color = YELLOW)
                mob = OldTex("?").scale(1.3).set_color(YELLOW)
            result_terms.add(mob.move_to(a))
        VGroup(result_brackets, result_terms).next_to(equals, RIGHT)

        brace = Brace(
            VGroup(self.w_labels, self.a_labels_in_sum), DOWN
        )
        arrow = Arrow(
            brace.get_bottom(),
            result_terms[0].get_top(), 
            buff = SMALL_BUFF 
        )

        self.play(
            GrowArrow(arrow),
            GrowFromCenter(brace),
        )
        self.play(
            Write(equals),
            FadeIn(result_brackets),
        )
        self.play(ShowCreation(column_rect))
        self.play(ReplacementTransform(
            VGroup(top_row_rect, column_rect).copy(),
            result_terms[0]
        ))
        self.play(LaggedStartMap(
            FadeIn, VGroup(*result_terms[1:])
        ))
        self.wait(2)
        self.show_meaning_of_lower_rows(
            arrow, brace, top_row_rect, result_terms
        )
        self.play(*list(map(FadeOut, [
            result_terms, result_brackets, equals, column_rect
        ])))

    def show_meaning_of_lower_rows(self, arrow, brace, row_rect, result_terms):
        n1, n2, nk = neurons = VGroup(*[
            self.network_mob.layers[1].neurons[i]
            for i in (0, 1, -1)
        ])
        for n in neurons:
            n.save_state()
            n.edges_in.save_state()

        rect2 = SurroundingRectangle(result_terms[1])
        rectk = SurroundingRectangle(result_terms[-1])
        VGroup(rect2, rectk).set_color(WHITE)
        row2 = self.lower_matrix_rows[0]
        rowk = self.lower_matrix_rows[-1]

        def show_edges(neuron):
            self.play(LaggedStartMap(
                ShowCreationThenDestruction,
                neuron.edges_in.copy().set_stroke(GREEN, 5),
                lag_ratio = 0.7,
                run_time = 1,
            ))

        self.play(
            row_rect.move_to, row2,
            n1.fade,
            n1.set_fill, None, 0,
            n1.edges_in.set_stroke, None, 1,
            n2.set_stroke, WHITE, 3,
            n2.edges_in.set_stroke, None, 3,
            ReplacementTransform(arrow, rect2),
            FadeOut(brace),
        )
        show_edges(n2)
        self.play(
            row_rect.move_to, rowk,
            n2.restore,
            n2.edges_in.restore,
            nk.set_stroke, WHITE, 3,
            nk.edges_in.set_stroke, None, 3,
            ReplacementTransform(rect2, rectk),
        )
        show_edges(nk)
        self.play(
            n1.restore,
            n1.edges_in.restore,
            nk.restore,
            nk.edges_in.restore,
            FadeOut(rectk),
            FadeOut(row_rect),
        )

    def add_bias_vector(self):
        bias = self.bias
        bias_name = self.bias_name
        a_column_brackets = self.a_column_brackets
        a_column = self.a_column

        plus = OldTex("+")
        b_brackets = a_column_brackets.copy()
        b_column = VGroup(*list(map(OldTex, [  # CHANGE: map(Tex) -> map(OldTex) (Cairo TexMobject)
            "b_0", "b_1", "\\vdots", "b_n",
        ])))
        b_column.scale(0.85)
        b_column.arrange(DOWN, buff = 0.35)
        b_column.move_to(a_column)
        b_column.set_color(BLUE)
        plus.next_to(a_column_brackets, RIGHT)
        VGroup(b_brackets, b_column).next_to(plus, RIGHT)

        bias_rect = SurroundingRectangle(bias)

        self.play(ShowCreation(bias_rect))
        self.play(FadeOut(bias_rect))
        self.play(
            Write(plus),
            Write(b_brackets),
            Transform(self.bias[1].copy(), b_column[0]),
            run_time = 1
        )
        self.play(LaggedStartMap(
            FadeIn, VGroup(*b_column[1:])
        ))
        self.wait()

        self.bias_plus = plus
        self.b_brackets = b_brackets
        self.b_column = b_column

    def apply_sigmoid(self):
        expression_bounds = VGroup(
            self.matrix_brackets[0], self.b_brackets[1]
        )
        sigma = self.sigma.copy()
        slp, srp = self.sigma_parens.copy()

        big_lp, big_rp = parens = OldTex("()")
        parens.scale(3)
        parens.stretch_to_fit_height(expression_bounds.get_height())
        big_lp.next_to(expression_bounds, LEFT, SMALL_BUFF)
        big_rp.next_to(expression_bounds, RIGHT, SMALL_BUFF)
        parens.set_color(YELLOW)

        self.play(
            sigma.scale, 2,
            sigma.next_to, big_lp, LEFT, SMALL_BUFF,
            Transform(slp, big_lp),
            Transform(srp, big_rp),
        )
        self.wait(2)

        self.big_sigma_group = VGroup(VGroup(sigma), slp, srp)

    def write_clean_final_expression(self):
        self.fade_weighted_sum()
        expression = OldTex(
            "\\textbf{a}^{(1)}", 
            "=",
            "\\sigma", 
            "\\big(", 
            "\\textbf{W}", 
            "\\textbf{a}^{(0)}",
            "+", 
            "\\textbf{b}", 
            "\\big)",
        )
        expression.set_color_by_tex_to_color_map({
            "sigma" : YELLOW,
            "big" : YELLOW,
            "W" : GREEN,
            "\\textbf{b}" : BLUE
        })
        expression.next_to(self.big_sigma_group, UP, LARGE_BUFF)
        a1, equals, sigma, lp, W, a0, plus, b, rp = expression

        neuron_anims = []
        neurons = VGroup(*self.network_mob.layers[1].neurons[1:])
        for neuron in neurons:
            neuron_anims += [
                neuron.restore,
                neuron.set_fill, None, random.random()
            ]
            neuron_anims += [
                neuron.edges_in.restore
            ]
        neurons.add_to_back(self.network_mob.layers[1].neurons[0])

        self.play(ReplacementTransform(
            VGroup(
                self.top_matrix_row, self.lower_matrix_rows,
                self.matrix_brackets
            ).copy(),
            VGroup(W), 
        ))
        self.play(ReplacementTransform(
            VGroup(self.a_column, self.a_column_brackets).copy(),
            VGroup(VGroup(a0)),
        ))
        self.play(
            ReplacementTransform(
                VGroup(self.b_column, self.b_brackets).copy(),
                VGroup(VGroup(b))
            ),
            ReplacementTransform(
                self.bias_plus.copy(), plus
            )
        )
        self.play(ReplacementTransform(
            self.big_sigma_group.copy(),
            VGroup(sigma, lp, rp)
        ))
        self.wait()
        self.play(*neuron_anims, run_time = 2)
        self.play(
            ReplacementTransform(neurons.copy(), a1),
            FadeIn(equals)
        )
        self.wait(2)

    def fade_weighted_sum(self):
        self.play(*list(map(FadeOut, [
            self.a1_label, self.a1_equals,
            self.sigma, self.sigma_parens, 
            self.weighted_sum,
            self.bias_name,
            self.sigmoid_name,
        ])))


    ###

    def get_brackets(self, mob):
        lb, rb = both = OldTex("\\big[\\big]")
        both.set_width(mob.get_width())
        both.stretch_to_fit_height(1.2*mob.get_height())
        lb.next_to(mob, LEFT, SMALL_BUFF)
        rb.next_to(mob, RIGHT, SMALL_BUFF)
        return both
